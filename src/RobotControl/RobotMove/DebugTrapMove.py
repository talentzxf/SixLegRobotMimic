from RobotControl.RobotMove.RobotMove import RobotMove


class DebugTrapMove(RobotMove):
    triggerTrap = False

    def __init__(self, legs=None, allLegsHeight=0, leg_init_stretch=0.3, ):
        super().__init__(legs, allLegsHeight, leg_init_stretch)
        self.hasTriggered = False

    def hasTriggered(self):
        return self.hasTriggered()

    def go(self):
        if DebugTrapMove.triggerTrap:
            DebugTrapMove.triggerTrap = False
            self.hasTriggered = True
            return super().go()

        return False  # Do nothing
