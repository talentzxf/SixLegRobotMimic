import time


class ForwardController:
    def __init__(self, start_time):
        self.start_time = start_time



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
        self.internallController = ForwardController(time.time())
