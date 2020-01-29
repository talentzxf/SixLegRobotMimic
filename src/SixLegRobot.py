#!/usr/bin/env python
import traceback

import numpy as np
import sys
import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider,
                             QWidget, QVBoxLayout, QLabel)

import OpenGL.GL as gl

from Geometry.CoordinateSystem import CoordinateSystem

from IKWindow import IKWindow

from GlobalContext import GlobalContext

from Geometry.cylinder import Cylinder

from Geometry import MatrixOps

from GlobalConfig import RobotConfig


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = GLWidget()
        self.legLabels = {}

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.glWidget)

        sliderLayout = QVBoxLayout()

        # 1st row
        self.addSliderRow(sliderLayout, [0, 1])
        self.addSliderRow(sliderLayout, [2, 3])
        self.addSliderRow(sliderLayout, [4, 5])

        mainLayout.addLayout(sliderLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle("Hello GL")
        self.setMinimumSize(1300, 600)

        timer = QTimer(self)
        timer.timeout.connect(self.glWidget.update)
        timer.start(0)

    def addSliderRow(self, outLayout, legNoArray):
        hboxLayout = QHBoxLayout()
        for legNo in legNoArray:
            hboxLayout.addLayout(self.createSliders(legNo))
        outLayout.addLayout(hboxLayout)

    def createSlider(self, minValue, maxValue, dir):
        slider = QSlider(dir)

        slider.setRange(minValue, maxValue)
        slider.setSingleStep(1)
        slider.setPageStep(10)
        slider.setTickInterval(10)
        slider.setTickPosition(QSlider.TicksRight)

        return slider

    def createSliders(self, legNo):
        robot_controller = GlobalContext.getRobot().getController()
        legLabelLayout = QVBoxLayout()
        label = QLabel()
        self.legLabels[legNo] = label
        self.refreshLegLabel(robot_controller, legNo)()
        legLabelLayout.addWidget(label)

        legSliderLayout = QHBoxLayout()

        sliders = [self.createSlider(-90, 90, Qt.Horizontal),
                   self.createSlider(-180, 180, Qt.Vertical),
                   self.createSlider(-180, 180, Qt.Vertical)]

        for idx in range(len(sliders)):
            slider = sliders[idx]
            legSliderLayout.addWidget(slider)

            slider.valueChanged.connect(robot_controller.setLegLinkAngle(legNo, idx))
            slider.valueChanged.connect(self.refreshLegLabel(robot_controller, legNo))

            def setValueOnly(slider):
                def _setValueOnly(value):
                    slider.blockSignals(True)
                    slider.setValue(int(value))
                    slider.blockSignals(False)

                return _setValueOnly

            robot_controller.addValueChangeCallback(legNo, idx, setValueOnly(slider))
            robot_controller.addValueChangeCallback(legNo, idx, self.refreshLegLabel(robot_controller, legNo))

        legLabelLayout.addLayout(legSliderLayout)
        return legLabelLayout

    def refreshLegLabel(self, robot_controller, legNo):
        def refreshLabel():
            label = self.legLabels[legNo]
            label.setText("Leg {} {}".format(legNo, robot_controller.getStatus(legNo)))

        return refreshLabel


class PositionedCylinder(Cylinder):
    def __init__(self, radius, length, color=None, slices=200):
        super().__init__(radius, length, color, slices)
        self.position = [0.0, 0.0, 0.0]

    def setInitPos(self, x, y, z):
        self.position = [x, y, z]

    def draw(self):
        gl.glPushMatrix()
        gl.glTranslated(self.position[0], self.position[1], self.position[2])
        super().draw()
        gl.glPopMatrix()


class InclineIndicator:
    def __init__(self):
        self.indicator = Cylinder(0.15, 10, QColor.fromRgb(255, 0, 255))
        # self.rotation_matrix = np.identity(4)

        self.targetLegEndPoints = []
        # right up
        rightUpCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        rightUpCylinder.setInitPos(RobotConfig.bodyWidth / 2, RobotConfig.bodyLength / 2, 0.0)
        self.targetLegEndPoints.append(rightUpCylinder)

        # right center
        rightCenterCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        rightCenterCylinder.setInitPos(RobotConfig.bodyWidth / 2, 0, 0.0)
        self.targetLegEndPoints.append(rightCenterCylinder)

        # right down
        rightDownCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        rightDownCylinder.setInitPos(RobotConfig.bodyWidth / 2, -RobotConfig.bodyLength / 2, 0.0)
        self.targetLegEndPoints.append(rightDownCylinder)

        # Left up
        leftUpCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        leftUpCylinder.setInitPos(-RobotConfig.bodyWidth / 2, RobotConfig.bodyLength / 2, 0.0)
        self.targetLegEndPoints.append(leftUpCylinder)

        # left center
        leftCenterCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        leftCenterCylinder.setInitPos(-RobotConfig.bodyWidth / 2, 0, 0.0)
        self.targetLegEndPoints.append(leftCenterCylinder)

        # Left down
        leftDownCylinder = PositionedCylinder(0.15, 0.5, QColor.fromRgb(0, 255, 255))
        leftDownCylinder.setInitPos(-RobotConfig.bodyWidth / 2, -RobotConfig.bodyLength / 2, 0.0)
        self.targetLegEndPoints.append(leftDownCylinder)

        self.rotation_matrix = MatrixOps.rotate_matrix(0.5750981,
                                                       [-0.2080853 * 180 / math.pi, -0.19589223 * 180 / math.pi,
                                                        -0.7665436 * 180 / math.pi])

    def incline(self, theta, axis):
        self.rotation_matrix = MatrixOps.rotate_matrix(theta, axis)

    def init_object(self):
        self.indicator.init_object()
        for endPoint in self.targetLegEndPoints:
            endPoint.init_object()

    def draw(self):
        gl.glPushMatrix()
        gl.glMultMatrixd(self.rotation_matrix)
        self.indicator.draw()
        # draw six leg new end points
        for endPoint in self.targetLegEndPoints:
            endPoint.draw()
        gl.glPopMatrix()




class GLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.xRot = 120
        self.yRot = 0
        self.zRot = -70

        self.lastPos = QPoint()
        self.bg_color = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

        self.coordinates = CoordinateSystem()

        self.inclineIndicator = InclineIndicator()

    def getOpenglInfo(self):
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
        """.format(
            gl.glGetString(gl.GL_VENDOR),
            gl.glGetString(gl.GL_RENDERER),
            gl.glGetString(gl.GL_VERSION),
            gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
        )

        return info

    def minimumSizeHint(self):
        return QSize(800, 600)

    def maxSizeHint(self):
        return QSize(800, 600)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.update()

    def initializeGL(self):
        print(self.getOpenglInfo())

        gl.glClearColor(self.bg_color.redF(), self.bg_color.greenF(), self.bg_color.blueF(), self.bg_color.alphaF())
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glEnable(gl.GL_DEPTH_TEST)

        self.enableLightAndMaterial()
        gl.glEnable(gl.GL_DEPTH_TEST)

        GlobalContext.getRobot().initRobot()
        self.coordinates.init_object()

        self.inclineIndicator.init_object()

    def enableLightAndMaterial(self):
        flashLightPos = [10.0, 10.0, 0.0]
        flashLightColor = [0.2, 0.2, 0.2]

        gl.glLightModeli(gl.GL_LIGHT_MODEL_TWO_SIDE, gl.GL_TRUE)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, flashLightPos)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, flashLightColor)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, flashLightColor)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, flashLightColor)

        # set up cube's material
        cubeColor = [0.6, 0.7, 1.0]
        cubeSpecular = [1.0, 1.0, 1.0]
        gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE, cubeColor)
        gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, cubeSpecular)
        gl.glMaterialf(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 10.0)

    def paintGL(self):
        gl.glClear(
            gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -10.0)
        gl.glRotated(self.xRot, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot, 0.0, 0.0, 1.0)
        self.coordinates.draw()
        GlobalContext.getRobot().draw()
        self.inclineIndicator.draw()

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport((width - side) // 2, (height - side) // 2, side,
                      side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-5, +5, +5, -5, 50.0, -50.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle


if __name__ == '__main__':
    try:
        RobotConfig.enable_serial = False
        app = QApplication(sys.argv)
        window = Window()
        window.show()

        ikWindow = IKWindow()
        ikWindow.show()
    except Exception as e:
        print(e)

    sys.exit(app.exec_())
