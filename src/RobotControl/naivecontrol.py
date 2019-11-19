from Geometry.CoordinateConverter import CoordinateConverter


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

    def next_move(self):
        next_pos = self.linearInterpolator.get_next()
        print("next_pos", next_pos)
        if next_pos:
            self.leg.set_end_pos_local(next_pos)
            return True
        elif self.next:
            print("In next trajectory !!!!!!!!!!")
            return self.next.next_move()
        return False


class StopTrajectory:
    def __init__(self, startTime, duration):
        pass


class NavieControl:
    def __init__(self, legs):
        self.legs = legs
        self.allLegsHeight = -0.1
        self.leg_init_stretch = 0.3
        self.step_size = 0.1
        self.trajectoryArray = []  # all currently running trajectories
        self.coord = CoordinateConverter()

    def update(self):
        endedTraj = []

        for traj in self.trajectoryArray:
            if traj is not None:
                if not traj.next_move():  # Can't move any more, at the end of the trajectory
                    endedTraj.append(traj)

        for tobeDeletedTraj in endedTraj:
            self.trajectoryArray.remove(tobeDeletedTraj)

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

    def genTrajectory(self, leg, world_positions):
        retTraj = None
        last_pos = None
        for pos in world_positions:
            if last_pos is None:
                last_pos = pos
            else:
                last_obj_pos = self.coord.worldToObject(last_pos, leg.get_init_transformation_matrix())
                next_obj_pos = self.coord.worldToObject(pos, leg.get_init_transformation_matrix())

                print("from obj:{} to {}", last_obj_pos, next_obj_pos)
                newTraj = LinearTrajectory(leg, last_obj_pos, next_obj_pos)
                last_pos = pos
                if retTraj is None:
                    retTraj = newTraj
                else:
                    retTraj.getLastTrajectory().setNext(newTraj)
        return retTraj

    def genLegMoveForwardTraj(self, legId):
        leg = self.legs[legId]
        objStartPos = [self.allLegsHeight, 0, self.leg_init_stretch]
        worldStartPos = self.coord.objectToWorld(objStartPos, leg.get_init_transformation_matrix())
        worldTargetPos1 = [worldStartPos[0], worldStartPos[1] + self.step_size / 2,
                           worldStartPos[2] + self.step_size / 2]
        worldTargetPos2 = [worldStartPos[0], worldStartPos[1] + self.step_size, worldStartPos[2]]

        print("Traj Points:{},{},{}".format(worldStartPos, worldTargetPos1, worldTargetPos2))
        return self.genTrajectory(leg,
                                  [worldStartPos, worldTargetPos1, worldTargetPos2])

    def robotGo(self):
        traj0 = self.genLegMoveForwardTraj(0)
        traj2 = self.genLegMoveForwardTraj(2)
        traj4 = self.genLegMoveForwardTraj(4)

        traj0.getLastTrajectory().setNext(self.genLegMoveForwardTraj(1))
        traj2.getLastTrajectory().setNext(self.genLegMoveForwardTraj(3))
        traj4.getLastTrajectory().setNext(self.genLegMoveForwardTraj(5))

        self.trajectoryArray.append(traj0)
        self.trajectoryArray.append(traj2)
        self.trajectoryArray.append(traj4)
