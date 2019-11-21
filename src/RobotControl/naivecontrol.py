from GlobalConfig import RobotConfig

from RobotControl.RobotMove.ForwardMove import MoveStepFactory


class NavieControl:
    def __init__(self, legs):
        self.legs = legs
        self.allLegsHeight = RobotConfig.defaultLegHeight
        self.leg_init_stretch = RobotConfig.defaultStretch
        self.moves = []

    def update(self):
        endedMoves = []
        for move in self.moves:
            if not move.go():
                move.invoke_call_back()
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
        stepFactory = MoveStepFactory(self.legs, self.allLegsHeight, self.leg_init_stretch)
        self.moves.append(stepFactory.getGoMove().setCallBack(self.robotGo))

    def robotStop(self):
        pass
