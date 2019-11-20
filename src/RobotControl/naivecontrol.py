from Geometry.CoordinateConverter import CoordinateConverter
import numpy as np


class LinearInterpolator:
    def __init__(self, start, end, steps):
        self.start = start
        self.end = end
        self.t = 0.0  # from 0.0 to 1.0
        self.delta = 1.0 / steps

    def get_next(self):
        retPoint = []
        for idx in range(len(self.start)):
            p = self.start[idx] + self.t * (self.end[idx] - self.start[idx])
            retPoint.append(p)
        self.t += self.delta
        if self.t > 1.0:
            return None
        return retPoint

    def reset(self):
        self.t = 0.0


class LinearTrajectory:
    def __init__(self, leg, start_point, end_point):
        self.leg = leg
        self.linearInterpolator = LinearInterpolator(start_point, end_point, 10)
        self.next = None

    def setNext(self, nextTrajectory):
        self.next = nextTrajectory

    def getLastTrajectory(self):
        if self.next:
            return self.next.getLastTrajectory()
        else:
            return self

    def go(self):
        next_pos = self.linearInterpolator.get_next()
        print("next_pos", next_pos)
        if next_pos:
            self.leg.set_end_pos_local(next_pos)
            print("current leg position:", self.leg.get_target_pos())
            return True
        elif self.next:
            print("In next trajectory !!!!!!!!!!")
            return self.next.go()
        return False

    coord = CoordinateConverter()

    @staticmethod
    def genTrajectory(leg, world_positions):
        retTraj = None
        last_pos = None
        for pos in world_positions:
            if last_pos is None:
                last_pos = pos
            else:
                last_obj_pos = LinearTrajectory.coord.worldToObject(last_pos, leg.get_init_transformation_matrix())
                next_obj_pos = LinearTrajectory.coord.worldToObject(pos, leg.get_init_transformation_matrix())

                newTraj = LinearTrajectory(leg, last_obj_pos, next_obj_pos)
                last_pos = pos
                if retTraj is None:
                    retTraj = newTraj
                else:
                    retTraj.getLastTrajectory().setNext(newTraj)
        return retTraj


class RobotMove:
    def __init__(self, legs, allLegsHeight, leg_init_stretch):
        self.legs = legs
        self.allLegsHeight = allLegsHeight
        self.leg_init_stretch = leg_init_stretch
        self.trajectoryArray = []  # all currently running trajectories
        self.step_size = 0.1

        self.next_move = None

    # Move up and down via a mid point in the air, i.e. the leg is moving and didn't hold body weight
    def genLegMoveForwardTraj(self, legId):
        leg = self.legs[legId]
        objStartPos = [self.allLegsHeight, 0, self.leg_init_stretch]
        worldStartPos = LinearTrajectory.coord.objectToWorld(objStartPos, leg.get_init_transformation_matrix())
        worldTargetPos1 = [worldStartPos[0], worldStartPos[1] + self.step_size / 2,
                           worldStartPos[2] + self.step_size / 2]
        worldTargetPos2 = [worldStartPos[0], worldStartPos[1] + self.step_size, worldStartPos[2]]

        print("Step1 Leg:{} Traj Points:{},{},{}".format(legId, worldStartPos, worldTargetPos1, worldTargetPos2))
        return LinearTrajectory.genTrajectory(leg,
                                              [worldStartPos, worldTargetPos1, worldTargetPos2])

    # Move directly to the original point (in object space),
    # i.e. the leg is just rotating and is holding the body weight
    def genLegBackwardTraj(self, legId):
        leg = self.legs[legId]
        # 1. get current leg target position in world
        leg_target_point = leg.get_target_pos()

        print("target is:", leg_target_point)
        # TODO: not sure how to elegantly convert numpy data to python list
        worldStartPos = [leg_target_point[0].item(0), leg_target_point[1].item(0), leg_target_point[2].item(0)]
        objTargetPos = [self.allLegsHeight, 0, self.leg_init_stretch]
        worldTargetPos = LinearTrajectory.coord.objectToWorld(objTargetPos, leg.get_init_transformation_matrix())

        print("Step2 Leg:{} Traj Points:{},{}".format(legId, worldStartPos, worldTargetPos))

        return LinearTrajectory.genTrajectory(leg, [worldStartPos, worldTargetPos])

    def go(self):  # return False if the move is finished
        endedTraj = []

        for traj in self.trajectoryArray:
            if traj is not None:
                if not traj.go():  # Can't move any more, at the end of the trajectory
                    endedTraj.append(traj)
        for tobeDeletedTraj in endedTraj:
            self.trajectoryArray.remove(tobeDeletedTraj)

        if len(self.trajectoryArray) is 0:
            if self.next_move is None:
                return False
            else:
                return self.next_move.go()
        return True

    def setNext(self, nextMove):
        self.next_move = nextMove
        return self


