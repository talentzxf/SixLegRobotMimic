class NavieControl:
    def __init__(self, legs):
        self.legs = legs

    def update(self):
        pass

    def setLegLinkAngle(self, legNo, linkNo):
        def setAngle(angle):
            self.legs[legNo].getLink(linkNo).setTheta(angle)
            pass
        return setAngle
