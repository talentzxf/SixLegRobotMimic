import serial

from GlobalConfig import RobotConfig


class SerialControl:
    def __init__(self):
        self.leg_link_angle_map = {
            0: {0: 0, 1: 0, 2: 0},
            1: {0: 0, 1: 0, 2: 0},
            2: {0: 0, 1: 0, 2: 0},
            3: {0: 0, 1: 0, 2: 0},
            4: {0: 0, 1: 0, 2: 0},
            5: {0: 0, 1: 0, 2: 0}
        }

        # self.leg_link_map = [[0, 1, 2],
        #                      [3, 4, 5],
        #                      [6, 7, 8],
        #                      [9, 10, 11],
        #                      [12, 13, 14],
        #                      [15, 16, 17]]


        self.leg_link_map = [[3, 2, 1],
                             [24, 23, 22],
                             [19, 18, 17],
                             [16, 15, 14],
                             [11, 10, 9],
                             [8, 7, 6]]

        # self.ser = serial.Serial(
        #     port='/dev/ttyAMA0',
        #     baudrate=115200,
        #     parity=serial.PARITY_NONE,
        #     stopbits=serial.STOPBITS_ONE,
        #     bytesize=serial.EIGHTBITS,
        #     timeout=1
        # )

        self.ser = serial.Serial("/dev/serial0", 9600)
        print('Serial enabled!')

    def convert_angle(self, angle):
        # 0 -- 500
        # 90 -- 1500
        # 180 -- 2000
        # return 1500 + angle / 180 * 2000
        return 1500 + angle/180 * 3000

    def set_angle(self, leg_id, link_id, angle):
        # Hack to make the mimic robot same as the real robot
        # if link_id == 1 or link_id == 0 or link_id == 2:
            # angle = -angle
        self.set_servo_angle(self.leg_link_map[leg_id][link_id], angle)

    def set_servo_angle(self, servo_id, angle):
        # cmd = '"#%03dP%04dT0100!"' % (servo_id, self.convert_angle(angle))
        cmd = '#%dP%04dT0200\r\n' % (servo_id, self.convert_angle(angle))
        self.ser.write(cmd.encode())
        print('Set serial:', cmd)
        return {"cmd": cmd}

class GlobalContext:
    robot = None
    serial = None

    @staticmethod
    def getRobot():
        from RobotControl.robotmodel import RobotModel
        if GlobalContext.robot is None:
            GlobalContext.robot = RobotModel()
        return GlobalContext.robot

    @staticmethod
    def getSerial():
        if GlobalContext.serial is None:
            GlobalContext.serial = SerialControl()
        return GlobalContext.serial

    @staticmethod
    def setCameraPitch(angle):
        GlobalContext.getSerial().set_servo_angle(RobotConfig.camera_pitch_servo_id, angle)

    @staticmethod
    def setCameraYaw(angle):
        GlobalContext.getSerial().set_servo_angle(RobotConfig.camera_yaw_servo_id, angle)
