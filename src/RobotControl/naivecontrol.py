import time


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
    def __init__(self, leg, start_point, end_point, stopWhenEnded=True):
        self.leg = leg
        self.linearInterpolator = LinearInterpolator(start_point, end_point, 10)
        self.stopWhenEnded = stopWhenEnded

    def next_move(self):
        next_pos = self.linearInterpolator.get_next()
        print("next_pos", next_pos)
        if next_pos:
            self.leg.set_end_pos_local(next_pos)
            return True
        elif not self.stopWhenEnded:
            self.linearInterpolator.reset()
            return True
        return False


class NavieControl:
    def __init__(self, legs):
        self.legs = legs
        self.allLegsHeight = 0.0
        self.trajectory = None

    def update(self):
        if self.trajectory:
            self.trajectory.next_move()

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
            leg.set_end_pos_local([self.allLegsHeight, 0, 0.3])

    def robotGo(self):
        self.trajectory = LinearTrajectory(self.legs[0],
                                           [self.allLegsHeight, 0, 0.3],
                                           [0.5, 0, 0.3])
