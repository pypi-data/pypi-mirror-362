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
from opentps.core.processing.planOptimization.planOptimization_backup import IMPTPlanOptimizer
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
iso_pos=_dicomIsocenterToMCsquare(roi.centerOfMass, ct.origin, ct.spacing, ct.gridSize)
iso_roi=roi.centerOfMass
print(iso_pos)
print(iso_roi)

#
mc2 = MCsquareDoseCalculator()
mc2.beamModel = bdl
mc2.ctCalibration = ctCalibration
#######################################################      functions      ################################################################################################


def find_indexes_not_equal_to_value(arr, target_value):
    indexes = [index for index, value in enumerate(arr) if value != target_value]
    return indexes
def element_equals_any(arr, target_element):
    result = np.any(arr == target_element)
    return result

def drawlistE(plan):
    elistdraw=[]
    for i in range(len(getattr(plan, "_beams"))):
        elistdraw.append(getattr(plan._beams[i]._layers[0],"nominalEnergy"))
    plt.plot(gantryAngles,elistdraw,".--")
    plt.xlabel("gantry angle(deg)")
    plt.ylabel("Energy(MeV)")
    plt.show()
    return 0
def count_elements_below_threshold(arr, threshold_factor):
    threshold = threshold_factor * np.mean(arr)
    count = np.sum(arr < threshold)
    return count
def coverage_compute_dose(plan,roi): ####by dose calculation
    mc2 = MCsquareDoseCalculator()
    mc2.beamModel = bdl
    mc2.ctCalibration = ctCalibration
    mc2.nbPrimaries = 1e7
    doseImage = mc2.computeDose(ct, plan)
    roi = resampleImage3DOnImage3D(roi, ct)
    COM_coord = roi.centerOfMass
    COM_index = roi.getVoxelIndexFromPosition(COM_coord)
    Z_coord = COM_index[2]
    # Display dose
    img_dose = resampleImage3DOnImage3D(doseImage, ct)
    img_dose = img_dose.imageArray[:, :, Z_coord].transpose(1, 0)
    target_img = roi.imageArray * img_dose
    target_withoutzero =target_img[target_img != 0]  # array

    threshold_factor = 0.95
    count_below_threshold = count_elements_below_threshold(target_withoutzero, threshold_factor)
    print("count_below_threshold=",count_below_threshold)
    return count_below_threshold

# def convert_image_and_roi(image_array, scale_factor):
#     expansion_radius = 5
#     true_positions = np.where(image_array)
#
#     # 对image_array进行resize，实现按照指定的scale_factor转换
#     new_shape = tuple(int(dim * scale_factor[i]) for i, dim in enumerate(image_array.shape))
#     converted_image_array = np.resize(image_array, new_shape)
#
#     # 对roi_range进行resize，同样按照指定的scale_factor转换
#     converted_roi_range = np.zeros_like(converted_image_array, dtype=bool)
#     for i, pos in enumerate(zip(*true_positions)):
#         # 确保 scale_factor 长度与坐标维度一致
#         scale_factor_i = scale_factor[min(i, len(scale_factor) - 1)]
#         roi_slices = slice(int(np.min(pos) * scale_factor_i), int(np.max(pos) * scale_factor_i) + 1)
#         converted_roi_range[pos[0], pos[1], pos[2]] = True
#
#     # 遍历True的位置，将其周围扩展指定半径
#     for i, pos in enumerate(zip(*true_positions)):
#         if np.any(converted_roi_range[pos]):
#             # 生成扩展半径范围
#             x_range = slice(max(0, int(pos[0] * scale_factor[0]) - expansion_radius), min(converted_roi_range.shape[0], int(pos[0] * scale_factor[0]) + expansion_radius + 1))
#             y_range = slice(max(0, int(pos[1] * scale_factor[1]) - expansion_radius), min(converted_roi_range.shape[1], int(pos[1] * scale_factor[1]) + expansion_radius + 1))
#             z_range = slice(max(0, int(pos[2] * scale_factor[2]) - expansion_radius), min(converted_roi_range.shape[2], int(pos[2] * scale_factor[2]) + expansion_radius + 1))
#
#             # 扩展周围范围
#             converted_roi_range[x_range, y_range, z_range] = True
#
#     return converted_image_array, converted_roi_range
import scipy
def convert_image_and_roi(image_array, scale_factor):
    spacing=scale_factor
    # 目标spacing为1毫米
    new_spacing = np.array([1.0, 1.0, 1.0])

    # 计算缩放因子
    zoom_factors = spacing / new_spacing

    # 重采样
    resampled_image = scipy.ndimage.zoom(image_array, zoom_factors, order=0)

    # 定义结构元素的大小
    expand_mm = 3  # 扩展3毫米
    structure_radius = int(np.ceil(expand_mm))

    # 创建结构元素（球形）
    structure = np.zeros((2*structure_radius+1, 2*structure_radius+1, 2*structure_radius+1), dtype=bool)
    center = structure_radius

    for x in range(2*structure_radius+1):
        for y in range(2*structure_radius+1):
            for z in range(2*structure_radius+1):
                if np.sqrt((x-center)**2 + (y-center)**2 + (z-center)**2) <= structure_radius:
                    structure[x, y, z] = True

    # 进行膨胀操作
    expanded_image = scipy.ndimage.binary_dilation(resampled_image, structure=structure)
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # x, y, z = np.where(expanded_image)
    # ax.scatter(x, y, z, c='red', marker='x', label='Coverage Array')
    # plt.show()
    return expanded_image
