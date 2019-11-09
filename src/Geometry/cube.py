import math
import OpenGL.GL as gl
from PyQt5.QtGui import QColor


class Cube:
    def __init__(self, length, width, height, face_color=None, slices=200):
        self.upper_face = []
        self.bottom_face = []
        self.left_face = []
        self.right_face = []
        self.front_face = []
        self.back_face = []

        if face_color is None:
            self.face_color = QColor.fromRgb(127, 127, 127)
        else:
            self.face_color = face_color

        self.display_list = 0
        self.length = length
        self.width = width
        self.height = height

        # Bottom face
        self.bottom_face.append([-width / 2, length / 2, 0, self.face_color])
        self.bottom_face.append([-width / 2, -length / 2, 0, self.face_color])
        self.bottom_face.append([width / 2, -length / 2, 0, self.face_color])
        self.bottom_face.append([width / 2, length / 2, 0, self.face_color])

        # Upper face
        self.upper_face.append([-width / 2, length / 2, height, self.face_color])
        self.upper_face.append([-width / 2, -length / 2, height, self.face_color])
        self.upper_face.append([width / 2, -length / 2, height, self.face_color])
        self.upper_face.append([width / 2, length / 2, height, self.face_color])

        # Left face
        self.left_face.append([width / 2, -length / 2, 0, self.face_color])
        self.left_face.append([width / 2, -length / 2, height, self.face_color])
        self.left_face.append([width / 2, length / 2, height, self.face_color])
        self.left_face.append([width / 2, length / 2, 0, self.face_color])

        # Right face
        self.left_face.append([-width / 2, -length / 2, 0, self.face_color])
        self.left_face.append([-width / 2, -length / 2, height, self.face_color])
        self.left_face.append([-width / 2, length / 2, height, self.face_color])
        self.left_face.append([-width / 2, length / 2, 0, self.face_color])

        # Front face
        self.front_face.append([-width / 2, length / 2, 0, self.face_color])
        self.front_face.append([-width / 2, length / 2, height, self.face_color])
        self.front_face.append([width / 2, length / 2, height, self.face_color])
        self.front_face.append([width / 2, length / 2, 0, self.face_color])

        # Back face
        self.back_face.append([-width / 2, -length / 2, 0, self.face_color])
        self.back_face.append([-width / 2, -length / 2, height, self.face_color])
        self.back_face.append([width / 2, -length / 2, height, self.face_color])
        self.back_face.append([width / 2, -length / 2, 0, self.face_color])

    def getLength(self):
        return self.length

    def init_object(self):
        display_list = gl.glGenLists(1)
        gl.glNewList(display_list, gl.GL_COMPILE)

        # Upper face
        gl.glBegin(gl.GL_QUADS)
        gl.glNormal3f(0.0, 1.0, 0.0)
        for vertex in self.upper_face:
            self.set_vertex(vertex)
        gl.glEnd()

        # Lower face
        gl.glBegin(gl.GL_QUADS)
        gl.glNormal3f(0.0, -1.0, 0.0)
        for vertex in self.bottom_face:
            self.set_vertex(vertex)
        gl.glEnd()

        # Left face
        gl.glBegin(gl.GL_QUADS)
        gl.glNormal3f(1.0, 0.0, 0.0)
        for vertex in self.left_face:
            self.set_vertex(vertex)
        gl.glEnd()

        # Left face
        gl.glBegin(gl.GL_QUADS)
        gl.glNormal3f(-1.0, 0.0, 0.0)
        for vertex in self.right_face:
            self.set_vertex(vertex)
        gl.glEnd()

        # Front face
        gl.glBegin(gl.GL_QUADS)
        gl.glNormal3f(0.0, -1.0, 0.0)
        for vertex in self.front_face:
            self.set_vertex(vertex)
        gl.glEnd()

        # Front face
        gl.glBegin(gl.GL_QUADS)
        gl.glNormal3f(0.0, 1.0, 0.0)
        for vertex in self.back_face:
            self.set_vertex(vertex)
        gl.glEnd()
        gl.glEndList()

        self.display_list = display_list

    @staticmethod
    def set_vertex(v):
        # set up cube's material
        cubeColor = [v[3].redF(), v[3].greenF(), v[3].blueF(), v[3].alphaF()]
        cubeSpecular = [1.0, 1.0, 1.0]
        gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE, cubeColor)
        gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, cubeSpecular)
        gl.glMaterialf(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 10.0)
        gl.glVertex3d(v[0], v[1], v[2])

    def draw(self):
        gl.glCallList(self.display_list)
