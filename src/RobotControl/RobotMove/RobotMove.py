from GlobalConfig import RobotConfig

from RobotControl.RobotMove.LinearTrajectory import LinearTrajectory


class RobotMove:
    def __init__(self, legs, allLegsHeight, leg_init_stretch):
        self.legs = legs
        self.allLegsHeight = allLegsHeight
        self.leg_init_stretch = leg_init_stretch
        self.trajectoryArray = []  # all currently running trajectories
        self.step_size = RobotConfig.defaultStepSize

        self.next_move = None
        self.after_move_complete_callback = None

    def setCallBack(self, callback):
        self.after_move_complete_callback = callback
        return self

    def invoke_call_back(self):
        if self.after_move_complete_callback:
            self.after_move_complete_callback()

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

        if len(self.trajectoryArray) == 0:
            if self.next_move is None:
                return False
            else:
                return self.next_move.go()
        return True

    def setNext(self, nextMove):
        self.next_move = nextMove
        return nextMove