def centertocorner(center):
    xshape,yshape,zshape=ct.origin
    corner_x=center[0]-xshape - ct.spacing[0]/2
    corner_y=center[1]-yshape - ct.spacing[1]/2
    corner_z=center[2]-zshape - ct.spacing[2]/2
    return corner_x,corner_y,corner_z

def calculate_coverage_rate(pos_all):
    expanded_image=convert_image_and_roi(roi.imageArray,ct.spacing)
    #expanded_image =roi.imageArray
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # x, y, z = np.where(expanded_image)
    # ax.scatter(x, y, z, c='red', marker='x', label='Coverage Array')
    # plt.show()
    # 获取 expanded_image 的大小
    x_max, y_max, z_max = expanded_image.shape
    # 定义覆盖范围的偏移量（+/- 2.5 mm）
    offsets = np.array([-2,-1, 0, 1,2])

    # 创建一个与 expanded_image 大小相同的布尔数组，用于记录被覆盖的靶区位置
    covered_image = np.zeros_like(expanded_image, dtype=bool)

    # 计算每个坐标点的覆盖范围
    for point in pos_all:
        # 将 point 转换为 NumPy 数组并加上 isocenter 值
        #point = np.array(point) + iso_pos - iso_roi
        point_tocenter=np.array(point)
        #point_corner=_dicomIsocenterToMCsquare(point_tocenter,ct.origin, ct.spacing, ct.gridSize)
        point_corner=centertocorner(point_tocenter)
        x, y, z = point_corner

        for dx in offsets:
            for dy in offsets:
                for dz in offsets:
                    # 计算覆盖点的坐标
                    x_new, y_new, z_new = int(round(x + dx)), int(round(y + dy)), int(round(z + dz))
                    # 检查是否在 expanded_image 范围内并且是靶区
                    if 0 <= x_new < x_max and 0 <= y_new < y_max and 0 <= z_new < z_max:
                        if expanded_image[x_new, y_new, z_new]:
                            covered_image[x_new, y_new, z_new] = True

    # 计算靶区总点数和覆盖点数
    total_target_points = np.sum(expanded_image)
    covered_target_points = np.sum(covered_image & expanded_image)

    # 计算覆盖率
    coverage_rate = covered_target_points / total_target_points if total_target_points > 0 else 0

    return coverage_rate,expanded_image,covered_image
