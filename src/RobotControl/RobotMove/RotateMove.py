from RobotControl.RobotMove.FlushMove import FlushMove
from RobotControl.RobotMove.RobotMove import RobotMove


class RotateMoveStep1(RobotMove):
    def __init__(self, legs, theta, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.theta = theta

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj1 = self.genLegBackToStartTraj(1)
            traj0 = self.genLegRotateTraj(0, self.theta)
            traj3 = self.genLegBackToStartTraj(3)
            traj2 = self.genLegRotateTraj(2, self.theta)
            traj5 = self.genLegBackToStartTraj(5)
            traj4 = self.genLegRotateTraj(4, self.theta)
            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)

        return super().go()


class RotateMoveStep2(RobotMove):
    def __init__(self, legs, theta, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.theta = theta

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj0 = self.genLegBackToStartTraj(0)
            traj1 = self.genLegRotateTraj(1, self.theta)
            traj2 = self.genLegBackToStartTraj(2)
            traj3 = self.genLegRotateTraj(3, self.theta)
            traj4 = self.genLegBackToStartTraj(4)
            traj5 = self.genLegRotateTraj(5, self.theta)
            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)

            self.trajectoryArray.append(FlushMove())

        return super().go()


class RotateMoveFactory(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        self.legs = legs
        self.allLegsHeight = allLegsHeight
        self.leg_init_stretch = leg_init_stretch

    def getMove(self, theta):
        step1 = RotateMoveStep1(self.legs, theta, self.allLegsHeight, self.leg_init_stretch)
        step1.setNext(RotateMoveStep2(self.legs, theta, self.allLegsHeight, self.leg_init_stretch))
        return step1
