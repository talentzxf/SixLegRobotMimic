from RobotControl.RobotMove.RobotMove import RobotMove


class IKLegMove(RobotMove):
    def __init__(self, legs, legId, targetHeight, allLegsHeight=0, leg_init_stretch=0.3, ):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.targetHeight = targetHeight
        self.legId = legId

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True

            self.trajectoryArray.append(self.genLegBackToStartTraj(self.legId, self.targetHeight))

        return super().go()