def coverage_compute(pos_all):
    scale_factor=ct.spacing
    existing_region = roi.imageArray
    converted_image_array, converted_roi_range=convert_image_and_roi(existing_region, scale_factor)

    existing_region=converted_roi_range

    coverage_array = np.zeros_like(existing_region, dtype=bool)
    coverage_radius = 5

    # 遍历每个点
    for point in pos_all:
        ###############################   球形 #####################################################
        # 将点的坐标四舍五入到最近的整数，以确定在数组中的索引
        # index = tuple(np.round(point).astype(int))
        #
        # # 确定在数组中的覆盖范围（球形）
        # x, y, z = np.meshgrid(np.arange(existing_region.shape[0]), np.arange(existing_region.shape[1]), np.arange(existing_region.shape[2]))
        # distances = np.sqrt((x - index[0])**2 + (y - index[1])**2 + (z - index[2])**2)
        # coverage_array[distances <= coverage_radius] = True
        # 将点的坐标四舍五入到最近的整数，以确定在数组中的索引
        ############################################################################################
        index = tuple(np.round(point).astype(int))

        # 确定在数组中的覆盖范围
        slices = tuple(slice(max(0, i - coverage_radius), min(s, i + coverage_radius + 1))
                       for i, s in zip(index, existing_region.shape))

        # 标记覆盖范围内的区域为True
        coverage_array[slices] = True

    # 统计覆盖区域和总区域的数量，只统计existing_region中布尔值为 True 的部分
    covered_area = np.sum(coverage_array & existing_region)
    total_area = np.sum(existing_region)

    # 计算覆盖程度
    coverage_percentage = (covered_area / total_area) * 100 if total_area > 0 else -1
    return coverage_percentage,coverage_array
import random
def visualize_coverage(image_array, coverage_array, coverage_percentage):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x, y, z = np.where(image_array)
    ax.scatter(x, y, z, c='blue', marker='o', label='Image Array')

    x, y, z = np.where(coverage_array)
    ax.scatter(x, y, z, c='red', marker='x', label='Coverage Array')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ax.legend()
    plt.title(f'Coverage Percentage: {coverage_percentage:.2f}%')
    plt.show()

def visualize_coverage_3d(expanded_image, covered_image):
    # 提取靶区和未覆盖区域的坐标
    target_coords = np.column_stack(np.where(expanded_image))
    uncovered_coords = np.column_stack(np.where(expanded_image & ~covered_image))

    # 创建 3D 图形
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制靶区轮廓
    ax.scatter(target_coords[:, 0], target_coords[:, 1], target_coords[:, 2], c='r', label='Target Area', alpha=0.3)

    # 绘制未覆盖区域
    ax.scatter(uncovered_coords[:, 0], uncovered_coords[:, 1], uncovered_coords[:, 2], c='b', label='Uncovered Area', alpha=0.9)

    # 设置图例
    ax.legend()

    # 设置标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 显示图形
    plt.show()
from skimage.measure import marching_cubes
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
def visualize_contour(expanded_image, covered_image):
    # 使用 marching_cubes 提取靶区的外轮廓
    verts_target, faces_target, _, _ = marching_cubes(expanded_image, level=0.5)
    verts_uncovered, faces_uncovered, _, _ = marching_cubes(expanded_image & ~covered_image, level=0.5)

    # 创建 3D 图形
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制靶区的外轮廓
    mesh_target = Poly3DCollection(verts_target[faces_target], alpha=0.3, facecolor='red')
    ax.add_collection3d(mesh_target)

    # 绘制未覆盖区域的外轮廓
    mesh_uncovered = Poly3DCollection(verts_uncovered[faces_uncovered], alpha=0.9, facecolor='blue')
    ax.add_collection3d(mesh_uncovered)

    # 设置图例
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 设置坐标轴范围
    ax.set_xlim(0, expanded_image.shape[0])
    ax.set_ylim(0, expanded_image.shape[1])
    ax.set_zlim(0, expanded_image.shape[2])

    # 显示图形
    plt.show()

def is_sorted_descending(lst):
    # 检查列表是否为降序排列
    return all(lst[i] >= lst[i + 1] for i in range(len(lst) - 1))

def random_selection(matrix):
    iterN=0
    while True:
        # 随机选择每一列的一个数据
        iterN=iterN+1
        selected_data = [random.choice(column) for column in matrix]
        # 检查是否满足降序排列条件
        if is_sorted_descending(selected_data):
            break
        elif iterN > 10000:
            print("can't select layer properly, try to reset group number")
            break
    return selected_data
def split_into_groups(sequence, num_groups):
    # 计算每组的大小
    group_size = len(sequence) // num_groups

    # 将序列按组大小划分
    groups = [sequence[i:i+group_size] for i in range(0, (num_groups-1)*group_size, group_size)]

    # 最后一组包含剩余的元素
    groups.append(sequence[(num_groups-1)*group_size:])

    return groups
