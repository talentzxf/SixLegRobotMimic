from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox)
from PyQt5.QtCore import pyqtSlot

from GlobalContext import GlobalContext


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
        tab.setLayout(tab.layout)
        return tab

    def initTab2(self):
        tab = QWidget()
        return tab

class IKWidget()