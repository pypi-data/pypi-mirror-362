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
ring=target.createMaskRings(1,10)
ring10=ring[0]
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

# def calculate_coverage_rate(pos_all):
#     expanded_image=convert_image_and_roi(roi.imageArray,ct.spacing)
#     radius=3
#     # 获取 expanded_image 的大小
#     x_max, y_max, z_max = expanded_image.shape
#
#     # 创建一个与 expanded_image 大小相同的布尔数组，用于记录被覆盖的靶区位置
#     covered_image = np.zeros_like(expanded_image, dtype=bool)
#
#     # 计算每个坐标点的覆盖范围
#     for point in pos_all:
#         # 将 point 转换为 NumPy 数组并加上 isocenter 值 进行坐标变换
#         #point = np.array(point) + iso_pos - iso_roi
#         point_tocenter=np.array(point)
#         #point_corner=_dicomIsocenterToMCsquare(point_tocenter,ct.origin, ct.spacing, ct.gridSize)
#         point_corner=centertocorner(point_tocenter)
#         x, y, z = point_corner
#         x_min = int(x - radius)
#         x_max = int(x + radius)
#         y_min = int(y - radius)
#         y_max = int(y + radius)
#         z_min = int(z - radius)
#         z_max = int(z + radius)
#
#         covered_image[x_min:x_max + 1, y_min:y_max + 1, z_min:z_max + 1] = True
#
#     # 计算靶区总点数和覆盖点数
#     total_target_points = np.sum(expanded_image)
#     covered_target_points = np.sum(covered_image & expanded_image)
#
#     # 计算覆盖率
#     coverage_rate = covered_target_points / total_target_points if total_target_points > 0 else 0
#
#     return coverage_rate,expanded_image,covered_image
import random


def calculate_coverage_rate(pos_all):
    # 假设 expanded_image 已经被传入，或者你可以在这里重新计算它
    expanded_image = convert_image_and_roi(roi.imageArray, ct.spacing)
    radius = 3

    # 创建一个与 expanded_image 大小相同的整数数组，用于记录每个位置被覆盖的次数
    coverage_counts = np.zeros_like(expanded_image, dtype=int)

    # 创建一个与 expanded_image 大小相同的布尔数组，用于记录是否至少被覆盖一次
    covered_image = np.zeros_like(expanded_image, dtype=bool)

    # 计算每个坐标点的覆盖范围
    for point in pos_all:
        # 假设 point_corner 是将点从某种坐标系转换到 expanded_image 坐标系的函数
        point_corner = centertocorner(np.array(point))  # 这里假设 centertocorner 已经定义
        x, y, z = point_corner

        x_min = int(x - radius)
        x_max = int(x + radius)
        y_min = int(y - radius)
        y_max = int(y + radius)
        z_min = int(z - radius)
        z_max = int(z + radius)

        # 更新 coverage_counts 和 covered_image
        slice_mask = (
            slice(x_min, x_max + 1),
            slice(y_min, y_max + 1),
            slice(z_min, z_max + 1)
        )
        coverage_counts[slice_mask] += 1
        covered_image[slice_mask] = True

        # 计算靶区总点数（这里假设 expanded_image 是二值化的靶区图像）
    total_target_points = np.sum(expanded_image)

    # 计算被覆盖的靶区点数（即 covered_image 中为 True 的点数）
    # 注意：这里其实不需要再计算，因为 total_covered_points 等于 np.sum(covered_image)
    # 但为了与原始逻辑保持一致，我们仍然可以这样做
    total_covered_points = np.sum(covered_image & expanded_image)  # 这其实等于 np.sum(covered_image)

    # 计算覆盖率（这里仍然使用，但注意它可能不是最准确的，因为 total_target_points 可能不是所有点的总数）
    coverage_rate = total_covered_points / total_target_points if total_target_points > 0 else 0

    return coverage_rate, expanded_image, covered_image, coverage_counts
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
    ax.set_box_aspect([expanded_image.shape[0], expanded_image.shape[1], expanded_image.shape[2]])
    # 显示图形
    plt.show()