def group_selection(fullElist,num_groups):
    length=len(fullElist)
    col_id=np.arange(length)
    res=split_into_groups(col_id, num_groups)
    selected_full=[]
    for i in range(len(res)):
        col=res[i]
        list_for_select=[fullElist[j]for j in col]
        selected_list=random_selection(list_for_select)
        selected_full.append(selected_list)
    result = [item for sublist in selected_full for item in sublist]
    return result
# def layer_choose(plan):# randomly choose energy for each beam
#     full_elist = []
#     for a in range(72):
#         elist=[]
#         for i in range(len(getattr(plan._beams[a], "_layers"))):
#             elist.append(getattr(plan._beams[a]._layers[i], "nominalEnergy"))# read Elist
#         full_elist.append(elist)
#     elist_aft=group_selection(full_elist,10)
#     print(elist_aft)
#     for a in range(72):# beam loop
#         j = 0 #layer number
#         energy=elist_aft[a]
#         layerid = find_indexes_not_equal_to_value(np.array(elist_aft), energy)
#         for i in range(len(elist_aft)): # layer loop
#             if element_equals_any(np.array(layerid), i):
#                 plan._beams[a].removeLayer(plan._beams[a]._layers[j])
#                 #("a layer has been removed")
#             else:
#                 #print("layer skiped",i)
#                 j=j+1
#                 continue
#     return plan,elist_aft
def randomlylayerchoose(plan):
    plan_temp=copy.deepcopy(plan)
    full_elist = []
    choose_energy = []
    for a in range((len(getattr(plan_temp, "_beams")))):
        j=0
        elist= []
        for i in range(len(getattr(plan_temp._beams[a], "_layers"))):
            elist.append(getattr(plan_temp._beams[a]._layers[i], "nominalEnergy"))  # read Elist
        full_elist.append(elist)

        energy = np.random.choice(np.array(full_elist[a]))
        choose_energy.append(energy)
        #print("choosed energy:",energy)
        layerid = find_indexes_not_equal_to_value(elist, energy)
        for i in range(len(np.array(full_elist[a]))):
            if element_equals_any(np.array(layerid), i):
                plan_temp._beams[a].removeLayer(plan_temp._beams[a]._layers[j])
                #print("a layer has been removed")
            else:
                #print("layer skiped",i)
                j=j+1
                continue
    return plan_temp,choose_energy


import random


def choose_energy_layers(energy_layers):#require GantryAngle*Candidate layers List
    chosen_layers = []

    previous_energy = random.choice(energy_layers[0])  # 第1步：随机选择第一行的一个能量层
    chosen_layers.append(previous_energy)

    for direction in range(1, len(energy_layers)):
        # 第2步：为每个后续的方向选择一个能量层
        # 查找所有有效的能量层（小于或等于上一个能量层）
        valid_layers = [e for e in energy_layers[direction] if e <= previous_energy]

        if valid_layers:
            chosen_layer =max(valid_layers)
        else:
            # 如果没有找到有效层，则允许向上跳跃
            chosen_layer = random.choice(energy_layers[direction])

        chosen_layers.append(chosen_layer)
        previous_energy = chosen_layer

    return chosen_layers



def ELSA_choose_layers(plan):
    plan_temp=copy.deepcopy(plan)
    full_elist = []
    chosen_layers = []
    for a in range((len(getattr(plan_temp, "_beams")))):
        elist = []
        for i in range(len(getattr(plan_temp._beams[a], "_layers"))):
            elist.append(getattr(plan_temp._beams[a]._layers[i], "nominalEnergy"))  # read Elist
        full_elist.append(elist)
    chosen_layers=choose_energy_layers(full_elist)
    for a in range((len(getattr(plan_temp, "_beams")))):
        j=0
        energy=chosen_layers[a]
        elist=full_elist[a]
        layerid = find_indexes_not_equal_to_value(elist, energy)
        for i in range(len(np.array(full_elist[a]))):
            if element_equals_any(np.array(layerid), i):
                plan_temp._beams[a].removeLayer(plan_temp._beams[a]._layers[j])
                # ("a layer has been removed")
            else:
                # print("layer skiped",i)
                j = j + 1
                continue
    return plan_temp,full_elist,chosen_layers

