from RobotControl.robotmodel import RobotModel


class GlobalContext:
    robot = None

    @staticmethod
    def getRobot():
        if GlobalContext.robot is None:
            GlobalContext.robot = RobotModel()
        return GlobalContext.robot