from skimage import measure
def visualize_contour_2D(expanded_image, covered_image, slice_z):
    # 提取相应Z层的布尔数组
    expanded_slice = expanded_image[:, :, slice_z]
    covered_slice = covered_image[:, :, slice_z]
    X=expanded_image.shape[0]
    Y = expanded_image.shape[1]
    # 创建一个新的数组来表示不同的覆盖状态
    combined_image = np.zeros((X, Y, 3))  # 用于存储RGB值

    # 设置不同覆盖状态的颜色
    combined_image[(expanded_slice & covered_slice)] = [1, 0, 0]  # 红色
    combined_image[(expanded_slice & ~covered_slice)] = [0, 1, 0]  # 绿色
    combined_image[(~expanded_slice & covered_slice)] = [0, 0, 1]  # 蓝色
    combined_image[(~expanded_slice & ~covered_slice)] = [1, 1, 1]  # 白色

    # 绘制合并的图像
    plt.figure(figsize=(6, 6))
    plt.title('Combined Coverage at Z={}'.format(slice_z))
    plt.imshow(combined_image, origin='lower')
    #plt.xlim(np.min(expanded_image[0])-30,np.max(expanded_image[0])+30)
    #plt.ylim(np.min(expanded_image[1])-30, np.max(expanded_image[1])+30)
    # 显示图形
    plt.show()

def visualize_contour_2D_count(expanded_image, covered_image, slice_z):
    # 提取相应Z层的布尔数组
    expanded_slice = expanded_image[:, :, slice_z]
    covered_slice = covered_image[:, :, slice_z]
    X=expanded_image.shape[0]
    Y = expanded_image.shape[1]
    # 创建一个新的数组来表示不同的覆盖状态
    combined_image = np.zeros((X, Y, 3))  # 用于存储RGB值

    # 设置不同覆盖状态的颜色
    combined_image[(expanded_slice & covered_slice)] = [1, 0, 0]  # 红色
    combined_image[(expanded_slice & ~covered_slice)] = [0, 1, 0]  # 绿色
    combined_image[(~expanded_slice & covered_slice)] = [0, 0, 1]  # 蓝色
    combined_image[(~expanded_slice & ~covered_slice)] = [1, 1, 1]  # 白色

    # 绘制合并的图像
    plt.figure(figsize=(6, 6))
    plt.title('Combined Coverage at Z={}'.format(slice_z))
    plt.imshow(combined_image, origin='lower')
    #plt.xlim(np.min(expanded_image[0])-30,np.max(expanded_image[0])+30)
    #plt.ylim(np.min(expanded_image[1])-30, np.max(expanded_image[1])+30)
    # 显示图形
    plt.show()

def get_surrounding_elements(index, max_index):
    # 定义左右边界，确保不会越界
    min_index = max(0, index - 3)
    max_index_to_include = min(max_index, index + 3)

    # 使用列表推导式生成数组
    return [i for i in range(min_index, max_index_to_include + 1)]
def choose_energy_layers_with_descending(energy_layers):
    """
    层选择函数，加入降序规则和中间层优先。
    - 如果有比上一射束小的层，从这些层中选择最大的。
    - 如果没有比上一射束小的层，则从中间层和最大层之间随机选择一个。
    """
    chosen_layers = []
    previous_layer = None  # 用于记录上一射束的选择
    
    for direction in range(len(energy_layers)):
        max_Eindex = len(energy_layers[direction])
        mid_layer_index = max_Eindex // 2  # 中间层索引
        
        # 获取中间附近的有效层索引
        valid_layers_index = get_surrounding_elements(mid_layer_index, max_Eindex)
        
        # 如果有前一射束的选择，筛选比前一射束小或相等的层
        smaller_layers_index = []
        if previous_layer is not None:
            smaller_layers_index = [i for i in valid_layers_index if energy_layers[direction][i] <= previous_layer]
        
        if smaller_layers_index:
            # 有比之前小的层，选择其中最大的
            chosen_layer_index = max(smaller_layers_index, key=lambda i: energy_layers[direction][i])
        else:
            # 没有比之前小的层，在中间层和最大层之间随机选择
            chosen_layer_index = np.random.choice(range(mid_layer_index, mid_layer_index+3))
        
        chosen_layer = energy_layers[direction][chosen_layer_index]
        chosen_layers.append(chosen_layer)
        
        # 更新上一射束的选择
        previous_layer = chosen_layer
    
    return chosen_layers

def CSS_choose_layers(plan):
    plan_temp=copy.deepcopy(plan)
    full_elist = []
    for a in range((len(getattr(plan_temp, "_beams")))):
        elist = []
        for i in range(len(getattr(plan_temp._beams[a], "_layers"))):
            elist.append(getattr(plan_temp._beams[a]._layers[i], "nominalEnergy"))  # read Elist
        full_elist.append(elist)
    chosen_layers=choose_energy_layers_with_descending(full_elist)
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


