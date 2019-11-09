from RobotControl.linksystem import LinkSystem
from RobotControl.naivecontrol import NavieControl
import OpenGL.GL as gl

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
        leg = LinkSystem([0.1, 0.1, 0], [[45, 0.0, 0.0, 1.0], [90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = LinkSystem([0.1, 0, 0], [[90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = LinkSystem([0.1, -0.1, 0], [[-45, 0.0, 0.0, 1.0], [90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = LinkSystem([-0.1, -0.1, 0], [[45, 0.0, 0.0, 1.0], [-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = LinkSystem([-0.1, 0, 0], [[-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        leg = LinkSystem([-0.1, 0.1, 0], [[-45, 0.0, 0.0, 1.0], [-90, 0.0, 1.0, 0.0]])
        self.addLegLinks(leg)
        self.legs.append(leg)

        self.control_system = NavieControl(self.legs)

    def getController(self):
        return self.control_system

    def initRobot(self):
        for leg in self.legs:
            leg.genObjectList()

    def draw(self):
        for leg in self.legs:
            gl.glPushMatrix()
            leg.draw()
            gl.glPopMatrix()

        self.control_system.update()
