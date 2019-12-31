from Geometry.MatrixOps import translate_matrix, rotate_matrix
from Geometry.cylinder import Cylinder
import OpenGL.GL as gl
import numpy as np

from Geometry.CoordinateSystem import CoordinateSystem
from PyQt5.QtCore import pyqtSignal

from GlobalConfig import RobotConfig


class Link(Cylinder):
    angleChanged = pyqtSignal(float)

    radius = RobotConfig.linkRadius
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
        self.angleChanged.emit(self.theta)

    def getTheta(self):
        return self.theta

    def addTheta(self, gap=1):
        self.theta += gap

    # if realDraw = False, we just want to know the target position
    def draw(self, realDraw=True):
        model_matrix = np.identity(4)
        if self.prev:
            prev = self.getPrev()
            if realDraw:
                gl.glTranslated(0.0, 0.0, prev.getLength())
            model_matrix = np.matmul(model_matrix, translate_matrix(0.0, 0.0, prev.getLength()))

        if self.axis:
            if realDraw:
                gl.glRotated(self.theta, self.axis[0], self.axis[1], self.axis[2])
            model_matrix = np.matmul(model_matrix, rotate_matrix(self.theta, self.axis))
        if realDraw:
            Cylinder.draw(self)
        return model_matrix


class LinkSystem:
    def __init__(self, pos=None, rotate=None):
        self.links = []
        self.cylinder = Cylinder(0.02, 0.02)
        self.init_pos = pos
        self.init_rotates = rotate  # Remember, in reverse order because of matrix multiplication order ~~~

        self.draw_coordinate = False
        self.coordinate = CoordinateSystem()

        self.targetModelMatrix = np.identity(4)

    def getSolver(self):
        return self.solver

    def add_link(self, length, axis):
        new_link = Link(length, axis)

        # get the last link
        if len(self.links) > 0:
            last_link = self.links[len(self.links) - 1]
            last_link.setNext(new_link)
            new_link.setPrev(last_link)

        self.links.append(new_link)

    def get_start_pos(self):
        return self.init_pos

    def get_init_transformation_matrix(self):
        model_matrix = np.identity(4)
        if self.init_pos:
            model_matrix = np.matmul(model_matrix,
                                     translate_matrix(self.init_pos[0], self.init_pos[1], self.init_pos[2]))

        if self.init_rotates:
            for rotate in self.init_rotates:
                model_matrix = np.matmul(model_matrix, rotate_matrix(rotate[0], [rotate[1], rotate[2], rotate[3]]))

        return model_matrix

    # World Coordinate
    def get_target_pos(self):
        model_matrix = self.get_init_transformation_matrix()

        for link in self.links:
            cur_model_matrix = link.draw(False)
            model_matrix = np.matmul(model_matrix, cur_model_matrix)

        # move along last link
        model_matrix = np.matmul(model_matrix, translate_matrix(0.0, 0.0, self.links[len(self.links) - 1].getLength()))
        return model_matrix[:, 3]

    def init_object(self):
        for link in self.links:
            link.init_object()
        self.cylinder.init_object()
        self.coordinate.init_object()

    def set_color(self, new_color):
        for link in self.links:
            link.set_color(new_color)

    def setDrawCoordinate(self, isDrawCoordinate):
        self.draw_coordinate = isDrawCoordinate

    def draw(self):
        if self.init_pos:
            gl.glTranslated(self.init_pos[0], self.init_pos[1], self.init_pos[2])

        if self.init_rotates:
            for rotate in self.init_rotates:
                gl.glRotated(rotate[0], rotate[1], rotate[2], rotate[3])

        if self.draw_coordinate:
            self.coordinate.draw()

        gl.glPushMatrix()
        self.targetModelMatrix = np.identity(4)
        for link in self.links:
            cur_model_matrix = link.draw()
            self.targetModelMatrix = np.matmul(self.targetModelMatrix, cur_model_matrix)
        gl.glPopMatrix()
        # Draw a cone at the destination
        # translate to the end of the last joint
        self.targetModelMatrix = np.matmul(self.targetModelMatrix,
                                           translate_matrix(0.0, 0.0, self.links[len(self.links) - 1].getLength()))
        gl.glMultTransposeMatrixd(self.targetModelMatrix.tolist())
        self.cylinder.draw()
