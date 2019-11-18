from RobotControl.linksystem import LinkSystem

from IKSolver.Solver import IKSolver

from Geometry.CoordinateConverter import CoordinateConverter


class RoboLeg(LinkSystem):
    def __init__(self, pos=None, rotate=None, name=None):
        super().__init__(pos, rotate)
        self.name = name
        self.link_length_array = []
        self.start_angles = []
        self.solver = IKSolver(self.link_length_array, self.start_angles)
        self.coord = CoordinateConverter()

    def getName(self):
        return self.name

    def add_link(self, length, axis):
        self.link_length_array.append(length)
        self.start_angles.append(0)
        super().add_link(length, axis)

    def set_link_angle(self, link_id, theta):
        self.links[link_id].setTheta(theta)

    def set_end_pos(self, target_world_pos):
        # 1. convert to object coordinate
        leg_relative_pos = self.coord.worldToObject(target_world_pos, self.get_init_transformation_matrix())
        # 2. Use IKSolver to solve it
        thetas = self.solver.solve(leg_relative_pos)

        if thetas is not None:
            # 3. Update angles
            for i in range(len(thetas)):
                self.set_link_angle(i, thetas[i])

    def getStatus(self):
        retStr = ""
        for linkIdx in range(len(self.links)):
            link = self.links[linkIdx]
            retStr += " link{}: {}".format(linkIdx, link.getTheta())

        return retStr
