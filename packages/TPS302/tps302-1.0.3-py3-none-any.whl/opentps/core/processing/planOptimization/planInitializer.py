import logging
import math
import warnings
import numpy as np
from opentps.core.data.CTCalibrations._abstractCTCalibration import AbstractCTCalibration
from opentps.core.data.images._ctImage import CTImage
from opentps.core.data.images._roiMask import ROIMask
from opentps.core.data.plan._planIonLayer import PlanIonLayer
from opentps.core.data.plan._rtPlan import RTPlan
from opentps.core.processing.C_libraries.libRayTracing_wrapper import WET_raytracing,transport_spots_to_target, \
    transport_spots_inside_target,compute_position_from_range
from opentps.core.processing.rangeEnergy import energyToRange, rangeToEnergy
import csv
logger = logging.getLogger(__name__)


class BeamInitializer:
    def __init__(self):
        self.spotSpacing = 5.
        self.layerSpacing = 2.
        self.targetMargin = 0.
        self.beam = None

        self.calibration: AbstractCTCalibration = None


    def initializeBeam(self):
        xxx=[]
        parElist=[]
        # generate hexagonal spot grid around isocenter
        spotGrid = self._defineHexagSpotGridAroundIsocenter()
        numSpots = len(spotGrid["x"])
        # compute direction vector
        u, v, w = 1e-10, 1.0, 1e-10  # BEV to 3D coordinates
        [u, v, w] = self._rotateVector([u, v, w], math.radians(self.beam.gantryAngle), 'z')  # rotation for gantry angle
        [u, v, w] = self._rotateVector([u, v, w], math.radians(self.beam.couchAngle), 'y')  # rotation for couch angle

        # prepare raytracing: translate initial positions at the CT image border
        for s in range(numSpots):
            translation = np.array([1.0, 1.0, 1.0])
            translation[0] = (spotGrid["x"][s] - self.imgBordersX[int(u < 0)]) / u
            translation[1] = (spotGrid["y"][s] - self.imgBordersY[int(v < 0)]) / v
            translation[2] = (spotGrid["z"][s] - self.imgBordersZ[int(w < 0)]) / w
            translation = translation.min()
            spotGrid["x"][s] = spotGrid["x"][s] - translation * u
            spotGrid["y"][s] = spotGrid["y"][s] - translation * v
            spotGrid["z"][s] = spotGrid["z"][s] - translation * w

        # transport each spot until it reaches the target


        transport_spots_to_target(self.rspImage, self.targetMask, spotGrid, [u, v, w])

        # remove spots that didn't reach the target
        minWET = 9999999
        for s in range(numSpots - 1, -1, -1):
            if spotGrid["WET"][s] < 0:
                spotGrid["BEVx"].pop(s)
                spotGrid["BEVy"].pop(s)
                spotGrid["x"].pop(s)
                spotGrid["y"].pop(s)
                spotGrid["z"].pop(s)
                spotGrid["WET"].pop(s)
            else:
                if self.beam.rangeShifter and self.beam.rangeShifter.WET > 0.0: spotGrid["WET"][
                    s] += self.beam.rangeShifter.WET
                if spotGrid["WET"][s] < minWET: minWET = spotGrid["WET"][s]
                if self.layersToSpacingAlignment: minWET = round(minWET / self.layerSpacing) * self.layerSpacing

        # raytracing of remaining spots to define energy layers
        transport_spots_inside_target(self.rspImage, self.targetMask, spotGrid, [u, v, w], minWET, self.layerSpacing)
        #print("posX=",spotGrid["posX"])
        #print(len(spotGrid["posX"]))
        # print("posY=",spotGrid["posY"])
        # print(len(spotGrid["posY"]))
        # print("posZ=",spotGrid["posZ"])
        # print(len(spotGrid["posZ"]))
        # print("EnergyLayer=", spotGrid["EnergyLayers"])
        # print("lenE=",len(spotGrid["EnergyLayers"]))
        # print(len(spotGrid["x"]))
        # print("y=", spotGrid["y"])
        # print("z=", spotGrid["z"])
        # print("EnergyLayer=",spotGrid["EnergyLayers"])
        # print(len(spotGrid["EnergyLayers"]))
        # print("WET=", spotGrid["WET"])
        # process valid spots
        numSpots = len(spotGrid["x"])
        for s in range(numSpots):
            initNumLayers = len(spotGrid["EnergyLayers"][s])
            if initNumLayers == 0: continue

            # additional layers in proximal and distal directions:
            if self.proximalLayers > 0:
                minEnergy = min(spotGrid["EnergyLayers"][s])
                minWET = energyToRange(minEnergy) * 10
                for l in range(self.proximalLayers):
                    minWET -= self.layerSpacing
                    if minWET/10 < 1.0:
                        warnings.warn('Small proton ranges are used, accuracy of energy computation cannot be guaranteed.')

                    spotGrid["EnergyLayers"][s].append(rangeToEnergy(minWET / 10))
                    spotGrid["posX"][s].append(spotGrid["posX"][s][-1])
                    spotGrid["posY"][s].append(spotGrid["posY"][s][-1])
                    spotGrid["posZ"][s].append(spotGrid["posZ"][s][-1])
            if self.distalLayers > 0:
                maxEnergy = max(spotGrid["EnergyLayers"][s])
                maxWET = energyToRange(maxEnergy) * 10
                for l in range(self.distalLayers):
                    maxWET += self.layerSpacing
                    if minWET/10 < 1.0:
                        warnings.warn('Small proton ranges are used, accuracy of energy computation cannot be guaranteed.')
                    spotGrid["EnergyLayers"][s].append(rangeToEnergy(maxWET / 10))
                    spotGrid["posX"][s].append(spotGrid["posX"][s][-1])
                    spotGrid["posY"][s].append(spotGrid["posY"][s][-1])
                    spotGrid["posZ"][s].append(spotGrid["posZ"][s][-1])
            #generate plan structure
            global xid
            xid = 0
            for energy in spotGrid["EnergyLayers"][s]:
                if energy <=0:
                    continue

                layerFound = 0
                for layer in self.beam.layers:

                    if abs(layer.nominalEnergy - energy) < 0.05:
                        # add spot to existing layer
                        #print("1xid=",xid)
                        #print(spotGrid["posX"][s][xid])
                        layer.appendSpot_XYZ(spotGrid["BEVx"][s], spotGrid["BEVy"][s], 1.,spotGrid["posX"][s][xid],spotGrid["posY"][s][xid],spotGrid["posZ"][s][xid])
                        xid = xid + 1
                        #xxx.append([spotGrid["x"][s],spotGrid["y"][s],spotGrid["z"][s]])
                        #print("xxx=",xxx)
                        # parElist.append(energy)
                        layerFound = 1

                if layerFound == 0:
                    # add new layer
                    layer = PlanIonLayer(energy)
                    #print("0xid=", xid)
                    layer.appendSpot_XYZ(spotGrid["BEVx"][s], spotGrid["BEVy"][s], 1.,spotGrid["posX"][s][xid],spotGrid["posY"][s][xid],spotGrid["posZ"][s][xid])
                    xid = xid + 1
                    #xxx.append([spotGrid["x"][s], spotGrid["y"][s], spotGrid["z"][s]])
                    # parElist.append(energy)
                    if self.beam.rangeShifter and self.beam.rangeShifter.WET > 0.0:
                        layer.rangeShifterSettings.rangeShifterSetting = 'IN'
                        layer.rangeShifterSettings.isocenterToRangeShifterDistance = 300.0  # TODO: raytrace distance from iso to body contour and add safety margin
                        layer.rangeShifterSettings.rangeShifterWaterEquivalentThickness = self.beam.rangeShifter.WET
                    self.beam.appendLayer(layer)
        # 指定文件路径
        # print("EnergyLayer=",spotGrid["EnergyLayers"])
        # print(len(spotGrid["EnergyLayers"]))
        # print("posX=",spotGrid["posX"])
        # print(len(spotGrid["posX"]))

        arrx= np.concatenate([np.array(sublist) for sublist in spotGrid["posX"]])
        arry=np.concatenate([np.array(sublist) for sublist in spotGrid["posY"]])
        arrz=np.concatenate([np.array(sublist) for sublist in spotGrid["posZ"]])
        xyzarr=np.concatenate([arrx, arry, arrz])
        #print(xyzarr)

        # print("BeVx=",spotGrid["BEVx"])
        # print(len(spotGrid["BEVx"]))
        # print("BeVy=", spotGrid["BEVy"])
        # print("x=", spotGrid["x"])
        # print(len(spotGrid["x"]))
        # print("y=", spotGrid["y"])
        # print("z=", spotGrid["z"])

        # print(len(spotGrid["EnergyLayers"]))
        # print("WET=", spotGrid["WET"])

        # file_path = 'xyz.txt'
        # # 打开文件，使用 'a' 模式以追加写入数据
        # with open(file_path, 'a') as file:
        #     # 将整个数组转换为字符串，以逗号分隔，并在末尾添加换行符
        #     line = ','.join(map(str, xyzarr)) + '\n'
        #     # 写入数据
        #     file.write(line)

    def _defineHexagSpotGridAroundIsocenter(self):
        FOV = 400  # max field size on IBA P+ is 30x40 cm
        numSpotX = math.ceil(FOV / self.spotSpacing)
        numSpotY = math.ceil(FOV / (self.spotSpacing * math.cos(math.pi / 6)))

        spotGrid = {"BEVx": [], "BEVy": [], "x": [], "y": [], "z": [], "WET": [], "EnergyLayers": [],"posX":[],"posY":[],"posZ":[]}

        for i in range(numSpotX):
            for j in range(numSpotY):
                spot = {}

                # coordinates in Beam-eye-view
                spotGrid["BEVx"].append((i - round(numSpotX / 2) + (j % 2) * 0.5) * self.spotSpacing)
                spotGrid["BEVy"].append((j - round(numSpotY / 2)) * self.spotSpacing * math.cos(math.pi / 6))

                # 3D coordinates
                x, y, z = spotGrid["BEVx"][-1], 0, spotGrid["BEVy"][-1]

                # rotation for gantry angle (around Z axis)
                [x, y, z] = self._rotateVector([x, y, z], math.radians(self.beam.gantryAngle), 'z')

                # rotation for couch angle (around Y axis)
                [x, y, z] = self._rotateVector([x, y, z], math.radians(self.beam.couchAngle), 'y')

                # Dicom CT coordinates
                spotGrid["x"].append(x + self.beam.isocenterPosition[0])
                spotGrid["y"].append(y + self.beam.isocenterPosition[1])
                spotGrid["z"].append(z + self.beam.isocenterPosition[2])
        return spotGrid

    def _rotateVector(self, vec, angle, axis):
        if axis == 'x':
            x = vec[0]
            y = vec[1] * math.cos(angle) - vec[2] * math.sin(angle)
            z = vec[1] * math.sin(angle) + vec[2] * math.cos(angle)
        elif axis == 'y':
            x = vec[0] * math.cos(angle) + vec[2] * math.sin(angle)
            y = vec[1]
            z = -vec[0] * math.sin(angle) + vec[2] * math.cos(angle)
        elif axis == 'z':
            x = vec[0] * math.cos(angle) - vec[1] * math.sin(angle)
            y = vec[0] * math.sin(angle) + vec[1] * math.cos(angle)
            z = vec[2]

        return [x, y, z]


