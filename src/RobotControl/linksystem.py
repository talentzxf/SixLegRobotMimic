from src.Geometry.MatrixOps import translate_matrix, rotate_matrix
from src.Geometry.cylinder import Cylinder
import OpenGL.GL as gl
import numpy as np


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
        model_matrix = np.identity(4)
        if self.prev:
            prev = self.getPrev()
            gl.glTranslated(0.0, 0.0, prev.getLength())
            model_matrix = np.matmul(translate_matrix(0.0, 0.0, prev.getLength()), model_matrix)

        if self.axis:
            gl.glRotated(self.theta, self.axis[0], self.axis[1], self.axis[2])
            model_matrix = np.matmul(rotate_matrix(self.theta, self.axis), model_matrix)
        Cylinder.draw(self)
        return model_matrix


class LinkSystem:
    def __init__(self):
        self.links = []
        self.cylinder = Cylinder(0.02, 0.02)

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
        self.cylinder.genObjectList()

    def getLink(self, idx):
        return self.links[idx]

    def draw(self):
        gl.glPushMatrix()
        model_matrix = np.identity(4)
        # for link in self.links:
        #     cur_model_matrix = link.draw()
        #     model_matrix = np.matmul(cur_model_matrix, model_matrix)
        model_matrix_1 = self.links[0].draw()
        model_matrix_2 = self.links[1].draw()
        model_matrix_3 = self.links[2].draw()
        model_matrix = np.matmul(model_matrix_1, model_matrix)
        model_matrix = np.matmul(model_matrix_2, model_matrix)
        model_matrix = np.matmul(model_matrix_3, model_matrix)
        print(model_matrix)
        gl.glPopMatrix()
        # Draw a cone at the destination
        gl.glMultTransposeMatrixd(model_matrix.tolist())
        self.cylinder.draw()