def covobj(choosed_Elist_index):
    plan_temp=copy.deepcopy(plan)
    choosed_Elist = [candidate_layers[row_index][column_index] for row_index, column_index in enumerate(choosed_Elist_index)]
    for a in range((len(getattr(plan_temp, "_beams")))):
        j=0
        energy=choosed_Elist[a]
        elist=[]
        for i in range(len(getattr(plan_temp._beams[a], "_layers"))):
            elist.append(getattr(plan_temp._beams[a]._layers[i], "nominalEnergy"))  # read Elist
        layerid = find_indexes_not_equal_to_value(elist, energy)
        for i in range(len(np.array(elist))):
            if element_equals_any(np.array(layerid), i):
                plan_temp._beams[a].removeLayer(plan_temp._beams[a]._layers[j])
                #("a layer has been removed")
            else:
                #print("layer skiped",i)
                j=j+1
                continue
    pos_all = np.empty((0, 3))
    for i in range(len(gantryAngles)):
        for j in range(len(getattr(plan_temp._beams[i], "_layers"))):
            posperlayer = np.column_stack((getattr(plan_temp._beams[i]._layers[j], "_posX"),
                                           getattr(plan_temp._beams[i]._layers[j], "_posY"),
                                           getattr(plan_temp._beams[i]._layers[j], "_posZ")))
            pos_all = np.concatenate((pos_all, posperlayer), axis=0)
    cov,_,_=calculate_coverage_rate(pos_all)
    return cov
def ELSTcalc(Elist_index):
    Elist = [candidate_layers[row_index][column_index] for row_index, column_index in enumerate(Elist_index)]
    Elist=np.array(Elist)
    uptime=5.5
    downtime=0.6
    diff=np.diff(Elist)
    result=np.sum(diff > 0) *downtime + np.sum(diff < 0 ) * uptime
    return result
# 示例目标函数
def getfullElist(plan):
    full_elist=[]
    for a in range((len(getattr(plan, "_beams")))):
        j=0
        elist = []
        for i in range(len(getattr(plan._beams[a], "_layers"))):
            elist.append(getattr(plan._beams[a]._layers[i], "nominalEnergy"))  # read Elist
        full_elist.append(elist)

    return full_elist

def ELSTcalc_2(choosed_elist):
    Elist=np.array(choosed_elist)
    uptime=5.5
    downtime=0.6
    diff=np.diff(Elist)
    result=np.sum(diff > 0) * uptime + np.sum(diff < 0 ) * downtime
    return result

###########################################################    setting plan parameters   ##########################################################
gantryAngles = np.linspace(0, 360, 45)
couchAngles = np.zeros(45)
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
planDesign.spotSpacing = 5.0
planDesign.layerSpacing = 5.0
planDesign.targetMargin = 3.0

plan = planDesign.buildPlan()  # Spot placement
plan.PlanName = "NewPlan"
####################################################        test          ##########################################################################
for i in range(3):
    plan_selected,choosed_E=randomlylayerchoose(plan)
    print(choosed_E)
    print(ELSTcalc_2(choosed_E))
    #drawlistE(plan_selected)
    pos_all = np.empty((0, 3))
    for i in range(len(gantryAngles)):
        for j in range(len(getattr(plan_selected._beams[i], "_layers"))):
            posperlayer=np.column_stack((getattr(plan_selected._beams[i]._layers[j],"_posX"),getattr(plan_selected._beams[i]._layers[j],"_posY"),getattr(plan_selected._beams[i]._layers[j],"_posZ")))
            pos_all=np.concatenate((pos_all,posperlayer),axis=0)
    coverage_percentage,expanded_image,covered_image=calculate_coverage_rate(pos_all)
    print(coverage_percentage)
