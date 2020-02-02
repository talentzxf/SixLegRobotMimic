from RobotControl.linksystem import LinkSystem

from IKSolver.Solver import IKSolver

from Geometry.CoordinateConverter import CoordinateConverter
from GlobalConfig import RobotConfig
from GlobalContext import GlobalContext


class RoboLeg(LinkSystem):
    def __init__(self, legId=None, pos=None, rotate=None):
        super().__init__(pos, rotate)
        self.legId = legId
        self.solver = IKSolver()
        self.coord = CoordinateConverter()

    def add_link(self, length, axis, init_theta=0.0, isMovable=True):
        new_link = super().add_link(length, axis, init_theta, isMovable)
        self.solver.add_link(new_link)

    # TODO: Move this to super class
    def set_link_angle(self, link_id, theta):
        self.movable_links[link_id].setTheta(theta)
        if RobotConfig.enable_serial:
            GlobalContext.getSerial().set_angle(self.legId, link_id, theta)

    def set_link_callback(self, link_id, callback):
        self.links[link_id].angleChanged.connect(callback)

    def set_end_pos_local(self, target_obj_pos):
        print("Setting local pos:" + str(target_obj_pos))
        thetas = self.solver.solve(target_obj_pos)
        print("theta:" + str(thetas))
        if thetas is not None:
            # 3. Update angles
            for i in range(len(thetas)):
                self.set_link_angle(i, thetas[i])
        return thetas

    def set_end_pos(self, target_world_pos):
        print("Setting world pos:" + str(target_world_pos))
        target_obj_pos = self.coord.worldToObject(target_world_pos, self.get_init_transformation_matrix())
        return self.set_end_pos_local(target_obj_pos)

    def getStatus(self):
        retStr = ""
        for linkIdx in range(len(self.links)):
            link = self.links[linkIdx]
            retStr += " link{}: {:4.2f}".format(linkIdx, link.getTheta())

        return retStr
