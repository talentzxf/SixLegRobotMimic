from RobotControl.RobotMove.FlushMove import FlushMove
from RobotControl.RobotMove.RobotMove import PointTrajMove


class StopMove(PointTrajMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True

            self.genLegBackToStartTraj(0)
            for legId in range(len(self.legs)):
                self.trajectoryArray.append(self.genLegBackToStartTraj(legId))

            self.trajectoryArray.append(FlushMove())
        return super().go()
