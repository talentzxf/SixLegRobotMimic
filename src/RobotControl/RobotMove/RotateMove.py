from RobotControl.RobotMove.FlushMove import FlushMove
from RobotControl.RobotMove.RobotMove import PointTrajMove


class RotateMoveStep1(PointTrajMove):
    def __init__(self, legs, theta, step, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.theta = theta
        self.step = step

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj1 = self.genLegBackToStartTraj(1)
            traj0 = self.genLegRotateTraj(0, self.theta, self.step)
            traj3 = self.genLegBackToStartTraj(3)
            traj2 = self.genLegRotateTraj(2, self.theta, self.step)
            traj5 = self.genLegBackToStartTraj(5)
            traj4 = self.genLegRotateTraj(4, self.theta, self.step)
            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)

            self.trajectoryArray.append(FlushMove())

        return super().go()


class RotateMoveStep2(PointTrajMove):
    def __init__(self, legs, theta, step, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.theta = theta
        self.step = step

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj0 = self.genLegBackToStartTraj(0)
            traj1 = self.genLegRotateTraj(1, self.theta, self.step)
            traj2 = self.genLegBackToStartTraj(2)
            traj3 = self.genLegRotateTraj(3, self.theta, self.step)
            traj4 = self.genLegBackToStartTraj(4)
            traj5 = self.genLegRotateTraj(5, self.theta, self.step)
            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)

            self.trajectoryArray.append(FlushMove())

        return super().go()


class RotateMoveFactory(PointTrajMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        self.legs = legs
        self.allLegsHeight = allLegsHeight
        self.leg_init_stretch = leg_init_stretch

    def genMove1(self, theta, step):
        return RotateMoveStep1(self.legs, theta, step, self.allLegsHeight, self.leg_init_stretch)

    def genMove2(self, theta, step):
        return RotateMoveStep2(self.legs, theta, step, self.allLegsHeight, self.leg_init_stretch)

    def getMove(self, theta):
        step1 = self.genMove1(theta, 1)
        step1.setNext(self.genMove1(theta, 2)).setNext(self.genMove2(theta, 1)).setNext(self.genMove2(theta, 2))
        return step1
