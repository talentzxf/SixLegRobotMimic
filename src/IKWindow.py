from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QFont

from GlobalContext import GlobalContext
from PyQt5.QtCore import Qt


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
        legComboBox = QComboBox()
        for legIdx in range(GlobalContext.getRobot().getLegNumber()):
            legComboBox.addItem(str(legIdx))

        legComboBox.currentIndexChanged.connect(GlobalContext.getRobot().legSelected)
        tab.layout.addWidget(legComboBox)

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
    scale = 10

    def convertToScr(self, x, y, width, height):
        centerX = CoordinateConverter.scrWidth / 2
        centerY = CoordinateConverter.scrHeight / 2
        left = (centerX + x) * CoordinateConverter.scale
        width = width * CoordinateConverter.scale
        top = centerY - y * CoordinateConverter.scale



class IKWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.coordConv = CoordinateConverter()
        self.setFixedSize(self.coordConv.scrWidth, self.coordConv.scrHeight)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.drawRect(10, 15, 90, 60)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, "Mamahong")