class GoForwardMoveStep1(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False

    def go(self):
        if not self.traj_calculated:
            traj0 = self.genLegMoveForwardTraj(0)
            traj2 = self.genLegMoveForwardTraj(2)
            traj4 = self.genLegMoveForwardTraj(4)

            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj4)

            self.traj_calculated = True
        return super().go()


class GoForwardMoveStep2(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj1 = self.genLegMoveForwardTraj(1)
            traj3 = self.genLegMoveForwardTraj(3)
            traj5 = self.genLegMoveForwardTraj(5)

            traj0 = self.genLegBackwardTraj(0)
            traj2 = self.genLegBackwardTraj(2)
            traj4 = self.genLegBackwardTraj(4)

            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)
        return super().go()


class GoForwardMoveStep3(RobotMove):
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.traj_calculated = False

    def go(self):
        if not self.traj_calculated:
            self.traj_calculated = True
            traj0 = self.genLegMoveForwardTraj(0)
            traj2 = self.genLegMoveForwardTraj(2)
            traj4 = self.genLegMoveForwardTraj(4)

            traj1 = self.genLegBackwardTraj(1)
            traj3 = self.genLegBackwardTraj(3)
            traj5 = self.genLegBackwardTraj(5)

            self.trajectoryArray.append(traj0)
            self.trajectoryArray.append(traj1)
            self.trajectoryArray.append(traj2)
            self.trajectoryArray.append(traj3)
            self.trajectoryArray.append(traj4)
            self.trajectoryArray.append(traj5)
        return super().go()


class MoveStepFactory:
    def __init__(self, legs, allLegsHeight=0, leg_init_stretch=0.3):
        self.legs = legs
        self.allLegsHeight = allLegsHeight
        self.leg_init_stretch = leg_init_stretch

    def genMove1(self):
        return GoForwardMoveStep1(self.legs, self.allLegsHeight, self.leg_init_stretch)

    def genMove2(self):
        return GoForwardMoveStep2(self.legs, self.allLegsHeight, self.leg_init_stretch)

    def genMove3(self):
        return GoForwardMoveStep3(self.legs, self.allLegsHeight, self.leg_init_stretch)

    def getGoMove(self):
        return self.genMove1().setNext(self.genMove2().setNext(self.genMove3().setNext(self.genMove2().setNext(self.genMove3()))))

class NavieControl:
    def __init__(self, legs):
        self.legs = legs
        self.allLegsHeight = -0.1
        self.leg_init_stretch = 0.3
        self.moves = []

    def update(self):
        endedMoves = []
        for move in self.moves:
            if not move.go():
                endedMoves.append(move)

        for endedMove in endedMoves:
            self.moves.remove(endedMove)

    def setLegHeight(self, height):
        self.allLegsHeight = height

    def setLegLinkAngle(self, legNo, linkNo):
        def setAngle(angle):
            self.legs[legNo].set_link_angle(linkNo, angle)
            print("Setting Leg:{}, link:{} to angle: {}".format(legNo, linkNo, angle))

        return setAngle

    def addValueChangeCallback(self, legNo, linkNo, callback):
        self.legs[legNo].set_link_callback(linkNo, callback)

    def getStatus(self, legNo):
        return self.legs[legNo].getStatus()

    def resetPos(self):
        for leg in self.legs:
            leg.set_end_pos_local([self.allLegsHeight, 0, self.leg_init_stretch])

    def robotGo(self):
        stepFactory = MoveStepFactory(self.legs, self.allLegsHeight,self.leg_init_stretch)
        self.moves.append(stepFactory.getGoMove())
