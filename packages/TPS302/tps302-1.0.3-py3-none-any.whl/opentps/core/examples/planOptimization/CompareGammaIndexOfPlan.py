import copy

ctSize = 150
import numpy as np
from matplotlib import pyplot as plt

#Import the needed opentps.core packages
from opentps.core.data.plan._planIonBeam import PlanIonBeam
from opentps.core.data.plan._planIonLayer import PlanIonLayer
from opentps.core.data.plan._planIonSpot import PlanIonSpot
import os
import logging
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
from opentps.core.io import mcsquareIO
from opentps.core.io.scannerReader import readScanner
from opentps.core.io.serializedObjectIO import saveRTPlan, loadRTPlan
from opentps.core.processing.doseCalculation.doseCalculationConfig import DoseCalculationConfig
from opentps.core.processing.doseCalculation.mcsquareDoseCalculator import MCsquareDoseCalculator
from opentps.core.processing.imageProcessing.resampler3D import resampleImage3DOnImage3D, resampleImage3D
from opentps.core.processing.planOptimization.planOptimization import IMPTPlanOptimizer
from opentps.core.data.plan import PlanDesign
from opentps.core.data import DVH
from opentps.core.io import mcsquareIO
from opentps.core.io.scannerReader import readScanner
from opentps.core.processing.doseCalculation.doseCalculationConfig import DoseCalculationConfig
from opentps.core.processing.doseCalculation.mcsquareDoseCalculator import MCsquareDoseCalculator
from opentps.core.io.dataLoader import readData
from opentps.core.data.plan import ObjectivesList
from opentps.core.data.plan import FidObjective
from opentps.core.io.serializedObjectIO import saveBeamlets, saveRTPlan, loadBeamlets, loadRTPlan
from opentps.core.processing.dataComparison.gammaIndex import xyz_axes_from_dataset,gammaIndex,computePassRate

from opentps.core.io.dicomIO import writeRTPlan, writeDicomCT, writeRTDose, writeRTStruct
###########################################        OPENTPS WATER     ###############################################################
# output_path = os.getcwd()
# plan_path1="Plan_Fixed_Angle.tps"
# plan1 = loadRTPlan(plan_path1)
# plan_path2="Plan_DynamicAngle.tps"
# plan2 = loadRTPlan(plan_path1)

# ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
# bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)
#
# patient = Patient()
# patient.name = 'Patient'
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
########################################################             TG119 prostate               ###########################################################################
# output_path = os.getcwd()
# # plan_path1="Arcplan_CSS_new_90GA_Opti.tps"
# # plan1 = loadRTPlan(plan_path1)
# # plan_path2="Arcplan_CSS_new_90GA_Opti_DynamicAngle.tps"
# # plan2 = loadRTPlan(plan_path1)
# ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
# bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)
# ctImagePath = "C:/Users/gcyyy/Desktop/TG119_prostate"
# data = readData(ctImagePath)
# #print(data)
# # #proton:RD RT RS CT
# # Photon:RD RD RD RD RD RS CT
# rt_struct = data[0]
# ct = data[1]
# rt_struct.print_ROINames()
# print("CT spacing=",ct.spacing)
# print("CT grid size",ct.gridSize)
# target_name = "PTV"

# target = rt_struct.getContourByName(target_name).getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
# roi=target

