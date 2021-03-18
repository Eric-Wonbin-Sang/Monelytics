from win32api import GetSystemMetrics

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GUIFiles import PyCute


class AccountWidget(QWidget):

    def __init__(self):

        super().__init__()
        self.horizontal_layout = QHBoxLayout()
        self.setLayout(self.horizontal_layout)

        self.horizontal_layout.addWidget(QLabel("AccountWidget"))
