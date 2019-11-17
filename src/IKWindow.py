import math

from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QSlider)
from PyQt5.QtCore import pyqtSlot, pyqtSignal
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
        self.tabs.addTab(self.initTab2(), "Tab 2")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    # TODO: better naming
    def initTab1(self):
        slider = QSlider(Qt.Vertical)
        slider.setRange(-10, 10)
        slider.setSingleStep(1)
        slider.setPageStep(10)
        slider.setTickInterval(10)
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
            self.heightSlider.setValue(draggableRect.getZ())
            self.heightSlider.show()
            self.heightSlider.valueChanged.connect(self.setZ(draggableRect))
        else:
            self.heightSlider.setValue(0)
            self.heightSlider.hide()

    def setZ(self, draggableRect):
        def _setZ(z):
            draggableRect.setZ(z)

        return _setZ

    def initTab2(self):
        tab = QWidget()
        return tab


# Everything in this class happens in Screen coordinate
class DraggableRect:
    size = QSize(10, 10)

    # leg means this rect corresponds to which leg.
    def __init__(self, pos, z, leg):
        adjusted_pos = QPoint(pos.x() - self.size.width() / 2, pos.y() - self.size.height() / 2)
        self.rect = QRect(adjusted_pos, self.size)
        self.leg = leg
        self.coord = CoordinateConverter()
        self.z = z  # z is the z coordinate of the leg in world space

    def setZ(self, z):
        self.z = z

    def getZ(self):
        return self.z

    def getLeg(self):
        return self.leg

    def setPos(self, pos):
        adjusted_pos = QPoint(pos.x() - self.size.width() / 2, pos.y() - self.size.height() / 2)
        self.rect = QRect(adjusted_pos, self.size)
        return adjusted_pos

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
            worldPosX = self.coord.objectToWorld([1, 0, self.z], self.leg.get_init_transformation_matrix())
            scrPosX = self.coord.worldToScr(worldPosX[0], worldPosX[1])

            qp.drawLine(leg_scr_position, scrPosX)
            # Local y coordinate
            color.setNamedColor('#00ff00')
            qp.setPen(color)
            worldPosY = self.coord.objectToWorld([0, 1, self.z], self.leg.get_init_transformation_matrix())
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
                self.update()

                self.legSelected.emit(self.currentRect)
                self.update()
                return

        self.legSelected.emit(None)
        self.currentRect = None
        self.update()

    def mouseMoveEvent(self, event):
        if self.currentRect:
            current_pos = event.pos()
            adjusted_pos = self.currentRect.setPos(current_pos)

            cur_leg = self.currentRect.getLeg()

            # TODO: Move this part to a separate IKSolver
            # use IK to find link position of the leg
            # 1. Convert to world coordinate
            world_pos = self.coord.scrToWorld(adjusted_pos)
            world_pos.append(self.currentRect.getZ())
            # 2. Convert to leg coordinate
            leg_relative_pos = self.coord.worldToObject(world_pos, cur_leg.get_init_transformation_matrix())
            # 3. Use IKSolver to solve it
            thetas = cur_leg.getSolver().solve(leg_relative_pos)

            if thetas is not None:
                # 4. Update angles
                # TODO: put this into logic of leg
                legId = GlobalContext.getRobot().getLegId(cur_leg.getName())
                GlobalContext.getRobot().getController().setLegLinkAngle(legId, 0)(thetas[0])
                GlobalContext.getRobot().getController().setLegLinkAngle(legId, 1)(thetas[1])
                GlobalContext.getRobot().getController().setLegLinkAngle(legId, 2)(thetas[2])

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

    def drawCoordinate(self, qp):
        color = QColor(0, 0, 0)
        # Draw Coordinate
        color.setNamedColor('#ff0000')
        qp.setPen(color)
        qp.drawLine(self.coord.worldToScr(0.0, 0.0), self.coord.worldToScr(1.0, 0.0))
        color.setNamedColor('#00ff00')
        qp.setPen(color)
        qp.drawLine(self.coord.worldToScr(0.0, 0.0), self.coord.worldToScr(0.0, 1.0))
