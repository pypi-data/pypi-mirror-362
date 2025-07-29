import copy

import numpy as np
from matplotlib import pyplot as plt
from opentps.core.processing.planDeliverySimulation.simpleBeamDeliveryTimings import SimpleBeamDeliveryTimings
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

output_path = os.path.dirname(__file__)
ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)

############################################### 0604 TG119 TEST ##############################################
ctCalibration = readScanner(DoseCalculationConfig().scannerFolder)
bdl = mcsquareIO.readBDL(DoseCalculationConfig().bdlFile)
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

target = rt_struct.getContourByName(target_name).getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
roi=target

OAR_Prostate = rt_struct.getContourByName("Prostate").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
OAR_bladder = rt_struct.getContourByName("Urinary bladder").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
OAR_Rectum = rt_struct.getContourByName("Rectum").getBinaryMask(origin=ct.origin,gridSize=ct.gridSize,spacing=ct.spacing)
#
COM_coord = target.centerOfMass
COM_index = target.getVoxelIndexFromPosition(COM_coord)
Z_COORD = COM_index[2]


###############################################################################################
#plan_path=output_path+"/"+"Arcplan_CSS_new_90GA_Opti.tps"  
plan_name = "Arcplan_CSS_new_90GA_Opti_SpotReduction-layer_redistribution.tps"  
plan_path=output_path+"/"+plan_name
plan = loadRTPlan(plan_path)
bdt = SimpleBeamDeliveryTimings(plan)
plan_with_timings = bdt.getPBSTimings(sort_spots="true")
timing=getattr(plan_with_timings,"spotTimings")
beamSWT=plan_with_timings.beamStartTime()
plt.plot(beamSWT,".",label="Beam Start Time",color="gray")
plt.xlabel("gantry angle(deg)")
plt.ylabel("beam(layer)switching time(s)")
plt.show()
#print(plan_with_timings._beams[0]._layers[0].__dict__)
###############################################################################################
# Irrtime=plan_with_timings._beams[0]._layers[0]._irradiationDuration
# Scantime=plan_with_timings._beams[0]._layers[0]._ScanningDuration
# totalTime=Irrtime+Scantime
# id=range(0,len(Irrtime))
# #plt.plot(id,Irrtime,".",label="Irradiation Time",color="gray")
# #plt.plot(id,Scantime,".",label="Scanning Time",color="black")
# plt.plot(id,totalTime,"-",label="Total Time",color="r")
# plt.xlabel("spot id")
# plt.ylabel("Time(s)")
# plt.legend()
# plt.show()



# ################################ All layers   ####################################################
# Irrtime_array=[]
# Scantime_array=[]
# Totaltime_array=[]
# from itertools import chain
# def homolist2array(lists):
#     # 使用itertools.chain.from_iterable来扁平化列表
#     from itertools import chain

#     flattened_list = list(chain.from_iterable(lists))

#     # 将扁平化的列表转换为NumPy数组
#     np_array = np.array(flattened_list)
#     return np_array
# for i in range(len(plan_with_timings._beams)):
#     Irrtime = plan_with_timings._beams[i]._layers[0]._irradiationDuration
#     Irrtime_array.append(Irrtime)
#     Scantime=plan_with_timings._beams[i]._layers[0]._ScanningDuration
#     Scantime_array.append(Scantime)
#     totalTime=Irrtime+Scantime
#     Totaltime_array.append(totalTime)

# Irr=homolist2array(Irrtime_array)
# id=range(0,len(Irr))
# Scan=homolist2array(Scantime_array)
# Totaltime=homolist2array(Totaltime_array)
# #plt.plot(id,Irr,".",label="Irradiation Time",color="gray")
# #plt.plot(id,Scan,".",label="Scanning Time",color="black")
# plt.plot(id,Totaltime,".",label="Total Time",color="r")
# plt.xlabel("spot id")
# plt.ylabel("Time(s)")
# plt.legend()
# plt.show()
# ################################################  plot  by layers     ################################################################
# # Irrtime_array=[]
# # Scantime_array=[]
# # Totaltime_array=[]
# #
# #
# # for i in range(len(plan_with_timings._beams)):
# #     Irrtime = plan_with_timings._beams[i]._layers[0]._irradiationDuration
# #     Irr_sum=np.sum(Irrtime)
# #     Irrtime_array.append(Irr_sum)
# #     Scantime=plan_with_timings._beams[i]._layers[0]._ScanningDuration
# #     Scan_sum=np.sum(Scantime)
# #     Scantime_array.append(Scan_sum)
# #     totalTime=Irrtime+Scantime
# #     totalTime_sum=np.sum(totalTime)
# #     Totaltime_array.append(totalTime_sum)
# # id=range(len(Irrtime_array))
# # plt.plot(id,Irrtime_array,".",label="Irradiation Time",color="gray")
# # plt.plot(id,Scantime_array,".",label="Scanning Time",color="black")
# # plt.plot(id,Totaltime_array,".",label="Total Time",color="r")
# # plt.xlabel("layer id")
# # plt.ylabel("Time(s)")
# # plt.legend()
# # plt.show()
# ############################################   Calculation of delta theta    ###########################################################################

