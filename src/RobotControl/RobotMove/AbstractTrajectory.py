class AbstractTrajectory:  # Responsible chain
    def __init__(self):
        self.next = None

    def setNext(self, nextTrajectory):
        self.next = nextTrajectory

    def getLastTrajectory(self):
        if self.next:
            return self.next.getLastTrajectory()
        else:
            return self

    def go(self):
        if self._go():
            return True
        else:
            return False if self.next is None else self.next._go()
