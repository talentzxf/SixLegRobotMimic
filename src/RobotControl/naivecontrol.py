class NavieControl:
    def __init__(self, legs):
        self.legs = legs

    def update(self):
        pass

    def setLegLinkAngle(self, legNo, linkNo):
        def setAngle(angle):
            self.legs[legNo].getLink(linkNo).setTheta(angle)
            print("Setting Leg:{}, link:{} to angle: {}".format(legNo, linkNo, angle))

        return setAngle

    def getStatus(self, legNo):
        leg = self.legs[legNo]
        retStr = ""
        for linkIdx in range(leg.getLinkNumber()):
            link = leg.getLink(linkIdx)
            retStr += " link{}: {}".format(linkIdx, link.getTheta())

        return retStr


