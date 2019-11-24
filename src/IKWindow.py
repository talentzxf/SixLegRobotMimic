import math

from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QSlider, QPushButton)
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QColor, QFont

from GlobalContext import GlobalContext
from PyQt5.QtCore import Qt, QRect, QPoint, QSize

from GlobalConfig import RobotConfig
from Geometry.CoordinateConverter import CoordinateConverter


class IKWindow(QWidget):
    def __init__(self):
        super(IKWindow, self).__init__()
        mainLayout = QHBoxLayout()
        tabWidget = MyTableWidget(self)
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout()

        # Initialize tab screen
        self.tabs = QTabWidget()

        # Add tabs
        self.tabs.addTab(self.initTab1(), "IK control")
        self.tabs.addTab(self.initTab2(), "Global control")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.prevSelectedRect = None

    # TODO: better naming
    def initTab1(self):
        slider = QSlider(Qt.Vertical)
        slider.setRange(-30, 30)
        slider.setSingleStep(1)
        slider.setPageStep(10)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksRight)

        self.heightSlider = slider
        tab = QWidget()
        # Create first tab
        tab.layout = QHBoxLayout()

        ikWidget = IKWidget()
        tab.layout.addWidget(ikWidget)
        tab.layout.addWidget(self.heightSlider)
        tab.setLayout(tab.layout)
        ikWidget.legSelected.connect(self.legSelected)
        self.ikWidget = ikWidget

        self.heightSlider.hide()
        return tab

    def legSelected(self, draggableRect):
        try:
            self.heightSlider.valueChanged.disconnect()
        except Exception:
            pass
        self.heightSlider.valueChanged.connect(self.ikWidget.update)

        if draggableRect:
            self.heightSlider.setValue(draggableRect.getZ() * 100.0)
            self.heightSlider.show()
            self.heightSlider.valueChanged.connect(self.setZ(draggableRect))
        else:
            self.heightSlider.setValue(0)
            self.heightSlider.hide()

    def setZ(self, draggableRect):
        def _setZ(z):
            draggableRect.setZ(z / 10.0)

        return _setZ

    def initTab2(self):
        tab = QWidget()
        vboxlayout = QVBoxLayout()
        button = QPushButton("Reset position")
        button.clicked.connect(self.resetRobotPos)
        vboxlayout.addWidget(button)

        goButton = QPushButton("Forward")
        vboxlayout.addWidget(goButton)
        goButton.clicked.connect(self.robotGo)

        stopButton = QPushButton("Stop")
        vboxlayout.addWidget(stopButton)
        stopButton.clicked.connect(self.robotStop)

        leftButton = QPushButton("Left")
        vboxlayout.addWidget(leftButton)
        leftButton.clicked.connect(self.robotLeft)

        rightButton = QPushButton("Right")
        vboxlayout.addWidget(rightButton)
        rightButton.clicked.connect(self.robotRight)

        hboxLayout = QHBoxLayout()
        zslider = QSlider(Qt.Vertical)
        zslider.setRange(-30, 30)
        zslider.setSingleStep(1)
        zslider.setPageStep(10)
        zslider.setTickInterval(1)
        zslider.setTickPosition(QSlider.TicksRight)
        zslider.valueChanged.connect(self.globalZChanged)

        hboxLayout.addWidget(zslider)
        vboxlayout.addLayout(hboxLayout)

        tab.setLayout(vboxlayout)

        return tab

    def globalZChanged(self, newValue):
        GlobalContext.getRobot().getController().setLegHeight(newValue/10)
        GlobalContext.getRobot().getController().resetPos()

    def resetRobotPos(self):
        GlobalContext.getRobot().getController().resetPos()

    def robotGo(self):
        GlobalContext.getRobot().getController().robotGo()

    def robotStop(self):
        GlobalContext.getRobot().getController().robotStop()

    def robotLeft(self):
        GlobalContext.getRobot().getController().robotLeft()

    def robotRight(self):
        GlobalContext.getRobot().getController().robotRight()

