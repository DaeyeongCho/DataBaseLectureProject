import pymssql

# PyQt6 모듈
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon

# 사용자 모듈
import modules.functions as funcs
from defines.paths import *
from defines.strings import *

import modules.mainWindow as mainWindow
    
# ui 연결 변수
form_class = uic.loadUiType(funcs.resourcePath(MAIN_WINDOW_MANAGER_UI_PATH))[0]



class MainWindowManagerClass(QMainWindow, form_class):
    def __init__(self, userInfo):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.userInfo: tuple = userInfo # 로그인 시 사용자 정보

        ## ==================== 위젯 연결 ==================== ##
        self.pushButtonLogOut: QPushButton
        self.pushButtonBookManagement: QPushButton
        self.pushButtonMemberManagement: QPushButton
        self.pushButtonLoanManagement: QPushButton

        ## ==================== 시그널 연결 ==================== ##
        self.pushButtonLogOut.clicked.connect(self.logOutFunc)

    ## ==================== 함수 ==================== ##
    def logOutFunc(self):
        reply = QMessageBox.question(self, '확인', '로그아웃 하시겠습니까?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            self.mainWindow = mainWindow.MainWindowClass()
            self.mainWindow.show()
        else:
            return