from RobotControl.linksystem import LinkSystem
from RobotControl.naivecontrol import NavieControl
import OpenGL.GL as gl
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtGui import QColor

from GlobalConfig import RobotConfig

from Geometry.cube import Cube


class RobotModel:
    link1_length = 0.05
    link2_length = 0.1
    link3_length = 0.1

    @staticmethod
    def addLegLinks(leg):
        leg.add_link(RobotModel.link1_length, [1.0, 0.0, 0.0])
        leg.add_link(RobotModel.link2_length, [0.0, 1.0, 0.0])
        leg.add_link(RobotModel.link3_length, [0.0, 1.0, 0.0])

    def __init__(self):
        self.legs = []

        width = RobotConfig.bodyWidth
        length = RobotConfig.bodyLength
        height = RobotConfig.bodyHeight

        self.body = Cube(length, width, height)

        leg = LinkSystem([width/2, length/2, 0], [[45, 0.0, 0.0, 1.0], [90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = LinkSystem([width/2, 0, 0], [[90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = LinkSystem([width/2, -length/2, 0], [[-45, 0.0, 0.0, 1.0], [90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = LinkSystem([-width/2, -length/2, 0], [[45, 0.0, 0.0, 1.0], [-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = LinkSystem([-width/2, 0, 0], [[-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = LinkSystem([-width/2, length/2, 0], [[-45, 0.0, 0.0, 1.0], [-90, 0.0, 1.0, 0.0]])
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
