import sys

from PyQt6.QtWidgets import *

from modules.mainWindow import MainWindowClass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MainWindowClass()
    myWindow.show()
    app.exec()
    