from Geometry import MatrixOps
from GlobalConfig import RobotConfig

from RobotControl.RobotMove.ForwardMove import MoveStepFactory
from RobotControl.RobotMove.InclineMove import InclineMove

from RobotControl.RobotMove.StopMove import StopMove

from RobotControl.RobotMove.RotateMove import RotateMoveFactory

from RobotControl.RobotMove.BackStepFactory import BackStepFactory

from RobotControl.RobotMove.IKLegMove import IKLegMove


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

    def getLegHeight(self):
        return self.allLegsHeight

    def getLegStretch(self):
        return self.leg_init_stretch

    def setLegStretch(self, stretch):
        self.leg_init_stretch = stretch

    def setLegLinkAngle(self, legNo, linkNo, write_remote=False):
        def setAngle(angle):
            print("Setting Leg:{}, link:{} to angle: {}".format(legNo, linkNo, angle))
            self.legs[legNo].set_link_angle(linkNo, angle)

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

    def inclineRobot(self, theta, axis):
        # self.moves = []  # Stop current moves

        # 1. Convert angles to matrix
        rotate_matrix = MatrixOps.rotate_matrix(theta, axis)
        # 2. Calculate it's inverse
        rotate_matrix_inv = MatrixOps.inverse_rotate_matrix(rotate_matrix)

        inclineMove = InclineMove(self.legs, rotate_matrix_inv, self.allLegsHeight, self.leg_init_stretch)
        self.moves.append(inclineMove)

    def _robotBack(self):
        stepFactory = BackStepFactory(self.legs, self.allLegsHeight, self.leg_init_stretch)
        self.moves.append(stepFactory.getBackMove().setCallBack(self._robotBack))

    def robotBack(self):
        self.robotStop(self._robotBack)

    def robotGo(self):
        self.robotStop(self._robotGo)

    # TODO, check if leg is too low. If too low, raise and then put down to avoid damage!!!
    def robotStop(self, callback = None):
        self.moves = []  # Remove all current moves
        stopMove = StopMove(self.legs, self.allLegsHeight, self.leg_init_stretch)
        if callback is not None:
            stopMove.setCallBack(callback)
        self.moves.append(stopMove)

    def setSingleLegHeight(self, legId, targetHeight):
        # self.robotStop()
        self.moves.append(IKLegMove(self.legs, legId, targetHeight, self.allLegsHeight, self.leg_init_stretch))

    def _robotRotate(self, theta):
        def __robotRotate():
            rotateStepFactory = RotateMoveFactory(self.legs, self.allLegsHeight, self.leg_init_stretch)
            self.moves.append(rotateStepFactory.getMove(theta).setCallBack(self._robotRotate(theta)))

        return __robotRotate

    def robotLeft(self):
        self.robotStop(self._robotRotate(-45))

    def robotRight(self):
        self.robotStop(self._robotRotate(45))