# OAR_Prostate = rt_struct.getContourByName("Prostate").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
# OAR_bladder = rt_struct.getContourByName("Urinary bladder").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
# OAR_Rectum = rt_struct.getContourByName("Rectum").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
# #
# COM_coord = target.centerOfMass
# COM_index = target.getVoxelIndexFromPosition(COM_coord)
# Z_COORD = COM_index[2]
######################################################         DOSE CALCULATION      #############################################################################
# mc2 = MCsquareDoseCalculator()
# mc2.beamModel = bdl
# mc2.nbPrimaries = 5e4
# mc2.ctCalibration = ctCalibration
#
# # MCsquare simulation
# mc2.nbPrimaries = 1e7
# doseImage1 = mc2.computeDose(ct, plan1)
# doseImage2 = mc2.computeDose(ct, plan2)
#
# # Compute DVH on resampled contour
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
# # Don't delete it
# doseImage1.referencePlan = plan1
# doseImage1.referenceCT = ct
# doseImage2.referencePlan = plan2
# doseImage2.referenceCT = ct
# writeRTDose(doseImage1, output_path)
# writeRTDose(doseImage2, output_path)
#
# fig, ax = plt.subplots(1, 2, figsize=(15, 5))
# ax[0].axes.get_xaxis().set_visible(False)
# ax[0].axes.get_yaxis().set_visible(False)
# ax[0].imshow(img_ct, cmap='gray')
# ax[0].imshow(img_mask, alpha=.2, cmap='binary')  # PTV
# dose = ax[0].imshow(img_dose1, cmap='jet', alpha=.2)
# plt.colorbar(dose, ax=ax[0])
# ax[1].plot(target_DVH1.histogram[0], target_DVH1.histogram[1], label="target_DVH1")
# ax[1].plot(target_DVH2.histogram[0], target_DVH2.histogram[1], label="target_DVH2")
# ax[1].set_xlabel("Dose (Gy)")
# ax[1].set_ylabel("Volume (%)")
# ax[1].grid(True)
# ax[1].legend()
#
# plt.show()
#
# gamma_Image=gammaIndex(doseImage1,doseImage2,1, 1, lower_percent_dose_cutoff=20,
#                interp_fraction=10, max_gamma=None, local_gamma=False, global_normalisation=None,
#                skip_once_passed=False, random_subset=None, ram_available=int(2**30 * 4)
# )
# print("Gamma index= ",computePassRate(gamma_Image))

############################################################         GAMMA INDEX           ########################################################################

#
# # reference_filepath=output_path+"/"+"RD1.2.826.0.1.3680043.8.498.54035127769693224855749760027886893510.dcm" #WATER ORIGINAL
# # evaluation_filepath=output_path+"/"+"RD1.2.826.0.1.3680043.8.498.31356163708435341239357020297642502791.dcm" #WATER DYNAMIC
import pydicom
import pymedphys
# reference_filepath=output_path+"/"+"RD1.2.826.0.1.3680043.8.498.69327382680056856025233491995892662997.dcm" #patient ORIGINAL
# evaluation_filepath=output_path+"/"+"RD1.2.826.0.1.3680043.8.498.51753181714929711259635350596694363186.dcm" #patient DYNAMIC
# reference_filepath=output_path+"/"+"RD1.2.826.0.1.3680043.8.498.45843219279613395029686892390951350881.dcm" #patient ORIGINAL
# evaluation_filepath=output_path+"/"+"RD1.2.826.0.1.3680043.8.498.12855534024498979538361437145251430617.dcm" #patient DYNAMIC NEW 1GA
#evaluation_filepath=output_path+"/"+"RD1.2.826.0.1.3680043.8.498.16330865473291672235500786499350053800.dcm" #patient DYNAMIC NEW 0.5GA speed
# reference_filepath="C:/Users/gcyyy/Desktop/DynamicArcCheck/Static"+"/"+"ArcplanCSSnew90GAOptiSpotReductionlayerredistributiontps.dcm" #patient ORIGINAL
# evaluation_filepath="C:/Users/gcyyy/Desktop/DynamicArcCheck/Dynamic"+"/"+"ArcplanCSSnew90GAOptiSpotReductionlayerredistribution_1.dcm" #patient DYNAMIC NEW 1GA
reference_filepath="E:\OpenTPS\opentps-master\opentps_core\opentps\core\examples\planOptimization\AOCHANGJIAN/RD1.2.752.243.1.1.20250116144115074.1200.46086.dcm" #patient ORIGINAL
evaluation_filepath="E:\OpenTPS\opentps-master\opentps_core\opentps\core\examples\planOptimization\opentpsSFRT250116dcm.dcm" #patient DYNAMIC NEW 1GA
reference = pydicom.read_file(str(reference_filepath), force=True)
evaluation = pydicom.read_file(str(evaluation_filepath), force=True)
axes_reference, dose_reference = pymedphys.dicom.zyx_and_dose_from_dataset(reference)
axes_evaluation, dose_evaluation = pymedphys.dicom.zyx_and_dose_from_dataset(evaluation)
# axes_reference, dose_reference0 = pymedphys.dicom.zyx_and_dose_from_dataset(reference)
# axes_evaluation, dose_evaluation0 = pymedphys.dicom.zyx_and_dose_from_dataset(evaluation)
# roi_zyx = np.transpose(roi.imageArray, (2, 1, 0))
# dose_reference=dose_reference0 * roi_zyx
# dose_evaluation = dose_evaluation0 * roi_zyx
(z_ref, y_ref, x_ref) = axes_reference
(z_eval, y_eval, x_eval) = axes_evaluation