def getfullElist(plan):
    full_elist=[]
    for a in range((len(getattr(plan, "_beams")))):
        j=0
        elist = []
        for i in range(len(getattr(plan._beams[a], "_layers"))):
            elist.append(getattr(plan._beams[a]._layers[i], "nominalEnergy"))  # read Elist
        full_elist.append(elist)
    return full_elist
def ELSTcalc(choosed_elist):
    Elist=np.array(choosed_elist)
    uptime=5.5
    downtime=0.6
    diff=np.diff(Elist)
    result=np.sum(diff > 0) *uptime + np.sum(diff < 0 ) * downtime
    return result

# 更新plan_selected中的点
def update_plan_with_indices(plan, selected_indices):
    plan_temp=copy.deepcopy(plan)
    """
    根据聚类结果的索引更新plan_selected，将未选择的点的_mu设置为0。
    """
    current_index = 0  # 全局索引
    for i in range(len(plan_temp.planDesign.gantryAngles)):
        for j in range(len(getattr(plan_temp._beams[i], "_layers"))):
            # 获取当前层的点数
            layer = getattr(plan_temp._beams[i]._layers[j], "_posX").shape[0]

            # 当前层的全局索引范围
            layer_indices = list(range(current_index, current_index + layer))
            current_index += layer

            # 找出当前层中被选中的点
            selected_in_layer = [idx for idx in selected_indices if idx in layer_indices]
            local_selected_indices = [idx - layer_indices[0] for idx in selected_in_layer]

            # 更新_x, _y 和 _mu
            _x = getattr(plan_temp._beams[i]._layers[j], "_x")
            _y = getattr(plan_temp._beams[i]._layers[j], "_y")
            _mu = getattr(plan_temp._beams[i]._layers[j], "_mu")

            # 将未选择的点的_mu设置为0
            for k in range(layer):
                if k not in local_selected_indices:
                    _mu[k] = 0

            # 更新plan中对应的属性
            setattr(plan_temp._beams[i]._layers[j], "_mu", _mu)

    return plan_temp

import numpy as np
from sklearn.cluster import DBSCAN


# 使用DBSCAN减少点
def reduce_points_with_dbscan(points, eps=3, min_samples=1):
    """
    使用DBSCAN对点进行聚类，返回每个聚类的索引。
    """
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    labels = db.labels_

    selected_indices = []  # 存储每个聚类的代表点索引
    for label in np.unique(labels):
        if label != -1:  # 忽略噪声点
            cluster_indices = np.where(labels == label)[0]
            selected_indices.append(cluster_indices[0])  # 选择每个簇的第一个点（或其他策略）
    return selected_indices


###########################################################    setting plan parameters   ##########################################################
gantryAngles = np.linspace(0, 360, 90)
couchAngles = np.zeros(90)
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

# ########################################                 CSS                ######################################################################
start_time = time.time()

best_plan_selected = None
ELStime_array=[]
plan_selected,fullElist,choosed_E=CSS_choose_layers(plan)
ELST=ELSTcalc(choosed_E)
print("time=",ELST)
ELStime_array.append(ELST)
pos_all = np.empty((0, 3))
for i in range(len(gantryAngles)):
    for j in range(len(getattr(plan_selected._beams[i], "_layers"))):
        posperlayer=np.column_stack((getattr(plan_selected._beams[i]._layers[j],"_posX"),getattr(plan_selected._beams[i]._layers[j],"_posY"),getattr(plan_selected._beams[i]._layers[j],"_posZ")))
        pos_all=np.concatenate((pos_all,posperlayer),axis=0)
# 对pos_all应用减少策略，获取需要保留的点索引
print(pos_all.shape)
selected_indices = reduce_points_with_dbscan(pos_all, eps=1, min_samples=1)

plan_selected_reduced = update_plan_with_indices(plan_selected, selected_indices)
plan_selected_reduced.simplify()# remove zero mu spots
pos_all_reduced = np.empty((0, 3))
for i in range(len(plan_selected_reduced.beams)):
    for j in range(len(getattr(plan_selected_reduced._beams[i], "_layers"))):
        posperlayer=np.column_stack((getattr(plan_selected_reduced._beams[i]._layers[j],"_posX"),getattr(plan_selected_reduced._beams[i]._layers[j],"_posY"),getattr(plan_selected_reduced._beams[i]._layers[j],"_posZ")))
        pos_all_reduced=np.concatenate((pos_all_reduced,posperlayer),axis=0)
