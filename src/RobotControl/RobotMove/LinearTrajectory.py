from Geometry.CoordinateConverter import CoordinateConverter


class LinearInterpolator:
    def __init__(self, start, end, steps):
        self.start = start
        self.end = end
        self.t = 0.0  # from 0.0 to 1.0
        self.delta = 1.0 / steps

    def get_next(self):
        if self.t > 1.0:
            return None

        retPoint = []
        for idx in range(len(self.start)):
            p = self.start[idx] + self.t * (self.end[idx] - self.start[idx])
            retPoint.append(p)
        self.t += self.delta
        return retPoint

    def reset(self):
        self.t = 0.0


class LinearTrajectory:
    def __init__(self, leg, start_point, end_point):
        self.leg = leg
        self.linearInterpolator = LinearInterpolator(start_point, end_point, 1)
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
        if next_pos:
            self.leg.set_end_pos_local(next_pos)
            print("\t Set leg position:", self.coord.objectToWorld(next_pos, self.leg.get_init_transformation_matrix()))
            print("\t Current leg position:", self.leg.get_target_pos())
            return True
        elif self.next:
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
