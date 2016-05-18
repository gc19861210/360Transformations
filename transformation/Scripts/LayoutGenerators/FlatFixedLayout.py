from .Layout import Layout
from .QEC import QEC
import random
import numpy as np
import math

class FlatFixedLayout(Layout):
    def __init__(self, layoutName, width, height, horizontalAngle, ypr):
        super().__init__(layoutName)
        self.yaw = ypr[0]
        self.pitch = ypr[1]
        self.roll = ypr[2]
        self.width = width
        self.height = height
        self.horizontalAngle = horizontalAngle

    def GenerateLayout(self, mediumRatio):
        c = '[{}]\ntype=flatFixed\n'.format(self.GetName())
        c += 'relativeResolution=false\n'

        c+='yaw={}\npitch={}\nroll={}\n'.format(self.yaw, self.pitch, self.roll)
        c += 'width={}\n'.format(self.width)
        c += 'height={}\n'.format(self.height)
        c += 'horizontalAngleOfVision={}\n'.format(self.horizontalAngle)
        return c

    wasRandomInit = False
    @classmethod
    def GetRandomCenter(cls):
        if not cls.wasRandomInit:
            cls.wasRandomInit = True
            random.seed(1)
        return (random.uniform(-180,180), random.uniform(-90,90))

    @classmethod
    def GetRandomCenterAtDistance(cls, qec, dist):
        '''Return a random point (theta, phi) at the distance dist from the given qec'''
        if not cls.wasRandomInit:
            cls.wasRandomInit = True
            random.seed(1)
        theta = math.radians(random.uniform(-90,90))
        c = np.matrix('{};{};{}'.format(math.sin(dist)*math.cos(theta), math.sin(dist)*math.sin(theta), math.cos(dist)))
        realPoint = np.reshape(qec.GetRotMat()*QEC.ToRotMat(0,math.radians(-90),0)*c, 3)
        (rx, ry, rz) = (realPoint.item(0), realPoint.item(1), realPoint.item(2))
        theta = math.acos( rz / math.sqrt(np.inner(realPoint,realPoint)))
        phi = math.atan2(ry,rx)
        return (theta, phi)

