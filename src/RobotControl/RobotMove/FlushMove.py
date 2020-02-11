from GlobalConfig import RobotConfig
from GlobalContext import GlobalContext
from RobotControl.RobotMove.AbstractTrajectory import AbstractTrajectory


class FlushMove(AbstractTrajectory):
    def _go(self):
        GlobalContext.getSerial().flush()
        # import time
        # time.sleep(0.1)
        return False # Always propagate