class PlanInitializer:
    def __init__(self):
        self.ctCalibration: AbstractCTCalibration = None
        self.ct: CTImage = None
        self.plan: RTPlan = None
        self.targetMask: ROIMask = None

        self._beamInitializer = BeamInitializer()

    def placeSpots(self, spotSpacing: float, layerSpacing: float, targetMargin: float = 0.,
                   layersToSpacingAlignment=False, proximalLayers=1, distalLayers=1):
        self._beamInitializer.calibration = self.ctCalibration
        self._beamInitializer.spotSpacing = spotSpacing
        self._beamInitializer.layerSpacing = layerSpacing
        self._beamInitializer.targetMargin = targetMargin
        self._beamInitializer.layersToSpacingAlignment = layersToSpacingAlignment
        self._beamInitializer.proximalLayers = proximalLayers
        self._beamInitializer.distalLayers = distalLayers

        from opentps.core.data.images._rspImage import RSPImage
        logger.info('Target is dilated using a margin of {} mm. This process might take some time.'.format(targetMargin))
        roiDilated = ROIMask.fromImage3D(self.targetMask, patient=None)
        roiDilated.dilateMask(radius=targetMargin)

        self._beamInitializer.targetMask = roiDilated

        rspImage = RSPImage.fromCT(self.ct, self.ctCalibration, energy=100.)
        rspImage.patient = None
        self._beamInitializer.rspImage = rspImage

        imgBordersX = [rspImage.origin[0], rspImage.origin[0] + rspImage.gridSize[0] * rspImage.spacing[0]]
        imgBordersY = [rspImage.origin[1], rspImage.origin[1] + rspImage.gridSize[1] * rspImage.spacing[1]]
        imgBordersZ = [rspImage.origin[2], rspImage.origin[2] + rspImage.gridSize[2] * rspImage.spacing[2]]

        self._beamInitializer.imgBordersX = imgBordersX
        self._beamInitializer.imgBordersY = imgBordersY
        self._beamInitializer.imgBordersZ = imgBordersZ

        for beam in self.plan:
            beam.removeLayer(beam.layers)

            self._beamInitializer.beam = beam
            self._beamInitializer.initializeBeam()
