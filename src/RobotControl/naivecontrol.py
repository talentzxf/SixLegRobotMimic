import time


class LinerInterpolator:
    def __init__(self, start, end, steps):
        self.start = start
        self.end = end
        self.t = 0.0  # from 0.0 to 1.0
        self.delta = 1.0 / steps

    def get_result(self):
        cur_position_x = self.start[0] + self.t * (self.end[0] - self.start[0])
        cur_position_y = self.start[1] + self.t * (self.end[1] - self.start[1])
        self.t += self.delta
        yield [cur_position_x, cur_position_y]


class NavieControl:
    def __init__(self, legs):
        self.legs = legs
        self.allLegsHeight = 0.0
        self.internallController = None

    def update(self):
        if self.internallController:
            self.internallController.update()

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
        self.internallController = ForwardStatus()
