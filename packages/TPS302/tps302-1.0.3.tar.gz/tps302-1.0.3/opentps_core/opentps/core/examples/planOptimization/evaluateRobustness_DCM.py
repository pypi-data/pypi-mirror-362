
import os
import datetime
from opentps.core.io.dicomIO import readDicomPlan
import numpy as np
from matplotlib import pyplot as plt
from opentps.core.data.images import CTImage
from opentps.core.data.images import ROIMask
from opentps.core.data.plan import PlanDesign
from opentps.core.data import Patient
from opentps.core.io import mcsquareIO
from opentps.core.io.scannerReader import readScanner
from opentps.core.io.serializedObjectIO import saveRTPlan, loadRTPlan
from opentps.core.processing.doseCalculation.doseCalculationConfig import DoseCalculationConfig
from opentps.core.processing.doseCalculation.mcsquareDoseCalculator import MCsquareDoseCalculator
from opentps.core.processing.planEvaluation.robustnessEvaluation import RobustnessEval
from opentps.core.processing.imageProcessing.resampler3D import resampleImage3DOnImage3D
from opentps.core.processing.planOptimization.planOptimization import IMPTPlanOptimizer
from opentps.core.io.dataLoader import readData
output_path = os.getcwd()
from opentps.core.io.mcsquareIO import _dicomIsocenterToMCsquare
# Generic example: box of water with squared target

ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)
ctImagePath = "TG119_prostate"
data = readData(ctImagePath)
#print(data)
# #proton:RD RT RS CT
# Photon:RD RD RD RD RD RS CT
rt_struct = data[0]
ct = data[1]
rt_struct.print_ROINames()
print("CT spacing=",ct.spacing)
print("CT grid size",ct.gridSize)
target_name = "PTV"

target = rt_struct.getContourByName(target_name).getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
roi=target

OAR_Prostate = rt_struct.getContourByName("Prostate").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
OAR_bladder = rt_struct.getContourByName("Urinary bladder").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
OAR_Rectum = rt_struct.getContourByName("Rectum").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
#
COM_coord = target.centerOfMass
COM_index = target.getVoxelIndexFromPosition(COM_coord)
Z_COORD = COM_index[2]
iso_pos=_dicomIsocenterToMCsquare(roi.centerOfMass, ct.origin, ct.spacing, ct.gridSize)
iso_roi=roi.centerOfMass
print(iso_pos)
print(iso_roi)

#
mc2 = MCsquareDoseCalculator()
mc2.beamModel = bdl
mc2.ctCalibration = ctCalibration

# Create output folder
if not os.path.isdir(output_path):
    os.mkdir(output_path)

# Configure MCsquare
mc2 = MCsquareDoseCalculator()
mc2.beamModel = bdl
mc2.nbPrimaries = 5e4
mc2.statUncertainty = 2.
mc2.ctCalibration = ctCalibration

# Load / Generate new plan
plan_path = output_path +'/'+"IMPT_test_ROB.tps"
plan = loadRTPlan(plan_path)



# Load / Generate scenarios
scenario_name="IMPT_ROB_EVAL"
scenario_folder = os.path.join(output_path,scenario_name)
if os.path.isdir(scenario_folder):
    scenarios = RobustnessEval()
    scenarios.selectionStrategy = RobustnessEval.Strategies.REDUCED_SET
    scenarios.setupSystematicError = plan.planDesign.robustness.setupSystematicError
    scenarios.setupRandomError = plan.planDesign.robustness.setupRandomError
    scenarios.rangeSystematicError = plan.planDesign.robustness.rangeSystematicError
    scenarios.load(scenario_folder)
    print("scenarios loaded")
else:
    # MCsquare config for scenario dose computation
    plan.planDesign.targetMargin = 5.0
    mc2.nbPrimaries = 1e7
    plan.planDesign.robustnessEval = RobustnessEval()
    plan.planDesign.robustnessEval.setupSystematicError = [5.0, 5.0, 5.0]  # mm
    plan.planDesign.robustnessEval.setupRandomError = [0.0, 0.0, 0.0]  # mm (sigma)
    plan.planDesign.robustnessEval.rangeSystematicError = 3.0  # %
    plan.planDesign.robustnessEval.selectionStrategy = RobustnessEval.Strategies.REDUCED_SET
    # run MCsquare simulation
    scenarios = mc2.computeRobustScenario(ct, plan, [roi])
    scenarios.numScenarios=21
    if not os.path.isdir(output_path):
      os.mkdir(output_path)
    output_folder = os.path.join(output_path, scenario_name)
    scenarios.save(output_folder)
#mc2.nbPrimaries = 1e7
#doseImage = mc2.computeDose(ct, plan)
#solver = IMPTPlanOptimizer(method='Scipy-LBFGS', plan=plan, maxit=100)
# Optimize treatment plan
#w, doseImage, ps = solver.optimize()

# center of mass
roi = resampleImage3DOnImage3D(roi, ct)
COM_coord = roi.centerOfMass
COM_index = roi.getVoxelIndexFromPosition(COM_coord)
Z_coord = COM_index[2]

img_ct = ct.imageArray[:, :, Z_coord].transpose(1, 0)
contourTargetMask = roi.getBinaryContourMask()
img_mask = contourTargetMask.imageArray[:, :, Z_coord].transpose(1, 0)
#img_dose = resampleImage3DOnImage3D(doseImage, ct)
#img_dose = img_dose.imageArray[:, :, Z_coord].transpose(1, 0)

# Display dose
#fig, ax = plt.subplots(1, 1, figsize=(12, 5))
#ax.imshow(img_ct, cmap='gray')
#ax.imshow(img_mask, alpha=.2, cmap='binary')  # PTV
#dose = ax.imshow(img_dose, cmap='jet', alpha=.2)
#plt.colorbar(dose, ax=ax)
# Robustness analysis
scenarios.analyzeErrorSpace(ct, "D95", roi, plan.planDesign.objectives.targetPrescription)
scenarios.printInfo()
scenarios.recomputeDVH([roi])

# Display DVH + DVH-bands
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
for dvh_band in scenarios.dvhBands:
    phigh = ax.plot(dvh_band._dose, dvh_band._volumeHigh, alpha=0.1)
    plow = ax.plot(dvh_band._dose, dvh_band._volumeLow, alpha=0.1)
    pNominal = ax.plot(dvh_band._nominalDVH._dose, dvh_band._nominalDVH._volume, label=dvh_band._roiName, color = 'C0')
    pfill = ax.fill_between(dvh_band._dose, dvh_band._volumeHigh, dvh_band._volumeLow, alpha=0.4, color='C0')
ax.set_xlabel("Dose (Gy)")
ax.set_ylabel("Volume (%)")
plt.grid(True)
plt.legend()

plt.show()

