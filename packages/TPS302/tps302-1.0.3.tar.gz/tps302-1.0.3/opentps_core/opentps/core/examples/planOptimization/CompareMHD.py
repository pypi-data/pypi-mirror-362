from opentps.core.io.mhdIO import exportImageMHD, importImageMHD
from opentps.core.io.mcsquareIO import readDose
from opentps.core.io.serializedObjectIO import saveBeamlets, saveRTPlan, loadBeamlets, loadRTPlan
from opentps.core.processing.dataComparison.gammaIndex import xyz_axes_from_dataset,gammaIndex,computePassRate
import copy
from opentps.core.data import DVH
import os
import logging
import numpy as np
from opentps.core.io import mcsquareIO
from opentps.core.io.scannerReader import readScanner
from opentps.core.processing.doseCalculation.doseCalculationConfig import DoseCalculationConfig
from opentps.core.processing.doseCalculation.mcsquareDoseCalculator import MCsquareDoseCalculator
from opentps.core.io.dataLoader import readData
from opentps.core.data.plan import ObjectivesList
from opentps.core.data.plan import FidObjective
from opentps.core.io.serializedObjectIO import saveBeamlets, saveRTPlan, loadBeamlets, loadRTPlan
from opentps.core.processing.imageProcessing.resampler3D import resampleImage3DOnImage3D, resampleImage3D
output_path = os.path.dirname(__file__)
ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)
from opentps.core.io.dicomIO import writeRTDose
############################################### 0604 TG119 TEST ##############################################
ctImagePath = "C:/Users/gcyyy/Desktop/TG119_prostate"
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
from matplotlib import pyplot as plt
target = rt_struct.getContourByName(target_name).getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
roi=target

OAR_Prostate = rt_struct.getContourByName("Prostate").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
OAR_bladder = rt_struct.getContourByName("Urinary bladder").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
OAR_Rectum = rt_struct.getContourByName("Rectum").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
#
COM_coord = target.centerOfMass
COM_index = target.getVoxelIndexFromPosition(COM_coord)
Z_COORD = COM_index[2]
plan_path="Arcplan_CSS_new_90GA_Opti_SpotReduction_layer_redistribution.tps"
plan = loadRTPlan(output_path+"/"+plan_path)
bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)

mc2 = MCsquareDoseCalculator()
mc2.nbPrimaries = 1e7
mc2.beamModel = bdl
mc2.ctCalibration = ctCalibration

##############################################################################################
plan2_path=output_path+"/"+"DynamicChecktemp.tps"
plan2 = loadRTPlan(plan2_path)
mc2_2 = MCsquareDoseCalculator()
mc2_2._ct=ct
mc2_2._plan=plan2
DosePath="C:/Users/gcyyy/Desktop/Arc_MHD/Dose.mhd"
mc2_2._doseFilePath=DosePath
#mc2_2.nbPrimaries = 1e7
mc2_2.beamModel = bdl
mc2_2.ctCalibration = ctCalibration
doseImage2=mc2_2._importDose(plan2)
# MCsquare simulation
#mc2.nbPrimaries = 1e7
#doseImage1 = mc2.computeDose(ct, plan)
#writeRTDose(doseImage1, "C:/Users/gcyyy/Desktop/DynamicArcCheck/Static",plan_path)
RTdosename = "Arcplan_CSS_new_90GA_Opti_SpotReduction-layer_redistribution"
writeRTDose(doseImage2, "C:/Users/gcyyy/Desktop/DynamicArcCheck/Dynamic",RTdosename)
###########################################################################################################
# gamma_Image=gammaIndex(doseImage1,doseImage2,1, 1, lower_percent_dose_cutoff=20,
#                interp_fraction=10, max_gamma=None, local_gamma=False, global_normalisation=None,
#                skip_once_passed=False, random_subset=None, ram_available=int(2**30 * 4)
# )
# print("Gamma index= ",computePassRate(gamma_Image))

###################                    DVH               ###################################################
# Compute DVH on resampled contour
# target_DVH1 = DVH(roi, doseImage1)
# target_DVH2 = DVH(roi, doseImage2)
#
# # center of mass
# roi = resampleImage3DOnImage3D(roi, ct)
# COM_coord = roi.centerOfMass
# COM_index = roi.getVoxelIndexFromPosition(COM_coord)
# Z_coord = COM_index[2]
#
# img_ct = ct.imageArray[:, :, Z_coord].transpose(1, 0)
# contourTargetMask = roi.getBinaryContourMask()
# img_mask = contourTargetMask.imageArray[:, :, Z_coord].transpose(1, 0)
# img_dose1 = resampleImage3DOnImage3D(doseImage1, ct)
# img_dose1 = img_dose1.imageArray[:, :, Z_coord].transpose(1, 0)
#
#
# fig, ax = plt.subplots(1, 2, figsize=(15, 5))
# ax[0].axes.get_xaxis().set_visible(False)
# ax[0].axes.get_yaxis().set_visible(False)
# ax[0].imshow(img_ct, cmap='gray')
# ax[0].imshow(img_mask, alpha=.2, cmap='binary')  # PTV
# dose = ax[0].imshow(img_dose1, cmap='jet', alpha=.2)
# plt.colorbar(dose, ax=ax[0])
# ax[1].plot(target_DVH1.histogram[0], target_DVH1.histogram[1], label="Original")
# ax[1].plot(target_DVH2.histogram[0], target_DVH2.histogram[1], label="DynamicDose")
# ax[1].set_xlabel("Dose (Gy)")
# ax[1].set_ylabel("Volume (%)")
# ax[1].grid(True)
# ax[1].legend()
#
# plt.show()