from RobotControl.RobotMove.FlushMove import FlushMove
from RobotControl.RobotMove.RobotMove import PointTrajMove


class InclineMove(PointTrajMove):
    def __init__(self, legs, matrix=None, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.incline_matrix = matrix

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True

            for legId in range(len(self.legs)):
                self.trajectoryArray.append(self.genLegBackToStartTraj(legId, None, self.incline_matrix))
            self.trajectoryArray.append(FlushMove())
        return super().go()
