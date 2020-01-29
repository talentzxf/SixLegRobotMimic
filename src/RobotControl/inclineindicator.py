import math

from PyQt5.QtGui import QColor

from Geometry import MatrixOps
from Geometry.cylinder import Cylinder

import OpenGL.GL as gl

from GlobalConfig import RobotConfig


class PositionedCylinder(Cylinder):
    def __init__(self, radius, length, color=None, slices=200):
        super().__init__(radius, length, color, slices)
        self.position = [0.0, 0.0, 0.0]

    def setInitPos(self, x, y, z):
        self.position = [x, y, z]

    def draw(self):
        gl.glPushMatrix()
        gl.glTranslated(self.position[0], self.position[1], self.position[2])
        super().draw()
        gl.glPopMatrix()


class InclineIndicator:
    def __init__(self):
        self.indicator = Cylinder(0.15, 10, QColor.fromRgb(255, 0, 255))
        # self.rotation_matrix = np.identity(4)

        self.targetLegEndPoints = []
        # right up
        rightUpCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        rightUpCylinder.setInitPos(RobotConfig.bodyWidth / 2, RobotConfig.bodyLength / 2, 0.0)
        self.targetLegEndPoints.append(rightUpCylinder)

        # right center
        rightCenterCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        rightCenterCylinder.setInitPos(RobotConfig.bodyWidth / 2, 0, 0.0)
        self.targetLegEndPoints.append(rightCenterCylinder)

        # right down
        rightDownCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        rightDownCylinder.setInitPos(RobotConfig.bodyWidth / 2, -RobotConfig.bodyLength / 2, 0.0)
        self.targetLegEndPoints.append(rightDownCylinder)

        # Left up
        leftUpCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        leftUpCylinder.setInitPos(-RobotConfig.bodyWidth / 2, RobotConfig.bodyLength / 2, 0.0)
        self.targetLegEndPoints.append(leftUpCylinder)

        # left center
        leftCenterCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        leftCenterCylinder.setInitPos(-RobotConfig.bodyWidth / 2, 0, 0.0)
        self.targetLegEndPoints.append(leftCenterCylinder)

        # Left down
        leftDownCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        leftDownCylinder.setInitPos(-RobotConfig.bodyWidth / 2, -RobotConfig.bodyLength / 2, 0.0)
        self.targetLegEndPoints.append(leftDownCylinder)

        self.rotation_matrix = MatrixOps.rotate_matrix(0.5750981,
                                                       [-0.2080853 * 180 / math.pi, -0.19589223 * 180 / math.pi,
                                                        -0.7665436 * 180 / math.pi])

    def incline(self, theta, axis):
        self.rotation_matrix = MatrixOps.rotate_matrix(theta, axis)

    def init_object(self):
        self.indicator.init_object()
        for endPoint in self.targetLegEndPoints:
            endPoint.init_object()

    def draw(self):
        gl.glPushMatrix()
        gl.glMultMatrixd(self.rotation_matrix)
        self.indicator.draw()
        # draw six leg new end points
        for endPoint in self.targetLegEndPoints:
            endPoint.draw()
        gl.glPopMatrix()

    def getController(self):
        return self.controller