#print(plan._beams[0])
#plan_selected,choosed_E=randomlylayerchoose(plan)
# pos_all = np.empty((0, 3))
# for i in range(len(gantryAngles)):
#     for j in range(len(getattr(plan_selected._beams[i], "_layers"))):
#         posperlayer=np.column_stack((getattr(plan_selected._beams[i]._layers[j],"_posX"),getattr(plan_selected._beams[i]._layers[j],"_posY"),getattr(plan_selected._beams[i]._layers[j],"_posZ")))
#         pos_all=np.concatenate((pos_all,posperlayer),axis=0)
# print(pos_all)
# print(dir(plan_selected))
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# x, y, z = np.where(roi.imageArray)
# ax.scatter(x, y, z, c='red', marker='x', label='Coverage Array')
# plt.show()
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')#
# # 设置坐标轴标签
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# # 清空图形
# ax.clear()
#
# # 计算每个坐标点的覆盖范围
# for point in pos_all:
#     # 将 point 转换为 NumPy 数组并加上 isocenter 值
#     point = np.array(point) - iso_roi + iso_pos
#     x, y, z = point
#     ax.scatter(x, y, z)
# plt.show()
# ax = fig.add_subplot(111, projection='3d')#
# # 设置坐标轴标签
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# # 清空图形
# ax.clear()
# # 绘制散点图
# ax.scatter(pos_all[:, 0],pos_all[:, 1], pos_all[:, 2])
# # 设置坐标轴标签
# plt.show()
#
# #drawlistE(plan_selected)
# coverage_percentage,expanded_image,covered_image=calculate_coverage_rate(pos_all)
# print(coverage_percentage)
# #visualize_coverage(roi.imageArray,coverage_array,coverage_percentage)
# # # 可视化三维结果
# visualize_coverage_3d(expanded_image, covered_image)
# visualize_contour(expanded_image, covered_image)
# ########################################                 ELSA                 ######################################################################
# for a in range(10):
#     plan_selected,fullElist,choosed_E=ELSA_choose_layers(plan)
#     pos_all = np.empty((0, 3))
#     for i in range(len(gantryAngles)):
#         for j in range(len(getattr(plan_selected._beams[i], "_layers"))):
#             posperlayer=np.column_stack((getattr(plan_selected._beams[i]._layers[j],"_posX"),getattr(plan_selected._beams[i]._layers[j],"_posY"),getattr(plan_selected._beams[i]._layers[j],"_posZ")))
#             pos_all=np.concatenate((pos_all,posperlayer),axis=0)
#     coverage_percentage,expanded_image,covered_image=calculate_coverage_rate(pos_all)
#     print(coverage_percentage)
#     plt.scatter(a,coverage_percentage,color="r")
#     plt.xlabel("index")
#     plt.ylabel("coverage")
# plt.show()
    #visualize_coverage(roi.imageArray,coverage_array,coverage_percentage)
# #print(fullElist)
# #print(len(choosed_E))

# for i in range(len(gantryAngles)):
#     for j in range(len(fullElist[i])):
#         plt.scatter(gantryAngles[i],fullElist[i][j],marker="o",color='r',alpha=0.3,label="All candidate layers")
#
# plt.plot(gantryAngles, choosed_E, ".--",label="selected layers")
# plt.xlabel("gantry angle(deg)")
# plt.ylabel("Energy(MeV)")
# plt.show()

