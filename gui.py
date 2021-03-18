import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream

from GUIFiles import MainWindow


def main():

    app = QtWidgets.QApplication(sys.argv)

    # file = QFile(":/dark.qss")
    # file.open(QFile.ReadOnly | QFile.Text)
    # stream = QTextStream(file)
    # app.setStyleSheet(stream.readAll())

    main_window = MainWindow.MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()