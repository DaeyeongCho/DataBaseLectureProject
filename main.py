import sys

from PyQt6.QtWidgets import *

from modules.MainWindow import WindowClass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec()