# gantryspeed =1 ##deg/s
# degree=gantryspeed*np.cumsum(totalTime)
# # plt.plot(id,degree)
# # plt.xlabel("spot id")
# # plt.ylabel("degree")
# # plt.show()
# ################################################  plot  by layers     ################################################################
cumtotaltime=[]
for i in range(len(plan_with_timings._beams)):
    totaltime=plan_with_timings._beams[i]._layers[0]._irradiationDuration+plan_with_timings._beams[i]._layers[0]._ScanningDuration
    layer_totaltime_array=np.cumsum(totaltime)
    cumtotaltime.append(layer_totaltime_array)
#print(cumtotaltime)


def diff_from_median(arr):
    # 计算原数组的中位数
    median_value = np.median(arr)
    # 计算每个元素与中位数之差
    # 使用广播来确保median_value与arr的形状相匹配，从而可以直接进行减法操作
    diff_array = arr - median_value
    return diff_array

# ################################################       modify plan       ################################################
from opentps.core.data.plan._planIonBeam import PlanIonBeam
from opentps.core.data.plan._planIonLayer import PlanIonLayer
from opentps.core.data.plan._planIonSpot import PlanIonSpot
plan_with_diff_angle=copy.deepcopy(plan)
for beam in plan_with_diff_angle.beams:
    plan_with_diff_angle.removeBeam(beam)

for i in range(len(cumtotaltime)):
    diff_GA=diff_from_median(cumtotaltime[i]) * (2)### GA speed = 2 deg/s
    for index,item in enumerate(diff_GA): ### diff_GA should has same length with numspots of beam i
        newbeam=PlanIonBeam()
        newbeam.isocenterPosition=plan.beams[i].isocenterPosition
        newbeam.gantryAngle=item+plan.beams[i].gantryAngle ########GA has been modified
        newbeam.couchAngle=plan.beams[i].couchAngle
        newlayer=PlanIonLayer()
        newlayer.nominalEnergy=plan.beams[i].layers[0].nominalEnergy
        spotX=plan.beams[i].layers[0]._x[index]
        spotY = plan.beams[i].layers[0]._y[index]
        spotMU=plan.beams[i].layers[0]._mu[index]
        newlayer.appendSpot(spotX,spotY,spotMU)
        newbeam.appendLayer(newlayer)
        plan_with_diff_angle.appendBeam(newbeam)
    # if i>6 :
    #     break


print(len(plan_with_diff_angle.beams))
#saveRTPlan(plan_with_diff_angle,output_path+"/ELSA_plan_with_diff_angle_90GA_1GA_Speed.tps")
#saveRTPlan(plan_with_diff_angle,output_path+"/plan_with_diff_angle_90GA_0.5GA_Speed.tps")
saveRTPlan(plan_with_diff_angle,output_path+"/DynamicChecktemp.tps")
# ##########################################################################################
mc2 = MCsquareDoseCalculator()
mc2.beamModel = bdl
mc2.ctCalibration = ctCalibration

# MCsquare simulation
mc2.nbPrimaries = 1e7
# doseImage1 = mc2.computeDose(ct, plan)
doseImage2 = mc2.computeDose(ct, plan_with_diff_angle)
# #
# # # Compute DVH on resampled contour
# # target_DVH1 = DVH(roi, doseImage1)
# # target_DVH2 = DVH(roi, doseImage2)
# #
# # # center of mass
# # roi = resampleImage3DOnImage3D(roi, ct)
# # COM_coord = roi.centerOfMass
# # COM_index = roi.getVoxelIndexFromPosition(COM_coord)
# # Z_coord = COM_index[2]
# #
# # img_ct = ct.imageArray[:, :, Z_coord].transpose(1, 0)
# # contourTargetMask = roi.getBinaryContourMask()
# # img_mask = contourTargetMask.imageArray[:, :, Z_coord].transpose(1, 0)
# # img_dose1 = resampleImage3DOnImage3D(doseImage1, ct)
# # img_dose1 = img_dose1.imageArray[:, :, Z_coord].transpose(1, 0)
# # from opentps.core.io.dicomIO import writeRTPlan, writeDicomCT, writeRTDose, writeRTStruct
# # # Don't delete it
# # doseImage1.referencePlan = plan
# # doseImage1.referenceCT = ct
# # doseImage2.referencePlan = plan_with_diff_angle
# # doseImage2.referenceCT = ct
# # writeRTDose(doseImage1, output_path)
# # writeRTDose(doseImage2, output_path)
# #
# # #
# # fig, ax = plt.subplots(1, 2, figsize=(15, 5))
# # ax[0].axes.get_xaxis().set_visible(False)
# # ax[0].axes.get_yaxis().set_visible(False)
# # ax[0].imshow(img_ct, cmap='gray')
# # ax[0].imshow(img_mask, alpha=.2, cmap='binary')  # PTV
# # dose = ax[0].imshow(img_dose1, cmap='jet', alpha=.2)
# # plt.colorbar(dose, ax=ax[0])
# # ax[1].plot(target_DVH1.histogram[0], target_DVH1.histogram[1], label="target_DVH1")
# # ax[1].plot(target_DVH2.histogram[0], target_DVH2.histogram[1], label="target_DVH2")
# # ax[1].set_xlabel("Dose (Gy)")
# # ax[1].set_ylabel("Volume (%)")
# # ax[1].grid(True)
# # ax[1].legend()
# #
# # plt.show()