# Everything in this class happens in Screen coordinate
class DraggableRect(QObject):
    valueChanged = pyqtSignal()
    size = QSize(10, 10)

    # leg means this rect corresponds to which leg.
    def __init__(self, pos, z, leg):
        QObject.__init__(self)
        adjusted_pos = QPoint(pos.x() - self.size.width() / 2, pos.y() - self.size.height() / 2)
        self.pos = adjusted_pos
        self.rect = QRect(adjusted_pos, self.size)
        self.leg = leg
        self.coord = CoordinateConverter()
        self.z = z  # z is the z coordinate of the leg in world space

    def setZ(self, z):
        self.z = z
        self.valueChanged.emit()

    def getZ(self):
        return self.z

    def getLeg(self):
        return self.leg

    def setPos(self, pos):
        adjusted_pos = QPoint(pos.x() - self.size.width() / 2, pos.y() - self.size.height() / 2)
        self.pos = adjusted_pos
        self.rect = QRect(adjusted_pos, self.size)

    def getPos(self):
        return self.pos

    def draw(self, qp, selected=False):
        old_pen = qp.pen()
        if selected:
            qp.setBrush(QColor(0, 0, 127))
        else:
            qp.setBrush(QColor(127, 127, 127))
        qp.drawRect(self.rect)

        if selected:
            color = QColor(0, 0, 0)
            color.setNamedColor('#ff0000')
            qp.setPen(color)
            # draw the local coordinate of the leg
            leg_start_point = self.leg.get_start_pos()
            leg_scr_position = self.coord.worldToScr(leg_start_point[0], leg_start_point[1])
            # Local x coordinate
            worldPosX = self.coord.objectToWorld([1, 0, 0], self.leg.get_init_transformation_matrix())
            scrPosX = self.coord.worldToScr(worldPosX[0], worldPosX[1])

            qp.drawLine(leg_scr_position, scrPosX)
            # Local y coordinate
            color.setNamedColor('#00ff00')
            qp.setPen(color)
            worldPosY = self.coord.objectToWorld([0, 1, 0], self.leg.get_init_transformation_matrix())
            scrPosY = self.coord.worldToScr(worldPosY[0], worldPosY[1])
            qp.drawLine(leg_scr_position, scrPosY)

            # Local z coordinate
            color.setNamedColor('#0000ff')
            qp.setPen(color)
            worldPosZ = self.coord.objectToWorld([0, 0, 1], self.leg.get_init_transformation_matrix())
            scrPosZ = self.coord.worldToScr(worldPosZ[0], worldPosZ[1])
            qp.drawLine(leg_scr_position, scrPosZ)
        qp.setPen(old_pen)

    def contains(self, p):
        return self.rect.contains(p)


class IKWidget(QWidget):
    legSelected = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.coord = CoordinateConverter()
        self.setFixedSize(self.coord.scrWidth, self.coord.scrHeight)

        self.draggableRectMap = {}

        self.currentRect = None

    def mousePressEvent(self, event):
        for leg in self.draggableRectMap:
            rect = self.draggableRectMap[leg]
            if rect.contains(event.pos()):
                self.currentRect = rect
                self.legSelected.emit(self.currentRect)
                self.update()
                return

        self.legSelected.emit(None)
        self.currentRect = None
        self.update()

    def mouseMoveEvent(self, event):
        if self.currentRect:
            current_pos = event.pos()
            self.currentRect.setPos(current_pos)
            self.updateRobot()
            self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        color = QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)

        qp.setBrush(QColor(127, 127, 127))
        body_length = RobotConfig.bodyLength
        body_width = RobotConfig.bodyWidth

        body_rect = self.coord.convertRectToScr(-body_width / 2, body_length / 2, body_width, body_length)
        qp.drawRect(body_rect)

        # Draw all the leg targets
        robot_legs = GlobalContext.getRobot().getLegs()
        for leg in robot_legs:
            leg_start_point = leg.get_start_pos()
            leg_target_point = leg.get_target_pos()
            target_scr_point = self.coord.worldToScr(leg_target_point[0].item(0), leg_target_point[1].item(0))

            if leg not in self.draggableRectMap:
                self.draggableRectMap[leg] = DraggableRect(target_scr_point, leg_target_point[2].item(0), leg)
                self.draggableRectMap[leg].valueChanged.connect(self.updateRobot)
            qp.drawLine(self.coord.worldToScr(leg_start_point[0], leg_start_point[1]),
                        target_scr_point)

            if self.draggableRectMap[leg] is self.currentRect:
                self.draggableRectMap[leg].draw(qp, True)
                leg.setDrawCoordinate(True)
            else:
                self.draggableRectMap[leg].draw(qp, False)
                leg.setDrawCoordinate(False)

        self.drawCoordinate(qp)
        qp.end()

    def updateRobot(self):
        if self.currentRect is not None:
            cur_leg = self.currentRect.getLeg()

            # use IK to find link position of the leg
            world_pos = self.coord.scrToWorld(self.currentRect.getPos())
            world_pos.append(self.currentRect.getZ())
            cur_leg.set_end_pos(world_pos)

    def drawCoordinate(self, qp):
        color = QColor(0, 0, 0)
        # Draw Coordinate
        color.setNamedColor('#ff0000')
        qp.setPen(color)
        qp.drawLine(self.coord.worldToScr(0.0, 0.0), self.coord.worldToScr(1.0, 0.0))
        color.setNamedColor('#00ff00')
        qp.setPen(color)
        qp.drawLine(self.coord.worldToScr(0.0, 0.0), self.coord.worldToScr(0.0, 1.0))
