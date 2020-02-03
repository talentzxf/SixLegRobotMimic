from RobotControl.RobotMove.RobotMove import RobotMove


class StopMove(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True

            # for legId in range(len(self.legs)):
                 #self.trajectoryArray.append(self.genLegBackToStartTraj(legId))

            self.trajectoryArray.append(self.genLegBackToStartTraj(0))
        return super().go()
