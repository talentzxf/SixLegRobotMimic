from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QFont

from GlobalContext import GlobalContext
from PyQt5.QtCore import Qt, QRect, QPoint, QSize

from GlobalConfig import RobotConfig


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
        tab = QWidget()
        # Create first tab
        tab.layout = QVBoxLayout()

        ikWidget = IKWidget()
        tab.layout.addWidget(ikWidget)
        tab.setLayout(tab.layout)
        return tab

    def initTab2(self):
        tab = QWidget()
        return tab


class CoordinateConverter:
    scrWidth = 400
    scrHeight = 400
    scale = 200

    def convertRectToScr(self, x, y, width, height):
        centerX = CoordinateConverter.scrWidth / 2
        centerY = CoordinateConverter.scrHeight / 2
        left = centerX + x * CoordinateConverter.scale
        width = width * CoordinateConverter.scale
        top = centerY - y * CoordinateConverter.scale
        height = height * CoordinateConverter.scale
        return QRect(left, top, width, height)

    def convertPointToScr(self, x, y):
        centerX = CoordinateConverter.scrWidth / 2
        centerY = CoordinateConverter.scrHeight / 2
        scrX = centerX + x * CoordinateConverter.scale
        scrY = centerY - y * CoordinateConverter.scale
        return QPoint(scrX, scrY)


# Everything in this class happens in Screen coordinate
class DraggableRect:
    size = QSize(10, 10)

    def __init__(self, pos):
        adjusted_pos = QPoint(pos.x() - self.size.width() / 2, pos.y() - self.size.height() / 2)
        self.rect = QRect(adjusted_pos, self.size)

    def setPos(self, pos):
        adjusted_pos = QPoint(pos.x() - self.size.width() / 2, pos.y() - self.size.height() / 2)
        self.rect = QRect(adjusted_pos, self.size)

    def draw(self, qp, selected=False):
        if selected:
            qp.setBrush(QColor(0, 0, 127))
        else:
            qp.setBrush(QColor(127, 127, 127))
        qp.drawRect(self.rect)

    def contains(self, p):
        return self.rect.contains(p)


class IKWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.coordConv = CoordinateConverter()
        self.setFixedSize(self.coordConv.scrWidth, self.coordConv.scrHeight)

        self.draggableRectMap = {}

        self.currentRect = None

    def mousePressEvent(self, event):
        for leg in self.draggableRectMap:
            rect = self.draggableRectMap[leg]
            if rect.contains(event.pos()):
                print("Rect:" + str(rect) + " selected!")
                self.currentRect = rect
                self.update()
                return
        self.currentRect = None
        self.update()

    def mouseMoveEvent(self, event):
        if self.currentRect:
            current_pos = event.pos()
            self.currentRect.setPos(current_pos)
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

        body_rect = self.coordConv.convertRectToScr(-body_width / 2, body_length / 2, body_width, body_length)
        print(body_rect)
        qp.drawRect(body_rect)

        # Draw all the leg targets
        robot_legs = GlobalContext.getRobot().getLegs()
        for leg in robot_legs:
            leg_start_point = leg.get_start_pos()
            leg_target_point = leg.get_target_pos()
            target_scr_point = self.coordConv.convertPointToScr(leg_target_point[0], leg_target_point[1])

            if leg not in self.draggableRectMap:
                self.draggableRectMap[leg] = DraggableRect(target_scr_point)
            qp.drawLine(self.coordConv.convertPointToScr(leg_start_point[0], leg_start_point[1]),
                        target_scr_point)

            if self.draggableRectMap[leg] is self.currentRect:
                self.draggableRectMap[leg].draw(qp, True)
            else:
                self.draggableRectMap[leg].draw(qp, False)

        self.drawCoordinate(qp)
        qp.end()

    def drawCoordinate(self, qp):
        color = QColor(0, 0, 0)
        # Draw Coordinate
        color.setNamedColor('#ff0000')
        qp.setPen(color)
        qp.drawLine(self.coordConv.convertPointToScr(-1.0, 0.0), self.coordConv.convertPointToScr(1.0, 0.0))
        color.setNamedColor('#00070a')
        qp.setPen(color)
        qp.drawLine(self.coordConv.convertPointToScr(0.0, -1.0), self.coordConv.convertPointToScr(0.0, 1.0))