coverage_percentage,expanded_image,covered_image,covered_count=calculate_coverage_rate(pos_all_reduced)
# 计算并打印运行时间
end_time = time.time()
execution_time = end_time - start_time
print(f"代码执行时间: {execution_time}秒")
#visualize_contour(expanded_image,covered_image)
COM_index = roi.getVoxelIndexFromPosition(COM_coord)
Z_coord = int(COM_index[2]/ct.gridSize[2]*expanded_image.shape[2])
#visualize_contour_2D(expanded_image,covered_image, slice_z=Z_coord)
for i in range(len(gantryAngles)):
    for j in range(len(fullElist[i])):
        plt.scatter(gantryAngles[i],fullElist[i][j],marker="o",color='gray',alpha=0.3,label="All candidate layers")
        plt.plot(gantryAngles, choosed_E, ".--",color='salmon', label="selected layers")
plt.xlabel("gantry angle(deg)")
plt.ylabel("Energy(MeV)")
plt.show()
best_plan_selected=copy.deepcopy(plan_selected_reduced)

# plt.plot(gantryAngles, choosed_E, ".--",label="selected layers")
# plt.xlabel("gantry angle(deg)")
# plt.ylabel("Energy(MeV)")
# plt.show()

print(coverage_percentage)
print(pos_all_reduced.shape)
# # ########################################                 Beamlet Calculate                             ############################################################################
#Configure MCsquare
mc2 = MCsquareDoseCalculator()
mc2.beamModel = bdl
mc2.nbPrimaries = 5e4
mc2.ctCalibration = ctCalibration
beamlets = mc2.computeBeamlets(ct, best_plan_selected)
#beamlets=loadBeamlets("CSS_new_90GA_blm_spotreduction-layer_redistribution.blm")
best_plan_selected.planDesign.beamlets = beamlets
saveBeamlets(beamlets,"CSS_new_90GA_blm_spotreduction-layer_redistribution.blm")

#########################################                    Plan Opti  TG119 prostate                                  ###############################################################
best_plan_selected.planDesign.objectives = ObjectivesList()
best_plan_selected.planDesign.objectives.setTarget(roi.name,roi, 80.0)
best_plan_selected.planDesign.objectives.fidObjList = []
best_plan_selected.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DVHMAX, 82.5, 100.0,volume=5)
best_plan_selected.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DVHMIN, 75.6, 100.0,volume=95)
best_plan_selected.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DUNIFORM, 80.0, 200.0)
#best_plan_selected.planDesign.objectives.addFidObjective(roi, FidObjective.Metrics.DMIN, 76.0, 100.0)
best_plan_selected.planDesign.objectives.addFidObjective(ring10, FidObjective.Metrics.DVHMAX, 84.0, 100.0,volume=5)
best_plan_selected.planDesign.objectives.addFidObjective(OAR_Rectum, FidObjective.Metrics.DVHMAX, 75.0, 50.0,volume=10)
best_plan_selected.planDesign.objectives.addFidObjective(OAR_Rectum, FidObjective.Metrics.DVHMAX, 75.0, 50.0,volume=10)
best_plan_selected.planDesign.objectives.addFidObjective(OAR_bladder, FidObjective.Metrics.DVHMAX, 70.0, 10.0,volume=30)
best_plan_selected.planDesign.objectives.addFidObjective(OAR_bladder, FidObjective.Metrics.DVHMAX, 70.0, 10.0,volume=30)
solver = IMPTPlanOptimizer(method='Scipy_L-BFGS-B', plan=best_plan_selected, maxiter=100)
# Optimize treatment plan
w, doseImage, ps = solver.optimize()

#########################################                    Dicom Plan  output         ######################################################################

patient = Patient()
patient.name = 'Patient'
best_plan_selected.patient = patient
output_path = os.path.dirname(__file__)
#dcm_file = os.path.join(output_path, "Arcplan_CSS_new_90GA_Opti.dcm")
#tps_file = os.path.join(output_path, "Arcplan_CSS_new_90GA_Opti_SpotReduction-layer_redistribution.tps")
#writeRTPlan(best_plan_selected, dcm_file)
#saveRTPlan(best_plan_selected, tps_file)
########################################                DVH and Dose display                          ##################################################################
#MCsquare simulation
mc2.nbPrimaries = 1e7
doseImage = mc2.computeDose(ct, best_plan_selected)
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
#
