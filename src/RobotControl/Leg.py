from RobotControl.linksystem import LinkSystem

from IKSolver.Solver import IKSolver

from Geometry.CoordinateConverter import CoordinateConverter
from GlobalConfig import RobotConfig
from GlobalContext import GlobalContext


class RoboLeg(LinkSystem):
    def __init__(self, legId=None, pos=None, rotate=None):
        super().__init__(pos, rotate)
        self.legId = legId
        self.link_length_array = []
        self.start_angles = []
        self.solver = IKSolver(self.link_length_array, self.start_angles)
        self.coord = CoordinateConverter()

    def add_link(self, length, axis, init_theta=0.0):
        self.link_length_array.append(length)
        self.start_angles.append(init_theta)
        super().add_link(length, axis, init_theta)

    def set_link_angle(self, link_id, theta):
        self.links[link_id].setTheta(theta)
        if RobotConfig.enable_serial:
            GlobalContext.getSerial().set_angle(self.legId, link_id, theta)

    def set_link_callback(self, link_id, callback):
        self.links[link_id].angleChanged.connect(callback)

    def set_end_pos_local(self, target_obj_pos):
        print("Setting local pos:"+str(target_obj_pos))
        thetas = self.solver.solve(target_obj_pos)
        print("theta:"+str(thetas))
        if thetas is not None:
            # 3. Update angles
            for i in range(len(thetas)):
                self.set_link_angle(i, thetas[i])

    def set_end_pos(self, target_world_pos):
        print("Setting world pos:" + str(target_world_pos))
        target_obj_pos = self.coord.worldToObject(target_world_pos, self.get_init_transformation_matrix())
        self.set_end_pos_local(target_obj_pos)

    def getStatus(self):
        retStr = ""
        for linkIdx in range(len(self.links)):
            link = self.links[linkIdx]
            retStr += " link{}: {:4.2f}".format(linkIdx, link.getTheta())

        return retStr
