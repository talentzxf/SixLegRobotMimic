from RobotControl.RobotMove.RobotMove import RobotMove


class InclineMove(RobotMove):
    def __init__(self, legs, matrix=None, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.incline_matrix = matrix

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True

            for legId in range(len(self.legs)):
                self.trajectoryArray.append(self.genLegBackToStartTraj(legId, None, self.incline_matrix))

        return super().go()
