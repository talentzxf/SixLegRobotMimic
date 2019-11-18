class NavieControl:
    def __init__(self, legs):
        self.legs = legs

    def update(self):
        pass

    def setLegLinkAngle(self, legNo, linkNo):
        def setAngle(angle):
            self.legs[legNo].set_link_angle(linkNo, angle)
            print("Setting Leg:{}, link:{} to angle: {}".format(legNo, linkNo, angle))

        return setAngle

    def getStatus(self, legNo):
        return self.legs[legNo].getStatus()