#coverage_percentage,coverage_array=coverage_compute(pos_all)
#print(coverage_percentage)
#visualize_coverage(roi.imageArray,coverage_array,coverage_percentage)
#########################################                  Geatpy                     #####################################################################
# import numpy as np
# import geatpy as ea
# num_angles = int(len(gantryAngles))
# candidate_layers = getfullElist(plan)
# def objective_function(x):
#     # x是每一行选择的索引，例如 [0, 1, 0, ...]
#     coverage=covobj(x)
#     time=ELSTcalc(x)
#     return [coverage, time]
# # 定义问题类
# class MyProblem(ea.Problem):
#     def __init__(self):
#         name = 'MyProblem'
#         M = 2  # 目标维数
#         lb = [0] * len(candidate_layers)  # 每行的最小索引
#         ub = [len(row) - 1 for row in candidate_layers]
#         Dim = num_angles  # 决策变量维数
#         maxormins = [-1,1]  # 目标最小化问题
#         varTypes = [1] * Dim  # 决策变量类型，1表示整数
#         lbin=[1] * Dim
#         ubin = [1] * Dim
#         self.M=M
#         ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
#     def aimFunc(self, pop):
#         # 目标函数
#         Vars = pop.Phen  # 决策变量矩阵
#         results = np.zeros((pop.sizes, self.M))
#         for i in range(pop.sizes):
#             results[i, :] = objective_function(Vars[i, :])
#         pop.ObjV = results
#
#     def calConstraint(self, pop):
#         # 计算约束条件
#         Vars = pop.Phen
#         coverage_values = []
#         for i in range(pop.sizes):
#             coverage, _ = objective_function(Vars[i, :])
#             coverage_values.append(coverage)
#         coverage_values = np.array(coverage_values)
#
#         # 添加约束条件，要求coverage大于70
#         pop.CV = coverage_values - 0.7
# # 创建问题实例
# my_problem = MyProblem()
# algorithm = ea.moea_NSGA3_templet(my_problem,
#                                   ea.Population(Encoding='RI', NIND=20),
#                                   MAXGEN=30,  # 最大进化代数
#                                   logTras=2)  # 表示每隔多少代记录一次日志信息，0表示不记录。
# res = ea.optimize(algorithm, seed=1, verbose=True, drawing=1, outputMsg=True, drawLog=True, saveFlag=True, dirName='Arcresult')
########################################                     DEAP                          #####################################################################
# import numpy as np
# import multiprocessing
# from deap import base, creator, tools, algorithms
# num_angles = int(len(gantryAngles))
# candidate_layers = getfullElist(plan)
# # 设置DEAP
# creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))  # 最小化coverage，最大化time
# creator.create("Individual", list, fitness=creator.FitnessMulti)
#
# toolbox = base.Toolbox()
#
# # 定义个体
# def create_individual():
#     return [np.random.randint(0, len(row)) for row in candidate_layers]
#
# toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#
# # 定义评估函数
# def evaluate(individual):
#     return objective_function(individual)
#
# toolbox.register("mate", tools.cxTwoPoint)
# toolbox.register("mutate", tools.mutUniformInt, low=[0]*len(candidate_layers), up=[len(row)-1 for row in candidate_layers], indpb=0.2)
# toolbox.register("select", tools.selNSGA2)
# toolbox.register("evaluate", evaluate)
#
# # 并行计算
# toolbox.register("map", multiprocessing.Pool().map)
#
# def main():
#     population = toolbox.population(n=50)
#     ngen = 50
#     cxpb = 0.7
#     mutpb = 0.2
#
#     # 使用NSGA-II算法
#     result_population, logbook = algorithms.eaMuPlusLambda(
#         population, toolbox, mu=50, lambda_=100, cxpb=cxpb, mutpb=mutpb,
#         ngen=ngen, stats=None, halloffame=None, verbose=True)
#
#     return result_population, logbook
#
# if __name__ == "__main__":
#     result_population, logbook = main()
#     # 打印结果
#     for ind in result_population:
#         print(ind, ind.fitness.values)
#########################################                  Dicom Plan  output         ######################################################################

