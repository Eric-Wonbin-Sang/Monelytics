from win32api import GetSystemMetrics

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GUIFiles import PastWidget, FutureWidget, AccountWidget
from GUIFiles import PyCute

from NewPastSystem import main as past_system

from General import Functions, Constants


class MainWindow(QMainWindow):

    main_window_title = "Monelytics"
    init_width = 1600
    init_height = 1000

    def __init__(self):

        super().__init__()

        bank_list = past_system.get_full_bank_list()
        for bank in bank_list:
            print(bank)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.content_widget_list = [
            PastWidget.PastWidget(bank_list),
            FutureWidget.FutureWidget(),
            AccountWidget.AccountWidget()
        ]
        self.stacked_layout = PyCute.get_stacked_layout(self.content_widget_list)

        self.setup_gui()
        self.show()

    def get_menu_widget(self):

        menu_layout = QHBoxLayout()

        image_widget = PyCute.Image("GUIFiles/ImageFiles/monelytics logo.jpg", height=self.init_height * .25)
        past_button = PyCute.Button("Past", connect_func=PyCute.change_stack_index(self.stacked_layout, 0))
        future_button = PyCute.Button("Future", connect_func=PyCute.change_stack_index(self.stacked_layout, 1))
        account_button = PyCute.Button("Account", connect_func=PyCute.change_stack_index(self.stacked_layout, 2))

        menu_layout.addWidget(image_widget, alignment=Qt.AlignLeft)
        menu_layout.addWidget(past_button, alignment=Qt.AlignLeft)
        menu_layout.addWidget(future_button, alignment=Qt.AlignLeft)
        menu_layout.addWidget(account_button, alignment=Qt.AlignRight)

        container = PyCute.get_container_widget(menu_layout)
        container.setStyleSheet("background-color:rgb(173, 217, 255);")

        return container

    def setup_gui(self):

        init_x = GetSystemMetrics(0)/2 - self.init_width/2
        init_y = GetSystemMetrics(1)/2 - self.init_height/2

        main_layout = QGridLayout()
        self.main_widget.setLayout(main_layout)

        main_layout.addWidget(self.get_menu_widget(), 0, 0, 1, 1)
        main_layout.addWidget(PyCute.get_container_widget(self.stacked_layout), 1, 0, 9, 1)

        self.setGeometry(init_x, init_y, self.init_width, self.init_height)
        self.setWindowTitle(self.main_window_title)
