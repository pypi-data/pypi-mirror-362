import copy

import numpy as np
from matplotlib import pyplot as plt
#Import the needed opentps.core packages
import time
import os
import logging
import math
import numpy as np
from matplotlib import pyplot as plt
import sys
from opentps.core.io.dicomIO import writeRTPlan
from opentps.core.processing.planOptimization.tools import evaluateClinical
from opentps.core.data.images import CTImage
from opentps.core.data.images import ROIMask
from opentps.core.data.plan import ObjectivesList
from opentps.core.data.plan import PlanDesign
from opentps.core.data import DVH
from opentps.core.data import Patient
from opentps.core.data.plan import FidObjective
from opentps.core.io.scannerReader import readScanner
from opentps.core.io.serializedObjectIO import saveRTPlan, loadRTPlan
from opentps.core.processing.doseCalculation.doseCalculationConfig import DoseCalculationConfig
from opentps.core.processing.doseCalculation.mcsquareDoseCalculator import MCsquareDoseCalculator
from opentps.core.processing.imageProcessing.resampler3D import resampleImage3DOnImage3D, resampleImage3D
from opentps.core.processing.C_libraries.libRayTracing_wrapper import WET_raytracing
from opentps.core.processing.planOptimization.planOptimization import IMPTPlanOptimizer
from opentps.core.data.plan import PlanDesign
from opentps.core.data import DVH
from opentps.core.io import mcsquareIO
from opentps.core.io.mcsquareIO import _dicomIsocenterToMCsquare
from opentps.core.io.scannerReader import readScanner
from opentps.core.processing.doseCalculation.doseCalculationConfig import DoseCalculationConfig
from opentps.core.processing.doseCalculation.mcsquareDoseCalculator import MCsquareDoseCalculator
from opentps.core.io.dataLoader import readData
from opentps.core.data.plan import ObjectivesList
from opentps.core.data.plan import FidObjective
from opentps.core.io.serializedObjectIO import saveBeamlets, saveRTPlan, loadBeamlets, loadRTPlan

# ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
#
# bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)
#
# patient = Patient()
# patient.name = 'Patient'
#
# ctSize = 150
#
# ct = CTImage()
# ct.name = 'CT'
# ct.patient = patient
#
# huAir = -1024.
# huWater = ctCalibration.convertRSP2HU(1.)
# data = huAir * np.ones((ctSize, ctSize, ctSize))
# data[:, 50:, :] = huWater
# ct.imageArray = data
#
# roi = ROIMask()
# roi.patient = patient
# roi.name = 'TV'
# roi.color = (255, 0, 0)  # red
# data = np.zeros((ctSize, ctSize, ctSize)).astype(bool)
# data[100:120, 100:120, 100:120] = True
# roi.imageArray = data

# ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
# bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)
# ctImagePath = "D:/0/"
# data = readData(ctImagePath)
# #print(data)
# # #proton:RD RT RS CT
# # Photon:RD RD RD RD RD RS CT
# rt_struct = data[1]
# ct = data[2]
# rt_struct.print_ROINames()
# print("CT spacing=",ct.spacing)
# print("CT grid size",ct.gridSize)
# target_name = "PTV_7920"
# target = rt_struct.getContourByName(target_name).getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
# roi=target
# print(type(roi))
# print(roi.imageArray.shape)
# OAR_L = rt_struct.getContourByName("Femur_L").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
# OAR_R = rt_struct.getContourByName("Femur_R").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
# OAR_Rectum = rt_struct.getContourByName("Rectum").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
# #
# COM_coord = target.centerOfMass
# COM_index = target.getVoxelIndexFromPosition(COM_coord)
# Z_COORD = COM_index[2]
# #
# mc2 = MCsquareDoseCalculator()
# mc2.beamModel = bdl
# mc2.ctCalibration = ctCalibration
############################################### 0604 TG119 TEST ##############################################
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
#######################################################      functions      ################################################################################################

###########################################################    setting plan parameters   ##########################################################
gantryAngles = [90]
couchAngles = [0]
beamNames = []
for i in range(len(gantryAngles)):
    beamNames.append("Beam%s" % i)
planDesign = PlanDesign()
planDesign.ct = ct
planDesign.gantryAngles = gantryAngles
planDesign.targetMask = roi
planDesign.beamNames = beamNames
planDesign.couchAngles = couchAngles
planDesign.calibration = ctCalibration
planDesign.robustness.setupSystematicError = [5.0, 5.0, 5.0]  # mm
planDesign.robustness.setupRandomError = [0.0, 0.0, 0.0]  # mm (sigma)
planDesign.robustness.rangeSystematicError = 3.0  # %

# Regular scenario sampling
planDesign.robustness.selectionStrategy = planDesign.robustness.Strategies.REDUCED_SET

# All scenarios (includes diagonals on sphere)
# planDesign.robustness.selectionStrategy = planDesign.robustness.Strategies.ALL

# Random scenario sampling
# planDesign.robustness.selectionStrategy = planDesign.robustness.Strategies.RANDOM
# planDesign.robustness.numScenarios = 5 # specify how many random scenarios to simulate, default = 100

planDesign.spotSpacing = 5.0
planDesign.layerSpacing = 5.0
planDesign.targetMargin = max(planDesign.spotSpacing, planDesign.layerSpacing) + max(
    planDesign.robustness.setupSystematicError)

planDesign.targetMargin = max(planDesign.spotSpacing, planDesign.layerSpacing) + max(planDesign.robustness.setupSystematicError)
planDesign.setScoringParameters(scoringSpacing=[2, 2, 2], adapt_gridSize_to_new_spacing=True)
# needs to be called after scoringGrid settings but prior to spot placement
planDesign.defineTargetMaskAndPrescription(target = roi, targetPrescription = 80.)
plan = planDesign.buildPlan()  # Spot placement