gamma_options = {
    'dose_percent_threshold': 3,
    'distance_mm_threshold': 3,
    'lower_percent_dose_cutoff': 20,
    'interp_fraction': 10,  # Should be 10 or more for more accurate results
    'max_gamma': 2,
    'random_subset': None,
    'local_gamma': True,
    'ram_available': 2 ** 29  # 1/2 GB
}

gamma = pymedphys.gamma(
    axes_reference, dose_reference,
    axes_evaluation, dose_evaluation,
    **gamma_options)
valid_gamma = gamma[~np.isnan(gamma)]

num_bins = (
        gamma_options['interp_fraction'] * gamma_options['max_gamma'])
bins = np.linspace(0, gamma_options['max_gamma'], num_bins + 1)

plt.hist(valid_gamma, bins, density=True)
# if density is True, y value is probability density; otherwise, it is count in a bin
plt.xlim([0, gamma_options['max_gamma']])
plt.xlabel('gamma index')
plt.ylabel('probability density')

pass_ratio = np.sum(valid_gamma <= 1) / len(valid_gamma)

if gamma_options['local_gamma']:
    gamma_norm_condition = 'Local gamma'
else:
    gamma_norm_condition = 'Global gamma'

plt.title(
    f"Dose cut: {gamma_options['lower_percent_dose_cutoff']}% | {gamma_norm_condition} ({gamma_options['dose_percent_threshold']}%/{gamma_options['distance_mm_threshold']}mm) | Pass Rate(/u03B3<=1): {pass_ratio * 100:.2f}% /n ref pts: {len(z_ref) * len(y_ref) * len(x_ref)} | valid /u03B3 pts: {len(valid_gamma)}")
