import math
import OpenGL.GL as gl
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QColor


class Cylinder(QObject):
    def __init__(self, radius, length, color=None, slices=200):
        super().__init__()
        self.upper_face = []  # Triangle Fan
        self.lower_face = []  # Triangle Fan
        self.wall = []  # Quads

        if color is None:
            self.color = QColor.fromRgb(127, 127, 127)
        else:
            self.color = color

        self.upper_face.append([0, 0, length])
        self.lower_face.append([0, 0, 0])

        self.display_list = 0
        self.length = length

        for i in range(slices + 1):
            angle = (i * 2 * math.pi) / slices
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.lower_face.append([x, y, 0])
            self.upper_face.append([x, y, length])

            angle2 = ((i + 1) * 2 * math.pi) / slices  # next angle
            x2 = radius * math.cos(angle2)
            y2 = radius * math.sin(angle2)
            self.wall.append([x, y, length])
            self.wall.append([x, y, 0])
            self.wall.append([x2, y2, 0])
            self.wall.append([x2, y2, length])

    def getLength(self):
        return self.length

    def init_object(self):
        display_list = gl.glGenLists(1)
        gl.glNewList(display_list, gl.GL_COMPILE)

        # Upper face
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glNormal3f(0.0, 1.0, 0.0)
        for vertex in self.upper_face:
            self.set_vertex(vertex)
        gl.glEnd()

        # Lower face
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glNormal3f(0.0, -1.0, 0.0)
        for vertex in self.lower_face:
            self.set_vertex(vertex)
        gl.glEnd()

        # Walls
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        for vertex in self.wall:
            self.set_vertex(vertex)
        gl.glEnd()
        gl.glEndList()

        self.display_list = display_list

    def set_vertex(self, v):
        # set up cube's material
        cubeColor = [self.color.redF(), self.color.greenF(), self.color.blueF(), self.color.alphaF()]
        cubeSpecular = [1.0, 1.0, 1.0]
        gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE, cubeColor)
        gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, cubeSpecular)
        gl.glMaterialf(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 10.0)
        gl.glVertex3d(v[0], v[1], v[2])

    def set_color(self, new_color):
        self.color = new_color

    def draw(self):
        gl.glCallList(self.display_list)
