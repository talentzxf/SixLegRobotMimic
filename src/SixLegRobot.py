#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2015 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,
## DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import sys
import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider,
                             QWidget)

import OpenGL.GL as gl

from src.Geometry.cylinder import Cylinder
from src.RobotControl.linksystem import LinkSystem


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = GLWidget()

        self.xSlider = self.createSlider()
        self.ySlider = self.createSlider()
        self.zSlider = self.createSlider()

        # self.xSlider.valueChanged.connect(self.glWidget.setXRotation)
        # self.glWidget.xRotationChanged.connect(self.xSlider.setValue)
        # self.ySlider.valueChanged.connect(self.glWidget.setYRotation)
        # self.glWidget.yRotationChanged.connect(self.ySlider.setValue)
        # self.zSlider.valueChanged.connect(self.glWidget.setZRotation)
        # self.glWidget.zRotationChanged.connect(self.zSlider.setValue)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.glWidget)
        mainLayout.addWidget(self.xSlider)
        mainLayout.addWidget(self.ySlider)
        mainLayout.addWidget(self.zSlider)
        self.setLayout(mainLayout)

        self.setWindowTitle("Hello GL")

        timer = QTimer(self)
        timer.timeout.connect(self.glWidget.update)
        timer.start(0)

    def createSlider(self):
        slider = QSlider(Qt.Vertical)

        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QSlider.TicksRight)

        return slider


class GLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.base = Cylinder(0.1, 0.01, 200)
        self.xRot = 70
        self.yRot = 0
        self.zRot = 70

        self.lastPos = QPoint()
        self.bg_color = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

        self.links = LinkSystem()
        self.links.add_link(0.3, [0.0, 0.0, 1.0])
        self.links.add_link(0.4, [1.0, 0.0, 0.0])
        self.links.add_link(0.5, [1.0, 0.0, 0.0])
        self.links.add_link(0.6, [1.0, 0.0, 0.0])

        # self.links.getLink(0).setTheta(90)
        self.links.getLink(1).setTheta(90)
        self.links.getLink(2).setTheta(90)
        self.links.getLink(3).setTheta(90)


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
        return QSize(50, 50)

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
        self.links.genObjectList()

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

        # gl.glTranslated(-0.3, 0.3, -10.0)
        gl.glTranslated(0.0, 0.0, -10.0)
        gl.glRotated(self.xRot, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot, 0.0, 0.0, 1.0)
        self.base.draw()
        self.links.draw()
        self.links.getLink(0).addTheta()

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
