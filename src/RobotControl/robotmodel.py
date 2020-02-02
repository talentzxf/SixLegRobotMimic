from RobotControl.linksystem import LinkSystem
from RobotControl.naivecontrol import NavieControl
import OpenGL.GL as gl
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtGui import QColor

from GlobalConfig import RobotConfig

from Geometry.cube import Cube

from RobotControl.Leg import RoboLeg

from GlobalConfig import RobotConfig


class RobotModel:
    link1_length = RobotConfig.link1Length
    link2_length = RobotConfig.link2Length

    link2_arm_length = getattr(RobotConfig, "link2_arm_length", None)
    link2_arm_angle = getattr(RobotConfig, "link2_arm_angle", 0.0)

    link3_length = RobotConfig.link3Length
    link4_length = getattr(RobotConfig, 'link4Length', None)

    # Add a static link4
    link3_4Angle_Y = getattr(RobotConfig, "link3_4Angle_Y", 0.0)

    @staticmethod
    def addLegLinks(leg):
        leg.add_link(RobotModel.link1_length, [1.0, 0.0, 0.0])
        leg.add_link(RobotModel.link2_length, [0.0, 1.0, 0.0])
        if RobotModel.link2_arm_length:
            leg.add_link(RobotModel.link2_arm_length, [0.0, 1.0, 0.0], RobotModel.link2_arm_angle, False)  # This arm is fixed
        leg.add_link(RobotModel.link3_length, [0.0, 1.0, 0.0])

        if RobotModel.link4_length is not None and RobotModel.link4_length > 0:
            leg.add_link(RobotModel.link4_length, [0.0, 1.0, 0.0], RobotModel.link3_4Angle_Y, False) # This link is fixed

    def __init__(self):
        self.legs = []

        width = RobotConfig.bodyWidth
        length = RobotConfig.bodyLength
        height = RobotConfig.bodyHeight

        self.body = Cube(length, width, height)

        leg = RoboLeg(0, [width / 2, length / 2, 0], [[-135, 0.0, 0.0, 1.0], [-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = RoboLeg(1, [width / 2, 0, 0], [[180, 0.0, 0.0, 1.0], [-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = RoboLeg(2, [width / 2, -length / 2, 0], [[135, 0.0, 0.0, 1.0], [-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = RoboLeg(3, [-width / 2, -length / 2, 0], [[45, 0.0, 0.0, 1.0], [-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = RoboLeg(4, [-width / 2, 0, 0], [[-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = RoboLeg(5, [-width / 2, length / 2, 0], [[-45, 0.0, 0.0, 1.0], [-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        self.control_system = NavieControl(self.legs)

    def getController(self):
        return self.control_system

    def initRobot(self):
        self.body.init_object()
        for leg in self.legs:
            leg.init_object()

    def getLegs(self):
        return self.legs

    def getLeg(self, legId):
        return self.legs[legId]

    def draw(self):
        self.body.draw()

        for leg in self.legs:
            gl.glPushMatrix()
            leg.draw()
            gl.glPopMatrix()

        self.control_system.update()

    def legSelected(self, legIdx):
        print("Leg:{} selected".format(legIdx))
        for idx in range(len(self.legs)):
            leg = self.legs[idx]
            if idx is legIdx:
                leg.set_color(QColor.fromRgb(127, 127, 0))
            else:
                leg.set_color(QColor.fromRgb(127, 127, 127))
