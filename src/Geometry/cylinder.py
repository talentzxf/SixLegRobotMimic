import math
import OpenGL.GL as gl
from PyQt5.QtGui import QColor


class Cylinder:
    def __init__(self, radius, height, slices):
        self.upper_face = []  # Triangle Fan
        self.lower_face = []  # Triangle Fan
        self.wall = []  # Quads
        self.face_color = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.wall_color = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)
        self.upper_face.append([0, 0, height / 2, self.face_color])
        self.lower_face.append([0, 0, -height / 2, self.face_color])

        self.display_list = 0

        for i in range(slices+1):
            angle = (i * 2 * math.pi) / slices
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.lower_face.append([x, y, -height / 2, self.face_color])
            self.upper_face.append([x, y, height / 2, self.face_color])

            angle2 = ((i + 1) * 2 * math.pi) / slices  # next angle
            x2 = radius * math.cos(angle2)
            y2 = radius * math.sin(angle2)
            self.wall.append([x, y, height / 2, self.face_color])
            self.wall.append([x, y, -height / 2, self.face_color])
            self.wall.append([x2, y2, -height / 2, self.face_color])
            self.wall.append([x2, y2, height / 2, self.face_color])

    def genObjectList(self):
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
        gl.glBegin(gl.GL_QUADS)
        for vertex in self.wall:
            self.set_vertex(vertex)
        gl.glEnd()
        gl.glEndList()

        self.display_list = display_list

    @staticmethod
    def set_vertex(v):
        # gl.glColor4f(v[3].redF(), v[3].greenF(), v[3].blueF(), v[3].alphaF())
        gl.glVertex3d(v[0], v[1], v[2])

    def draw(self):
        gl.glCallList(self.display_list)