# # ########################################                 Beamlet Calculate                             ############################################################################
#Configure MCsquare
output_path=os.getcwd()
BLpath=os.path.join(output_path, "IMPT_test_ROB")
if not os.path.isdir(BLpath):
    os.mkdir(BLpath)
mc2 = MCsquareDoseCalculator()
mc2.beamModel = bdl
mc2.nbPrimaries = 5e3
mc2.ctCalibration = ctCalibration
nominal, scenarios = mc2.computeRobustScenarioBeamlets(ct, plan,roi=[roi] ,storePath=BLpath)
plan.planDesign.beamlets = nominal
plan.planDesign.robustness.scenarios = scenarios
plan.planDesign.robustness.numScenarios = len(scenarios)
plan.PlanName = "NewPlan"

#########################################                  Plan Opti  patient0                                   ###############################################################
# plan_selected.planDesign.objectives = ObjectivesList()
# plan_selected.planDesign.objectives.setTarget(roi.name, 60.0)
# plan_selected.planDesign.objectives.fidObjList = []
# plan_selected.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMAX, 61.0, 1.0)
# plan_selected.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMIN, 58.5, 1.0)
# solver = IMPTPlanOptimizer(method='Scipy-LBFGS', plan=plan_selected, maxit=1000)
# # Optimize treatment plan
# w, doseImage, ps = solver.optimize()
#########################################                  Plan Opti  TG119 prostate                                  ###############################################################

plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMAX, 83.0, 100.0,robust=True)
plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMIN, 75.6, 100.0,robust=True)
plan.planDesign.objectives.addFidObjective(OAR_Rectum, FidObjective.Metrics.DMAX, 77.0, 50.0)
plan.planDesign.objectives.addFidObjective(OAR_bladder, FidObjective.Metrics.DMAX, 75.0, 10.0)
solver = IMPTPlanOptimizer(method='Scipy_L-BFGS-B', plan=plan, maxiter=100)
# Optimize treatment plan
doseImage, ps = solver.optimize()

#########################################                  Dicom Plan  output         ######################################################################

patient = Patient()
patient.name = 'Patient'
plan.patient = patient
output_path = os.getcwd()
tps_file = os.path.join(output_path, "IMPT_test_ROB.tps")
#writeRTPlan(plan, output_path,"IMPT_ROBOPTI.dcm")
saveRTPlan(plan, tps_file)
########################################                DVH and Dose display                          ##################################################################
#MCsquare simulation
mc2.nbPrimaries = 1e7
doseImage = mc2.computeDose(ct, plan)
# Compute DVH on resampled contour
target_DVH = DVH(roi, doseImage)
rectum_DVH = DVH(OAR_Rectum,doseImage)
bladder_DVH = DVH(OAR_bladder,doseImage)

print('D5 - D95 =  {} Gy'.format(target_DVH.D5 - target_DVH.D95))
clinROI = [roi.name, roi.name]
clinMetric = ["Dmin", "Dmax"]
clinLimit = [75.6, 83]
clinObj = {'ROI': clinROI, 'Metric': clinMetric, 'Limit': clinLimit}
print('Clinical evaluation')
evaluateClinical(doseImage, [roi], clinObj)

print("OAR_Rectum D30 : ",rectum_DVH.D30)
print("OAR_Rectum D10 : ",rectum_DVH.D10)
print("OAR_Bladder D30 : ",bladder_DVH.D30)
print("OAR_Bladder D10 : ",bladder_DVH.D10)
evaluateClinical(doseImage, [OAR_bladder], clinObj)
# center of mass
roi = resampleImage3DOnImage3D(roi, ct)
COM_coord = roi.centerOfMass
COM_index = roi.getVoxelIndexFromPosition(COM_coord)
Z_coord = COM_index[2]

img_ct = ct.imageArray[:, :, Z_coord].transpose(1, 0)
contourTargetMask = roi.getBinaryContourMask()
img_mask = contourTargetMask.imageArray[:, :, Z_coord].transpose(1, 0)
img_dose = resampleImage3DOnImage3D(doseImage, ct)
img_dose = img_dose.imageArray[:, :, Z_coord].transpose(1, 0)
image_rectum_axial = OAR_Rectum.imageArray[:,:,Z_COORD].transpose(1,0)
image_bladder_axial = OAR_bladder.imageArray[:,:,Z_COORD].transpose(1,0)
# Display dose
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
ax[0].axes.get_xaxis().set_visible(False)
ax[0].axes.get_yaxis().set_visible(False)
ax[0].imshow(img_ct, cmap='gray')
ax[0].imshow(img_mask, alpha=.2, cmap='binary')  # PTV
ax[0].contour(image_rectum_axial,colors="red",alpha=.2)
ax[0].contour(image_bladder_axial,colors="green")
dose = ax[0].imshow(img_dose, cmap='jet', alpha=.2)
plt.colorbar(dose, ax=ax[0])
ax[1].plot(target_DVH.histogram[0], target_DVH.histogram[1], label=target_DVH.name)
ax[1].plot(rectum_DVH.histogram[0], rectum_DVH.histogram[1], label=rectum_DVH.name)
ax[1].plot(bladder_DVH.histogram[0], bladder_DVH.histogram[1], label=bladder_DVH.name)
ax[1].set_xlabel("Dose (Gy)")
ax[1].set_ylabel("Volume (%)")
ax[1].grid(True)
ax[1].legend()
plt.show()

###

