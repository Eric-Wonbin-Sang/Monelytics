from win32api import GetSystemMetrics

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from General import Constants
from GUIFiles import PyCute


class MainWindow(QMainWindow):

    main_window_title = "Monelytics"
    init_width = 1600
    init_height = 1000

    def __init__(self):

        super().__init__()

        # self.vertical_layout = self.get_vertical_layout()
        # self.menu_layout = self.get_menu_layout()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.setup_gui()
        self.show()

    def get_menu_widget(self):
        container = QWidget()
        container.setStyleSheet("background-color:rgb(173, 217, 255);")

        menu_layout = QHBoxLayout()
        container.setLayout(menu_layout)

        label = QLabel()
        pixmap = QPixmap("GUIFiles/ImageFiles/monelytics logo.jpg")
        new_height = self.init_height * .25
        new_width = new_height * (pixmap.height() / pixmap.width())
        pixmap = pixmap.scaled(new_height, new_width)
        label.setPixmap(pixmap)

        past_button = PyCute.Button("Past", connect_func=None, parent_widget=container, shortcut_command=None)
        future_button = PyCute.Button("Future", connect_func=None, parent_widget=container, shortcut_command=None)
        account_button = PyCute.Button("Account", connect_func=None, parent_widget=container, shortcut_command=None)


        menu_layout.addWidget(label)
        menu_layout.addWidget(past_button, alignment=Qt.AlignLeft)
        menu_layout.addWidget(future_button, alignment=Qt.AlignLeft)
        menu_layout.addWidget(account_button, alignment=Qt.AlignRight)

        return container

    def get_content_widget(self):
        container = QWidget()

        stacked_layout = QStackedLayout()
        container.setLayout(stacked_layout)

        return container

    def setup_gui(self):

        init_x = GetSystemMetrics(0)/2 - self.init_width/2
        init_y = GetSystemMetrics(1)/2 - self.init_height/2

        main_layout = QGridLayout()
        self.main_widget.setLayout(main_layout)

        main_layout.addWidget(self.get_menu_widget(), 0, 0, 1, 1)
        main_layout.addWidget(self.get_content_widget(), 1, 0, 9, 1)

        self.setGeometry(init_x, init_y, self.init_width, self.init_height)
        self.setWindowTitle(self.main_window_title)
