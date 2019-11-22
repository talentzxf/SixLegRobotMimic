from RobotControl.RobotMove.RobotMove import RobotMove


# TODO, implement this
class LeftMoveStep1(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            self.genLegRotateTraj(0, -45)

        return super().go()


class LeftMoveFactory(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        self.legs = legs
        self.allLegsHeight = allLegsHeight
        self.leg_init_stretch = leg_init_stretch

    def getMove(self):
        step1 = LeftMoveStep1(self.legs, self.allLegsHeight, self.leg_init_stretch)
        return step1
