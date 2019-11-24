from RobotControl.RobotMove.RobotMove import RobotMove


class LeftMoveStep1(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj1 = self.genLegBackToStartTraj(1)
            traj0 = self.genLegRotateTraj(0, -45)
            traj3 = self.genLegBackToStartTraj(3)
            traj2 = self.genLegRotateTraj(2, -45)
            traj5 = self.genLegBackToStartTraj(5)
            traj4 = self.genLegRotateTraj(4, -45)
            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)

        return super().go()


class LeftMoveStep2(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj0 = self.genLegBackToStartTraj(0)
            traj1 = self.genLegRotateTraj(1, -45)
            traj2 = self.genLegBackToStartTraj(2)
            traj3 = self.genLegRotateTraj(3, -45)
            traj4 = self.genLegBackToStartTraj(4)
            traj5 = self.genLegRotateTraj(5, -45)
            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)

        return super().go()


class LeftMoveFactory(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        self.legs = legs
        self.allLegsHeight = allLegsHeight
        self.leg_init_stretch = leg_init_stretch

    def getMove(self):
        step1 = LeftMoveStep1(self.legs, self.allLegsHeight, self.leg_init_stretch)
        step1.setNext(LeftMoveStep2(self.legs, self.allLegsHeight, self.leg_init_stretch))
        return step1
