from Geometry.cylinder import Cylinder
import OpenGL.GL as gl
from PyQt5.QtGui import QColor


class CoordinateSystem:
    def __init__(self):
        self.coordinates = []
        self.coordinates.append(Cylinder(0.005, 0.5, QColor.fromRgb(255, 0, 0)))
        self.coordinates.append(Cylinder(0.005, 0.5, QColor.fromRgb(0, 255, 0)))
        self.coordinates.append(Cylinder(0.005, 0.5, QColor.fromRgb(0, 0, 255)))

    def init_object(self):
        for c in self.coordinates:
            c.init_object()

    def draw(self):
        gl.glPushMatrix()

        gl.glPushMatrix()
        # CCW Rotate around y to get x
        gl.glRotated(90, 0.0, 1.0, 0.0)
        self.coordinates[0].draw()
        gl.glPopMatrix()

        # CW Rotate around x to get y
        gl.glPushMatrix()
        gl.glRotated(-90, 1.0, 0.0, 0.0)
        self.coordinates[1].draw()
        gl.glPopMatrix()

        self.coordinates[2].draw()
        gl.glPopMatrix()