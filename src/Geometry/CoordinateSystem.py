from src.Geometry.cylinder import Cylinder
import OpenGL.GL as gl

class CoordinateSystem:
    def __init__(self):
        self.coordinates = []
        self.coordinates.append(Cylinder(0.005, 0.5))
        self.coordinates.append(Cylinder(0.005, 0.5))
        self.coordinates.append(Cylinder(0.005, 0.5))

    def init(self):
        for c in self.coordinates:
            c.genObjectList()

    def draw(self):
        gl.glPushMatrix()

        gl.glPushMatrix()
        # Rotate around y to get x
        gl.glRotated(90, 0.0, 1.0, 0.0)
        self.coordinates[0].draw()
        gl.glPopMatrix()

        # Rotate around x to get y
        gl.glPushMatrix()
        gl.glRotated(90, 1.0, 0.0, 0.0)
        self.coordinates[1].draw()
        gl.glPopMatrix()

        self.coordinates[2].draw()
        gl.glPopMatrix()