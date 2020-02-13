from RobotControl.RobotMove.FlushMove import FlushMove
from RobotControl.RobotMove.RobotMove import PointTrajMove


class GoBackMoveStep1(PointTrajMove):
    def __init__(self, legs, step, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.step = step

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj1 = self.genLegMoveBackTraj(1, self.step)
            traj3 = self.genLegMoveBackTraj(3, self.step)
            traj5 = self.genLegMoveBackTraj(5, self.step)

            traj0 = self.genLegBackToStartTraj(0)
            traj2 = self.genLegBackToStartTraj(2)
            traj4 = self.genLegBackToStartTraj(4)

            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)
            self.trajectoryArray.append(FlushMove())
        return super().go()


class GoBackMoveStep2(PointTrajMove):
    def __init__(self, legs, step, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.step = step

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj0 = self.genLegMoveBackTraj(0, self.step)
            traj2 = self.genLegMoveBackTraj(2, self.step)
            traj4 = self.genLegMoveBackTraj(4, self.step)

            traj1 = self.genLegBackToStartTraj(1)
            traj3 = self.genLegBackToStartTraj(3)
            traj5 = self.genLegBackToStartTraj(5)

            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)

            self.trajectoryArray.append(FlushMove())
        return super().go()


class BackStepFactory:
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        self.legs = legs
        self.allLegsHeight = allLegsHeight
        self.leg_init_stretch = leg_init_stretch

    def genMove1(self, step):
        return GoBackMoveStep1(self.legs, step, self.allLegsHeight, self.leg_init_stretch)

    def genMove2(self, step):
        return GoBackMoveStep2(self.legs, step, self.allLegsHeight, self.leg_init_stretch)

    def getBackMove(self):
        first_step = self.genMove1(1)
        first_step.setNext(self.genMove1(2)).setNext(self.genMove2(1)).setNext(self.genMove2(2))
        return first_step
