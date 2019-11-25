from GlobalConfig import RobotConfig

from RobotControl.RobotMove.ForwardMove import MoveStepFactory

from RobotControl.RobotMove.StopMove import StopMove

from RobotControl.RobotMove.RotateMove import RotateMoveFactory

import requests

import GlobalConfig
import serial


class SerialControl:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        print('Serial enabled!')

    def convert_angle(self, angle):
        # 0 -- 500
        # 90 -- 1500
        # 180 -- 2000
        return 1500 + angle / 180 * 2000

    def set_angle(self, leg_id, link_id, angle):
        # Hack to make the mimic robot same as the real robot
        if link_id == 1 or link_id == 0:
            angle = -angle
        cmd = '"#%03dP%04dT0100!"' % (self.leg_link_map[leg_id][link_id], self.convert_angle(angle))
        self.ser.write(cmd.encode())
        print('Set serial:', cmd)
        return {"cmd": cmd}


class NavieControl:
    def __init__(self, legs, update_serial=False):
        self.legs = legs
        self.allLegsHeight = RobotConfig.defaultLegHeight
        self.leg_init_stretch = RobotConfig.defaultStretch
        self.moves = []
        self.update_serial = update_serial
        if update_serial:
            self.enableSerial()

    def enableSerial(self):
        self.update_serial = True
        self.serial = SerialControl()

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

    def setLegLinkAngle(self, legNo, linkNo, write_remote=False):
        def setAngle(angle):
            self.legs[legNo].set_link_angle(linkNo, angle)
            print("Setting Leg:{}, link:{} to angle: {}".format(legNo, linkNo, angle))

            if self.update_serial:
                self.serial.set_angle(legNo, linkNo, angle)

            if write_remote:
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
