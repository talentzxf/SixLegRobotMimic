from RobotControl.linksystem import LinkSystem
from RobotControl.naivecontrol import NavieControl


class RobotModel:
    def __init__(self):
        self.legs = []
        leg = LinkSystem([-0.1, 0, 0], [90, 0.0, 1.0, 0.0])
        leg.add_link(0.2, [1.0, 0.0, 0.0])
        leg.add_link(0.1, [0.0, 1.0, 0.0])
        leg.add_link(0.1, [1.0, 0.0, 0.0])

        self.legs.append(leg)

        leg = LinkSystem([0.1, 0, 0], [90, 0.0, 1.0, 0.0])
        leg.add_link(0.2, [1.0, 0.0, 0.0])
        leg.add_link(0.1, [0.0, 1.0, 0.0])
        leg.add_link(0.1, [1.0, 0.0, 0.0])
        self.legs.append(leg)

        leg = LinkSystem([0.1, 0.1, 0], [45, 0.0, 0.0, 1.0])
        leg.add_link(0.2, [1.0, 0.0, 0.0])
        leg.add_link(0.1, [0.0, 1.0, 0.0])
        leg.add_link(0.1, [1.0, 0.0, 0.0])
        self.legs.append(leg)

        self.control_system = NavieControl(leg)

    def initRobot(self):
        for leg in self.legs:
            leg.genObjectList()

    def draw(self):
        for leg in self.legs:
            leg.draw()

        self.control_system.update()