# patient = Patient()
# patient.name = 'Patient'
# plan_selected.patient = patient
# output_path = os.getcwd()
#dcm_file = os.path.join(output_path, "Arcplan_Randomselected_WithoutOpti.dcm")
#writeRTPlan(plan_selected, dcm_file)
#########################################                 Beamlet Calculate                             ############################################################################
# Configure MCsquare
# mc2 = MCsquareDoseCalculator()
# mc2.beamModel = bdl
# mc2.nbPrimaries = 5e4
# mc2.ctCalibration = ctCalibration
# beamlets = mc2.computeBeamlets(ct, plan_selected, roi=[roi])
# plan_selected.planDesign.beamlets = beamlets
#
#
#
# #########################################                  Plan Opti  patient0                                   ###############################################################
# # plan_selected.planDesign.objectives = ObjectivesList()
# # plan_selected.planDesign.objectives.setTarget(roi.name, 60.0)
# # plan_selected.planDesign.objectives.fidObjList = []
# # plan_selected.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMAX, 61.0, 1.0)
# # plan_selected.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMIN, 58.5, 1.0)
# # solver = IMPTPlanOptimizer(method='Scipy-LBFGS', plan=plan_selected, maxit=1000)
# # # Optimize treatment plan
# # w, doseImage, ps = solver.optimize()
# #########################################                  Plan Opti  TG119 prostate                                  ###############################################################
# plan_selected.planDesign.objectives = ObjectivesList()
# plan_selected.planDesign.objectives.setTarget(roi.name, 80.0)
# plan_selected.planDesign.objectives.fidObjList = []
# plan_selected.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMAX, 83.0, 100.0)
# plan_selected.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMIN, 75.6, 100.0)
# plan_selected.planDesign.objectives.addFidObjective(OAR_Rectum, FidObjective.Metrics.DMAX, 77.0, 50.0)
# plan_selected.planDesign.objectives.addFidObjective(OAR_bladder, FidObjective.Metrics.DMAX, 75.0, 10.0)
# solver = IMPTPlanOptimizer(method='Scipy-LBFGS', plan=plan_selected, maxit=300)
# # Optimize treatment plan
# w, doseImage, ps = solver.optimize()
# ########################################                DVH and Dose display                          ##################################################################
# #MCsquare simulation
# mc2.nbPrimaries = 1e7
# doseImage = mc2.computeDose(ct, plan_selected)
# # Compute DVH on resampled contour
# target_DVH = DVH(roi, doseImage)
# rectum_DVH = DVH(OAR_Rectum,doseImage)
# bladder_DVH = DVH(OAR_bladder,doseImage)
#
# print('D5 - D95 =  {} Gy'.format(target_DVH.D5 - target_DVH.D95))
# clinROI = [roi.name, roi.name]
# clinMetric = ["Dmin", "Dmax"]
# clinLimit = [75.6, 83]
# clinObj = {'ROI': clinROI, 'Metric': clinMetric, 'Limit': clinLimit}
# print('Clinical evaluation')
# evaluateClinical(doseImage, [roi], clinObj)
#
# print("OAR_Rectum D30 : ",rectum_DVH.D30)
# print("OAR_Rectum D10 : ",rectum_DVH.D10)
# print("OAR_Bladder D30 : ",bladder_DVH.D30)
# print("OAR_Bladder D10 : ",bladder_DVH.D10)
# evaluateClinical(doseImage, [OAR_bladder], clinObj)
# # center of mass
# roi = resampleImage3DOnImage3D(roi, ct)
# COM_coord = roi.centerOfMass
# COM_index = roi.getVoxelIndexFromPosition(COM_coord)
# Z_coord = COM_index[2]
#
# img_ct = ct.imageArray[:, :, Z_coord].transpose(1, 0)
# contourTargetMask = roi.getBinaryContourMask()
# img_mask = contourTargetMask.imageArray[:, :, Z_coord].transpose(1, 0)
# img_dose = resampleImage3DOnImage3D(doseImage, ct)
# img_dose = img_dose.imageArray[:, :, Z_coord].transpose(1, 0)
# image_rectum_axial = OAR_Rectum.imageArray[:,:,Z_COORD].transpose(1,0)
# image_bladder_axial = OAR_bladder.imageArray[:,:,Z_COORD].transpose(1,0)
# # Display dose
# fig, ax = plt.subplots(1, 3, figsize=(15, 5))
# ax[0].axes.get_xaxis().set_visible(False)
# ax[0].axes.get_yaxis().set_visible(False)
# ax[0].imshow(img_ct, cmap='gray')
# ax[0].imshow(img_mask, alpha=.2, cmap='binary')  # PTV
# ax[0].contour(image_rectum_axial,colors="red",alpha=.2)
# ax[0].contour(image_bladder_axial,colors="green")
# dose = ax[0].imshow(img_dose, cmap='jet', alpha=.2)
# plt.colorbar(dose, ax=ax[0])
# ax[1].plot(target_DVH.histogram[0], target_DVH.histogram[1], label=target_DVH.name)
# ax[1].plot(rectum_DVH.histogram[0], rectum_DVH.histogram[1], label=rectum_DVH.name)
# ax[1].plot(bladder_DVH.histogram[0], bladder_DVH.histogram[1], label=bladder_DVH.name)
# ax[1].set_xlabel("Dose (Gy)")
# ax[1].set_ylabel("Volume (%)")
# ax[1].grid(True)
# ax[1].legend()
#
# convData = solver.getConvergenceData()
# ax[2].plot(np.arange(0, convData['time'], convData['time'] / convData['nIter']), convData['func_0'], 'bo-', lw=2,
#            label='Fidelity')
# ax[2].set_xlabel('Time (s)')
# ax[2].set_ylabel('Cost')
# ax[2].set_yscale('symlog')
# ax2 = ax[2].twiny()
# ax2.set_xlabel('Iterations')
# ax2.set_xlim(0, convData['nIter'])
# ax[2].grid(True)
#
# plt.show()

