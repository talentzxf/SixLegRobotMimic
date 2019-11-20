from RobotControl.linksystem import LinkSystem

from IKSolver.Solver import IKSolver

from Geometry.CoordinateConverter import CoordinateConverter


class RoboLeg(LinkSystem):
    def __init__(self, pos=None, rotate=None):
        super().__init__(pos, rotate)
        self.link_length_array = []
        self.start_angles = []
        self.solver = IKSolver(self.link_length_array, self.start_angles)
        self.coord = CoordinateConverter()

    def add_link(self, length, axis):
        self.link_length_array.append(length)
        self.start_angles.append(0)
        super().add_link(length, axis)

    def set_link_angle(self, link_id, theta):
        self.links[link_id].setTheta(theta)

    def set_link_callback(self, link_id, callback):
        self.links[link_id].angleChanged.connect(callback)

    def set_end_pos_local(self, target_obj_pos):
        thetas = self.solver.solve(target_obj_pos)
        if thetas is not None:
            # 3. Update angles
            for i in range(len(thetas)):
                self.set_link_angle(i, thetas[i])

    def set_end_pos(self, target_world_pos):
        target_obj_pos = self.coord.worldToObject(target_world_pos, self.get_init_transformation_matrix())
        self.set_end_pos_local(target_obj_pos)

    def getStatus(self):
        retStr = ""
        for linkIdx in range(len(self.links)):
            link = self.links[linkIdx]
            retStr += " link{}: {:4.2f}".format(linkIdx, link.getTheta())

        return retStr
