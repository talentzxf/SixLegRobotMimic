#!/usr/bin/env python


import numpy as np
import sys
import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider,
                             QWidget, QVBoxLayout)

import OpenGL.GL as gl

from Geometry.CoordinateSystem import CoordinateSystem
from Geometry.cylinder import Cylinder
from RobotControl.robotmodel import RobotModel

from Geometry.cube import Cube


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = GLWidget()

        # self.xSlider.valueChanged.connect(self.glWidget.setXRotation)
        # self.glWidget.xRotationChanged.connect(self.xSlider.setValue)
        # self.ySlider.valueChanged.connect(self.glWidget.setYRotation)
        # self.glWidget.yRotationChanged.connect(self.ySlider.setValue)
        # self.zSlider.valueChanged.connect(self.glWidget.setZRotation)
        # self.glWidget.zRotationChanged.connect(self.zSlider.setValue)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.glWidget)

        sliderLayout = QVBoxLayout()

        # 1st row
        firstRowLayout = QHBoxLayout()
        self.leg1Sliders = self.createSliders()
        firstRowLayout.addLayout(self.leg1Sliders)
        self.leg2Sliders = self.createSliders()
        firstRowLayout.addLayout(self.leg2Sliders)
        sliderLayout.addLayout(firstRowLayout)

        # 2nd row
        secondRowLayout = QHBoxLayout()
        self.leg3Sliders = self.createSliders()
        secondRowLayout.addLayout(self.leg3Sliders)
        self.leg4Sliders = self.createSliders()
        secondRowLayout.addLayout(self.leg4Sliders)

        sliderLayout.addLayout(secondRowLayout)

        # 3rd row
        # 2nd row
        thirdRowLayout = QHBoxLayout()
        self.leg5Sliders = self.createSliders()
        thirdRowLayout.addLayout(self.leg5Sliders)
        self.leg6Sliders = self.createSliders()
        thirdRowLayout.addLayout(self.leg6Sliders)

        sliderLayout.addLayout(thirdRowLayout)

        mainLayout.addLayout(sliderLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle("Hello GL")

        timer = QTimer(self)
        timer.timeout.connect(self.glWidget.update)
        timer.start(0)

    def createSlider(self, minValue, maxValue, dir):
        slider = QSlider(dir)

        slider.setRange(-45, 45)
        slider.setSingleStep(1)
        slider.setPageStep(10)
        slider.setTickInterval(10)
        slider.setTickPosition(QSlider.TicksRight)

        return slider

    def createSliders(self):
        legSliderLayout = QHBoxLayout()
        link1Slider = self.createSlider(-45, 45, Qt.Horizontal)
        link2Slider = self.createSlider(-45, 45, Qt.Vertical)
        link3Slider = self.createSlider(-45, 45, Qt.Vertical)
        legSliderLayout.addWidget(link1Slider)
        legSliderLayout.addWidget(link2Slider)
        legSliderLayout.addWidget(link3Slider)
        return legSliderLayout


class GLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        # self.base = Cylinder(0.1, 0.01)
        self.base = Cube(0.2, 0.2, 0.1)
        self.xRot = 70
        self.yRot = 0
        self.zRot = 70

        self.lastPos = QPoint()
        self.bg_color = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

        self.robot = RobotModel()
        self.coordinates = CoordinateSystem()

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
        return QSize(1024, 768)

    def sizeHint(self):
        return QSize(1024, 1024)

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
        self.base.genObjectList()

        self.robot.initRobot()
        self.coordinates.init()

    def enableLightAndMaterial(self):
        flashLightPos = [10.0, 10.0, 0.0]
        flashLightDir = [0.0, 0.0, -1.0]
        flashLightColor = [0.2, 0.2, 0.2]

        gl.glLightModeli(gl.GL_LIGHT_MODEL_TWO_SIDE, gl.GL_TRUE)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, flashLightPos)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, flashLightColor)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, flashLightColor)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, flashLightColor)
        # gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPOT_DIRECTION, flashLightDir)
        # gl.glLightf(gl.GL_LIGHT0, gl.GL_SPOT_CUTOFF, 12.0)

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
        self.base.draw()
        self.robot.draw()

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport((width - side) // 2, (height - side) // 2, side,
                      side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
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
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
