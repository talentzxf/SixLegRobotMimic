from Geometry.MatrixOps import translate_matrix, rotate_matrix
from Geometry.cylinder import Cylinder
import OpenGL.GL as gl
import numpy as np

from Geometry.CoordinateSystem import CoordinateSystem

from IKSolver.Solver import IKSolver


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

    def getTheta(self):
        return self.theta

    def addTheta(self, gap=1):
        self.theta += gap

    # if realDraw = False, we just want to know the target position
    def draw(self, realDraw=True):
        model_matrix = np.identity(4)
        if self.prev:
            prev = self.getPrev()
            gl.glTranslated(0.0, 0.0, prev.getLength())
            model_matrix = np.matmul(model_matrix, translate_matrix(0.0, 0.0, prev.getLength()))

        if self.axis:
            gl.glRotated(self.theta, self.axis[0], self.axis[1], self.axis[2])
            model_matrix = np.matmul(model_matrix, rotate_matrix(self.theta, self.axis))
        Cylinder.draw(self)
        return model_matrix


class LinkSystem:
    def __init__(self, pos=None, rotate=None):
        self.links = []
        self.cylinder = Cylinder(0.02, 0.02)
        self.init_pos = pos
        self.init_rotates = rotate  # Remember, in reverse order because of matrix multiplication order ~~~

        self.coordinate = CoordinateSystem()

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

    def get_target_pos(self):
        model_matrix = self.get_init_transformation_matrix()

        for link in self.links:
            cur_model_matrix = link.draw(False)
            model_matrix = np.matmul(model_matrix, cur_model_matrix)
        return model_matrix[:, 3]

    def init_object(self):
        for link in self.links:
            link.init_object()
        self.cylinder.init_object()
        self.coordinate.init_object()

    def get_link(self, idx):
        return self.links[idx]

    def get_link_number(self):
        return len(self.links)

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

        self.coordinate.draw()
        gl.glPushMatrix()
        model_matrix = np.identity(4)
        for link in self.links:
            cur_model_matrix = link.draw()
            model_matrix = np.matmul(model_matrix, cur_model_matrix)
        # print(model_matrix)
        gl.glPopMatrix()
        # Draw a cone at the destination
        # translate to the end of the last joint

        gl.glMultTransposeMatrixd(model_matrix.tolist())
        self.cylinder.draw()


from Geometry.MatrixOps import translate_matrix, rotate_matrix
from Geometry.cylinder import Cylinder
import OpenGL.GL as gl
import numpy as np

from Geometry.CoordinateSystem import CoordinateSystem


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

    def getTheta(self):
        return self.theta

    def addTheta(self, gap=1):
        self.theta += gap

    # if realDraw = False, we just want to know the target position
    def draw(self, realDraw=True):
        model_matrix = np.identity(4)
        if self.prev:
            prev = self.getPrev()
            gl.glTranslated(0.0, 0.0, prev.getLength())
            model_matrix = np.matmul(model_matrix, translate_matrix(0.0, 0.0, prev.getLength()))

        if self.axis:
            gl.glRotated(self.theta, self.axis[0], self.axis[1], self.axis[2])
            model_matrix = np.matmul(model_matrix, rotate_matrix(self.theta, self.axis))
        Cylinder.draw(self)
        return model_matrix


# TODO: inherit a leg class from LinkSystem
class LinkSystem:
    def __init__(self, pos=None, rotate=None, name=None):
        self.links = []
        self.cylinder = Cylinder(0.02, 0.02)
        self.init_pos = pos
        self.init_rotates = rotate  # Remember, in reverse order because of matrix multiplication order ~~~

        self.draw_coordinate = False
        self.coordinate = CoordinateSystem()
        self.name = name
        self.link_length_array = []
        self.start_angles = []
        self.solver = IKSolver(self.link_length_array, self.start_angles)

    def getSolver(self):
        return self.solver

    def getName(self):
        return self.name

    def add_link(self, length, axis):
        self.link_length_array.append(length)
        self.start_angles.append(0)
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

    def get_target_pos(self):
        model_matrix = self.get_init_transformation_matrix()

        for link in self.links:
            cur_model_matrix = link.draw(False)
            model_matrix = np.matmul(model_matrix, cur_model_matrix)
        return model_matrix[:, 3]

    def init_object(self):
        for link in self.links:
            link.init_object()
        self.cylinder.init_object()
        self.coordinate.init_object()

    def get_link(self, idx):
        return self.links[idx]

    def get_link_number(self):
        return len(self.links)

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
        model_matrix = np.identity(4)
        for link in self.links:
            cur_model_matrix = link.draw()
            model_matrix = np.matmul(model_matrix, cur_model_matrix)
        # print(model_matrix)
        gl.glPopMatrix()
        # Draw a cone at the destination
        # translate to the end of the last joint
        gl.glMultTransposeMatrixd(model_matrix.tolist())
        self.cylinder.draw()