plt.show()
# plt.savefig('gamma_hist.png', dpi=300)
#
# max_ref_dose = np.max(dose_reference)
#
# lower_dose_cutoff = gamma_options['lower_percent_dose_cutoff'] / 100 * max_ref_dose
#
# relevant_slice = (
#     np.max(dose_reference, axis=(1, 2)) >
#     lower_dose_cutoff)
# slice_start = np.max([
#         np.where(relevant_slice)[0][0],
#         0])
# slice_end = np.min([
#         np.where(relevant_slice)[0][-1],
#         len(z_ref)])
# z_vals = z_ref[slice(slice_start, slice_end, 5)]
#
# eval_slices = [
#     dose_evaluation[np.where(z_i == z_eval)[0][0], :, :]
#     for z_i in z_vals
# ]
#
# ref_slices = [
#     dose_reference[np.where(z_i == z_ref)[0][0], :, :]
#     for z_i in z_vals
# ]
#
# gamma_slices = [
#     gamma[np.where(z_i == z_ref)[0][0], :, :]
#     for z_i in z_vals
# ]
#
# diffs = [
#     eval_slice - ref_slice
#     for eval_slice, ref_slice
#     in zip(eval_slices, ref_slices)
# ]
#
# max_diff = np.max(np.abs(diffs))
#
# for i, (eval_slice, ref_slice, diff, gamma_slice) in enumerate(zip(eval_slices, ref_slices, diffs, gamma_slices)):
#     fig, ax = plt.subplots(figsize=(13, 10), nrows=2, ncols=2)
#
#     fig.suptitle('Slice Z_{0}'.format(slice_start + i * 5), fontsize=12)
#     c00 = ax[0, 0].contourf(
#         x_eval, y_eval, eval_slice, 100,
#         vmin=0, vmax=max_ref_dose)
#     ax[0, 0].set_title("Evaluation")
#     fig.colorbar(c00, ax=ax[0, 0], label='Dose (Gy)')
#     ax[0, 0].invert_yaxis()
#     ax[0, 0].set_xlabel('x (mm)')
#     ax[0, 0].set_ylabel('y (mm)')
#
#     c01 = ax[0, 1].contourf(
#         x_ref, y_ref, ref_slice, 100,
#         vmin=0, vmax=max_ref_dose)
#     ax[0, 1].set_title("Reference")
#     fig.colorbar(c01, ax=ax[0, 1], label='Dose (Gy)')
#     ax[0, 1].invert_yaxis()
#     ax[0, 1].set_xlabel('x (mm)')
#     ax[0, 1].set_ylabel('y (mm)')
#
#     c10 = ax[1, 0].contourf(
#         x_ref, y_ref, diff, 100,
#         vmin=-max_diff, vmax=max_diff, cmap=plt.get_cmap('seismic'))
#     ax[1, 0].set_title("Dose difference")
#     cbar = fig.colorbar(c10, ax=ax[1, 0], label='[Dose Eval] - [Dose Ref] (Gy)')
#     cbar.formatter.set_powerlimits((0, 0))  # use scientific notation
#     ax[1, 0].invert_yaxis()
#     ax[1, 0].set_xlabel('x (mm)')
#     ax[1, 0].set_ylabel('y (mm)')
#
#     c11 = ax[1, 1].contourf(
#         x_ref, y_ref, gamma_slice, 100,
#         vmin=0, vmax=2, cmap=plt.get_cmap('coolwarm'))
#     ax[1, 1].set_title(
#         f"{gamma_norm_condition} ({gamma_options['dose_percent_threshold']} % / {gamma_options['distance_mm_threshold']} mm)")
#     fig.colorbar(c11, ax=ax[1, 1], label='gamma index')
#     ax[1, 1].invert_yaxis()
#     ax[1, 1].set_xlabel('x (mm)')
#     ax[1, 1].set_ylabel('y (mm)')
#
#     plt.show()
#     print("/n")
###############################################################     DVH PLOT      ########################################################################################
#Compute DVH on resampled contour
# from opentps.core.io.dicomIO import readDicomDose, writeRTDose
# doseImage1=readDicomDose("RD1.2.826.0.1.3680043.8.498.90979781075462906833195151434177594889.dcm")
# doseImage2=readDicomDose("RD1.2.826.0.1.3680043.8.498.12855534024498979538361437145251430617.dcm")
# dosediff=doseImage1.imageArray-doseImage2.imageArray
# target_DVH1 = DVH(roi, doseImage1)
# target_DVH2 = DVH(roi, doseImage2)
# OAR_DVH1=DVH(OAR_Rectum,doseImage1)
# OAR_DVH2=DVH(OAR_Rectum,doseImage2)
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
# img_dose2 = resampleImage3DOnImage3D(doseImage1, ct)
# img_dose2 = img_dose2.imageArray[:, :, Z_coord].transpose(1, 0)
#
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider
#
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider
#
#
# # Define a function to update the images when the slider value changes
# def update_slice(val):
#     Z_coord = int(slider.val)
#
#     # Update images based on the selected Z_coord slice
#     img_ct_slice = ct.imageArray[:, :, Z_coord].transpose(1, 0)
#     img_mask_slice = contourTargetMask.imageArray[:, :, Z_coord].transpose(1, 0)
#     img_dose1_slice = doseImage1.imageArray[:, :, Z_coord].transpose(1, 0)
#     img_dose2_slice = doseImage2.imageArray[:, :, Z_coord].transpose(1, 0)
#     dose_diff_slice = dosediff[:, :, Z_coord].transpose(1, 0)
#
#     # Update displayed data for each subplot
#     ct_img1.set_data(img_ct_slice)
#     mask_img1.set_data(img_mask_slice)
#     dose1_img.set_data(img_dose1_slice)
#
#     ct_img2.set_data(img_ct_slice)
#     mask_img2.set_data(img_mask_slice)
#     dose2_img.set_data(dose_diff_slice)
#
#     fig.canvas.draw_idle()
#
#
# # Initial plot setup
# fig, ax = plt.subplots(1, 3, figsize=(15, 5))
# fig.subplots_adjust(bottom=0.2)
#
# # Set up the initial display with Z_coord slice
# Z_coord = COM_index[2]
# img_ct_slice = ct.imageArray[:, :, Z_coord].transpose(1, 0)
# img_mask_slice = contourTargetMask.imageArray[:, :, Z_coord].transpose(1, 0)
# img_dose1_slice = doseImage1.imageArray[:, :, Z_coord].transpose(1, 0)
# img_dose2_slice = doseImage2.imageArray[:, :, Z_coord].transpose(1, 0)
# dose_diff_slice = dosediff[:, :, Z_coord].transpose(1, 0)
#
# # Display initial images for the first subplot
# ct_img1 = ax[0].imshow(img_ct_slice, cmap='gray')
# mask_img1 = ax[0].imshow(img_mask_slice, alpha=.6, cmap='binary')
# dose1_img = ax[0].imshow(img_dose1_slice, cmap='jet', alpha=.4)  # Set color range for dose1
# plt.colorbar(dose1_img, ax=ax[0])
# ax[0].set_title("Original")
#
# # Display initial images for the second subplot
# ct_img2 = ax[1].imshow(img_ct_slice, cmap='gray')
# mask_img2 = ax[1].imshow(img_mask_slice, alpha=.6, cmap='binary')
# dose2_img = ax[1].imshow(dose_diff_slice, cmap='seismic', alpha=.6, vmin=-20, vmax=20)  # Set color range for dose diff
# ax[1].set_xlim(300, 200)
# ax[1].set_ylim(300, 200)
# plt.colorbar(dose2_img, ax=ax[1])
# ax[1].set_title("Dose Diff")
#
# # Plot DVH in the third axis
# ax[2].plot(target_DVH1.histogram[0], target_DVH1.histogram[1], label="Original")
# ax[2].plot(target_DVH2.histogram[0], target_DVH2.histogram[1], label="DynamicDose")
# ax[2].plot(OAR_DVH1.histogram[0], OAR_DVH1.histogram[1], label="Original_OAR")
# ax[2].plot(OAR_DVH2.histogram[0], OAR_DVH2.histogram[1], label="DynamicDose_OAR")
# ax[2].set_xlabel("Dose (Gy)")
# ax[2].set_ylabel("Volume (%)")
# ax[2].grid(True)
# ax[2].legend()
#
# # Add slider for selecting Z-coordinate (slice index)
# ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor="lightgray")
# slider = Slider(ax_slider, 'Slice', 0, doseImage1.imageArray.shape[2] - 1, valinit=Z_coord, valstep=1)
#
# # Update function for the slider
# slider.on_changed(update_slice)
#
# plt.show()

