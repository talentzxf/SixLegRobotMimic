from RobotControl.RobotMove.FlushMove import FlushMove
from RobotControl.RobotMove.RobotMove import PointTrajMove


class GoForwardMoveStep1(PointTrajMove):
    def __init__(self, legs, step, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.step = step

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True

            self.trajectoryArray.append(self.genLegBackToStartTraj(0))
            self.trajectoryArray.append(self.genLegBackToStartTraj(2))
            self.trajectoryArray.append(self.genLegBackToStartTraj(4))

            self.trajectoryArray.append(self.genLegMoveForwardTraj(1, self.step))
            self.trajectoryArray.append(self.genLegMoveForwardTraj(3, self.step))
            self.trajectoryArray.append(self.genLegMoveForwardTraj(5, self.step))
            self.trajectoryArray.append(FlushMove())
        return super().go()


class GoForwardMoveStep2(PointTrajMove):
    def __init__(self, legs, step, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False
        self.step = step

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True

            self.trajectoryArray.append(self.genLegBackToStartTraj(1))
            self.trajectoryArray.append(self.genLegBackToStartTraj(3))
            self.trajectoryArray.append(self.genLegBackToStartTraj(5))

            self.trajectoryArray.append(self.genLegMoveForwardTraj(0, self.step))
            self.trajectoryArray.append(self.genLegMoveForwardTraj(2, self.step))
            self.trajectoryArray.append(self.genLegMoveForwardTraj(4, self.step))
            self.trajectoryArray.append(FlushMove())

        return super().go()


class MoveStepFactory:
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        self.legs = legs
        self.allLegsHeight = allLegsHeight
        self.leg_init_stretch = leg_init_stretch

    def genMove1(self, step):
        return GoForwardMoveStep1(self.legs, step, self.allLegsHeight, self.leg_init_stretch)

    def genMove2(self, step):
        return GoForwardMoveStep2(self.legs, step, self.allLegsHeight, self.leg_init_stretch)

    def getGoMove(self):
        first_step = self.genMove1(1)
        first_step.setNext(self.genMove1(2)).setNext(self.genMove2(1)).setNext(self.genMove2(2))
        return first_step
