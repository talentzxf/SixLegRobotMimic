from RobotControl.RobotMove.RobotMove import RobotMove


class GoBackMoveStep1(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj1 = self.genLegMoveBackTraj(1)
            traj3 = self.genLegMoveBackTraj(3)
            traj5 = self.genLegMoveBackTraj(5)

            traj0 = self.genLegBackToStartTraj(0)
            traj2 = self.genLegBackToStartTraj(2)
            traj4 = self.genLegBackToStartTraj(4)

            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)
        return super().go()


class GoBackMoveStep2(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj0 = self.genLegMoveBackTraj(0)
            traj2 = self.genLegMoveBackTraj(2)
            traj4 = self.genLegMoveBackTraj(4)

            traj1 = self.genLegBackToStartTraj(1)
            traj3 = self.genLegBackToStartTraj(3)
            traj5 = self.genLegBackToStartTraj(5)

            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)
        return super().go()


class BackStepFactory:
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        self.legs = legs
        self.allLegsHeight = allLegsHeight
        self.leg_init_stretch = leg_init_stretch

    def genMove1(self):
        return GoBackMoveStep1(self.legs, self.allLegsHeight, self.leg_init_stretch)

    def genMove2(self):
        return GoBackMoveStep2(self.legs, self.allLegsHeight, self.leg_init_stretch)

    def getBackMove(self):
        first_step = self.genMove1()
        first_step.setNext(self.genMove2())
        return first_step
