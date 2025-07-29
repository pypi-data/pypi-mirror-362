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


############################################### 0604 TG119 TEST ##############################################
ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)
ctImagePath = "/home/user/miniconda3/envs/tps302/lib/python3.9/site-packages/opentps/core/examples/planOptimization/TG119_prostate"
data = readData(ctImagePath)
print(data)
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

OAR_Rectum = rt_struct.getContourByName("Rectum").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
#
COM_coord = target.centerOfMass
COM_index = target.getVoxelIndexFromPosition(COM_coord)
Z_COORD = COM_index[2]
iso_pos=_dicomIsocenterToMCsquare(roi.centerOfMass, ct.origin, ct.spacing, ct.gridSize)
iso_roi=roi.centerOfMass

#
mc2 = MCsquareDoseCalculator()
mc2.beamModel = bdl
mc2.ctCalibration = ctCalibration

###########################################################    setting plan parameters   ##########################################################
gantryAngles = [90]
couchAngles = [0]
beamNames = ["Beam1"]
planDesign = PlanDesign()
planDesign.ct = ct
planDesign.gantryAngles = gantryAngles
planDesign.beamNames = beamNames
planDesign.couchAngles = couchAngles
planDesign.calibration = ctCalibration
planDesign.spotSpacing = 5.0
planDesign.layerSpacing = 5.0
planDesign.targetMargin = 5.0
planDesign.setScoringParameters(scoringSpacing=[2, 2, 2], adapt_gridSize_to_new_spacing=True)
# needs to be called after scoringGrid settings but prior to spot placement
planDesign.defineTargetMaskAndPrescription(target = roi, targetPrescription = 80.) 

plan = planDesign.buildPlan()  # Spot placement
plan.PlanName = "NewPlan"


def find_closest_value(arr, value):
    """
    使用NumPy找到数组中与给定值最接近的元素

    参数:
    arr -- NumPy数组
    value -- 给定的值

    返回:
    数组中与给定值最接近的元素
    """
    # 计算数组中每个元素与给定值的差的绝对值
    abs_diff = np.abs(arr - value)
    # 找到绝对值最小的索引
    min_index = np.argmin(abs_diff)
    # 返回对应的元素
    return arr[min_index]

Raystation_Energy = [ 70.6,72.1,73.5,75,76.5,77.9,79.4,80.9,82.4,83.8,85.3,86.8,88.3,89.8,91.2,92.7,94.2,95.7,97.2,98.7,100.2,101.8,103.3,104.8,106.3,107.9,109.4,111,112.5,114.1,115.6,117.2,118.8,120.4,122,123.6,125.2,126.8,128.5,130.1,131.7,133.4,135.1,136.7,138.4,140.1,141.8,143.5,145.2,147,148.7,150.4,152.2,154,155.7,157.5,159.3,161.1,163,164.8,166.6,168.5,170.4,172.3,174.2,176.1,178,179.9,181.8,183.8,185.8,187.8,189.8,191.8,193.8,195.8,197.9,199.9,202,204.1,206.2,208.3,210.5,212.6,214.8,217,219.2,221.4,223.6,225.9,228.1,230.4,232.7,235 ]
Raystation_Energy =np.array(Raystation_Energy)
for beam in plan.beams:
    for layer in beam:
        energy=layer.nominalEnergy
        new_energy=find_closest_value(Raystation_Energy,energy)
        layer.nominalEnergy=new_energy
#########################################                 Beamlet Calculate                             ############################################################################
#Configure MCsquare
mc2 = MCsquareDoseCalculator()
mc2.beamModel = bdl
mc2.nbPrimaries = 5e4
mc2.ctCalibration = ctCalibration
beamlets = mc2.computeBeamlets(ct, plan)
plan.planDesign.beamlets = beamlets
#
#
#
#########################################                  Plan Opti  TG119 prostate                                  ###############################################################
plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMAX, 83.0, 100.0) #83.0为剂量，100为权重
plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMIN, 75.6, 100.0)#75.6为剂量，100为权重
plan.planDesign.objectives.addFidObjective(OAR_Rectum, FidObjective.Metrics.DMAX, 83.0, 50.0)
# plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMEAN, 20, 1.0) 
# plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DUNIFORM, 20, 1.0)
# plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DVHMIN, 19, 1.0, volume = 95)#D95< 19 Gy
# plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DVHMAX, 21, 1.0, volume = 5)
# plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.EUDMIN, 19.5, 1.0, EUDa = 0.2)
# plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.EUDMAX, 20, 1.0, EUDa = 1)
# plan.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.EUDUNIFORM, 20.5, 1.0, EUDa = 0.5)

solver = IMPTPlanOptimizer(method='Scipy_L-BFGS-B', plan=plan, maxiter=100)
# Optimize treatment plan
doseImage, ps  = solver.optimize()
doseImage.patient = plan.patient
#########################################                  Dicom Plan  output         ######################################################################

patient = Patient()
patient.name = 'Patient'
plan.patient = patient
output_path = os.getcwd()
writeRTPlan(plan,output_path,"IMPT-94Energy.dcm")
saveRTPlan(plan,output_path+"/IMPT-94Energy.tps")
########################################                DVH and Dose display                          ##################################################################
#MCsquare simulation
mc2.nbPrimaries = 1e7
doseImage = mc2.computeDose(ct, plan)
# Compute DVH on resampled contour
target_DVH = DVH(roi, doseImage)
rectum_DVH = DVH(OAR_Rectum,doseImage)

print('D5 - D95 =  {} Gy'.format(target_DVH.D5 - target_DVH.D95))
clinROI = [roi.name, roi.name]
clinMetric = ["Dmin", "Dmax"]
clinLimit = [75.6, 83]
clinObj = {'ROI': clinROI, 'Metric': clinMetric, 'Limit': clinLimit}
print('Clinical evaluation')
evaluateClinical(doseImage, [roi], clinObj)

print("OAR_Rectum D30 : ",rectum_DVH.D30)
print("OAR_Rectum D10 : ",rectum_DVH.D10)
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
# Display dose
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
ax[0].axes.get_xaxis().set_visible(False)
ax[0].axes.get_yaxis().set_visible(False)
ax[0].imshow(img_ct, cmap='gray')
ax[0].imshow(img_mask, alpha=.2, cmap='binary')  # PTV
ax[0].contour(image_rectum_axial,colors="red",alpha=.2)
dose = ax[0].imshow(img_dose, cmap='jet', alpha=.2)
plt.colorbar(dose, ax=ax[0])
ax[1].plot(target_DVH.histogram[0], target_DVH.histogram[1], label=target_DVH.name)
ax[1].plot(rectum_DVH.histogram[0], rectum_DVH.histogram[1], label=rectum_DVH.name)
ax[1].set_xlabel("Dose (Gy)")
ax[1].set_ylabel("Volume (%)")
ax[1].grid(True)
ax[1].legend()
plt.show()
#
