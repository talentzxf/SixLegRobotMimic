from Geometry.CoordinateConverter import CoordinateConverter
from RobotControl.RobotMove.AbstractTrajectory import AbstractTrajectory


class PointTrajectory(AbstractTrajectory):
    def __init__(self, leg, points):
        super().__init__()
        self.points = points
        self.leg = leg
        self.execute_pos_id = 0

    coord = CoordinateConverter()

    def _go(self):
        if self.execute_pos_id < len(self.points):
            next_pos = self.points[self.execute_pos_id]
            next_local_pos = self.coord.worldToObject(next_pos, self.leg.get_init_transformation_matrix())
            self.execute_pos_id += 1
            self.leg.set_end_pos_local(next_local_pos)
            print("\t Set leg position:", self.coord.objectToWorld(next_pos, self.leg.get_init_transformation_matrix()))
            print("\t Current leg position:", self.leg.get_target_pos())
            return True
        else:
            return False
