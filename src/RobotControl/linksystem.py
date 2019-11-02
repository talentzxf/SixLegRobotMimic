from src.Geometry.cylinder import Cylinder
import OpenGL.GL as gl


class Link(Cylinder):
    radius = 0.01
    next = None
    prev = None
    axis = None
    theta = 0

    def __init__(self, length, axis):
        Cylinder.__init__(self, self.radius, length)
        self.axis = axis

    def setNext(self, next):
        self.next = next

    def setPrev(self, prev):
        self.prev = prev

    def getPrev(self):
        return self.prev

    def getNext(self):
        return self.next

    def setRotateAxis(self, axis):
        self.axis = axis

    def setTheta(self, theta):
        self.theta = theta

    def addTheta(self, gap=1):
        self.theta += gap

    def draw(self):
        if self.prev:
            prev = self.getPrev()
            gl.glTranslated(0.0, 0.0, prev.getLength())

        if self.axis:
            gl.glRotated(self.theta, self.axis[0], self.axis[1], self.axis[2])
        Cylinder.draw(self)

class LinkSystem:
    def __init__(self):
        self.links = []

    def add_link(self, length, axis):
        new_link = Link(length, axis)

        # get the last link
        if len(self.links) > 0:
            last_link = self.links[len(self.links) - 1]
            last_link.setNext(new_link)
            new_link.setPrev(last_link)

        self.links.append(new_link)

    def genObjectList(self):
        for link in self.links:
            link.genObjectList()

    def getLink(self, idx):
        return self.links[idx]

    def draw(self):
        for link in self.links:
            link.draw()