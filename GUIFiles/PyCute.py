import PyQt5.QtWidgets
import PyQt5.QtCore
from PyQt5.QtGui import QKeySequence


class Button(PyQt5.QtWidgets.QPushButton):

    def __init__(self, default_text, connect_func=None, parent_widget=None, shortcut_command=None):

        super().__init__(str(default_text))

        self.default_text = default_text
        self.connect_func = connect_func
        self.parent_widget = parent_widget
        self.shortcut_command = shortcut_command
        self.shortcut = self.get_shortcut()

        if self.connect_func:
            self.clicked.connect(self.connect_func)

    def get_shortcut(self):
        return Shortcut(self.parent_widget, self.shortcut_command, connect_func=self.connect_func) \
            if self.shortcut_command is not None else None


class TextBox(PyQt5.QtWidgets.QLineEdit):

    def __init__(self, text=None):

        super().__init__()

        if text is not None:
            self.setText(str(text))

        self.init_text = self.text()

        self.setDragEnabled(True)

    def reset(self):
        self.setText(self.init_text)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            # for some reason, this doubles up the intro slash
            self.setText(str(urls[0].path())[1:])


class DropDown(PyQt5.QtWidgets.QComboBox):

    def __init__(self, option_list, default_option=None):

        super().__init__()

        self.option_list = option_list
        self.default_option = default_option

        self.setup()

    def setup(self):
        for option in self.option_list:
            self.addItem(option)
        if self.default_option in self.option_list:
            self.setCurrentIndex(self.option_list.index(self.default_option))


class Label(PyQt5.QtWidgets.QLabel):

    def __init__(self, **kwargs):

        super().__init__()

        self.text = str(kwargs.get("default_text"))
        self.setText(self.text)

        # if kwargs.get("align_right"):
        #     self.setAlignment(PyQt5.QtCore.Qt.AlignRight | PyQt5.QtCore.Qt.AlignVCenter)


class FileChooser(PyQt5.QtWidgets.QFileDialog):

    def __init__(self):

        super().__init__()
        self.setFileMode(PyQt5.QtWidgets.QFileDialog.ExistingFiles)


class Shortcut(PyQt5.QtWidgets.QShortcut):

    def __init__(self, parent_widget, command, connect_func=None):

        super().__init__(QKeySequence(command), parent_widget)

        self.connect_func = connect_func
        self.activated.connect(self.connect_func)


class Thread(PyQt5.QtCore.QRunnable):

    def __init__(self, connect_func=None):

        super().__init__()

        self.connect_func = connect_func

    @PyQt5.QtCore.pyqtSlot()
    def run(self):
        self.connect_func()


def get_spacer():
    return PyQt5.QtWidgets.QSpacerItem(20, 40, PyQt5.QtWidgets.QSizePolicy.Minimum, PyQt5.QtWidgets.QSizePolicy.Expanding)


def remove_from_layout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)


def add_to_layout(parent_layout, *args):
    for arg in args:
        if type(arg) == tuple:
            parent_layout.addWidget(*arg)
        elif PyQt5.QtWidgets.QLayout in type(arg).__mro__:
            parent_layout.addLayout(arg)
        elif PyQt5.QtWidgets.QSpacerItem in type(arg).__mro__:
            parent_layout.addItem(arg)
        else:
            parent_layout.addWidget(arg)
    return parent_layout
