from GlobalConfig import RobotConfig

from RobotControl.RobotMove.ForwardMove import MoveStepFactory

from RobotControl.RobotMove.StopMove import StopMove

from RobotControl.RobotMove.RotateMove import RotateMoveFactory

from RobotControl.RobotMove.BackStepFactory import BackStepFactory

import GlobalConfig


class NavieControl:
    def __init__(self, legs):
        self.legs = legs
        self.allLegsHeight = RobotConfig.defaultLegHeight
        self.leg_init_stretch = RobotConfig.defaultStretch
        self.moves = []

    def isMoving(self):
        if len(self.moves) != 0:
            return True
        return False

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
        RobotConfig.defaultLegHeight = height

    def getLegHeight(self):
        return self.allLegsHeight

    def setLegLinkAngle(self, legNo, linkNo, write_remote=False):
        def setAngle(angle):
            print("Setting Leg:{}, link:{} to angle: {}".format(legNo, linkNo, angle))
            self.legs[legNo].set_link_angle(linkNo, angle)

            if GlobalConfig.enable_remote_rest:
                # send command to remote
                base_url = GlobalConfig.RobotConfig.base_url
                full_url = base_url.format(legNo, linkNo, angle)
                print("calling:", full_url)

                try:
                    print("Response:", response=requests.post(full_url))
                except Exception as e:
                    print("Error calling remote service", e)

        return setAngle

    def addValueChangeCallback(self, legNo, linkNo, callback):
        self.legs[legNo].set_link_callback(linkNo, callback)

    def getStatus(self, legNo):
        return self.legs[legNo].getStatus()

    def resetPos(self):
        for leg in self.legs:
            leg.set_end_pos_local([self.allLegsHeight, 0, self.leg_init_stretch])

    def _robotGo(self):
        stepFactory = MoveStepFactory(self.legs, self.allLegsHeight, self.leg_init_stretch)
        self.moves.append(stepFactory.getGoMove().setCallBack(self._robotGo))

    def _robotBack(self):
        stepFactory = BackStepFactory(self.legs, self.allLegsHeight, self.leg_init_stretch)
        self.moves.append(stepFactory.getBackMove().setCallBack(self._robotBack))

    def robotBack(self):
        self.robotStop()  # Stop first, then go forward
        self._robotBack()

    def robotGo(self):
        self.robotStop()  # Stop first, then go forward
        self._robotGo()

    # TODO, check if leg is too low. If too low, raise and then put down to avoid damage!!!
    def robotStop(self):
        self.moves = []  # Remove all current moves
        self.moves.append(StopMove(self.legs, self.allLegsHeight, self.leg_init_stretch))

    def _robotRotate(self, theta):
        def __robotRotate():
            rotateStepFactory = RotateMoveFactory(self.legs, self.allLegsHeight, self.leg_init_stretch)
            self.moves.append(rotateStepFactory.getMove(theta).setCallBack(self._robotRotate(theta)))

        return __robotRotate

    def robotLeft(self):
        self.robotStop()
        self._robotRotate(-45)()

    def robotRight(self):
        self.robotStop()
        self._robotRotate(45)()
