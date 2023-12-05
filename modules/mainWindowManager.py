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
import modules.widgetManagerBook as widgetManagerBook
import modules.widgetManagerUser as widgetManagerUser
import modules.widgetManagerLoan as widgetManagerLoan
    
# ui 연결 변수
form_class = uic.loadUiType(funcs.resourcePath(MAIN_WINDOW_MANAGER_UI_PATH))[0]



class MainWindowManagerClass(QMainWindow, form_class):
    def __init__(self, userInfo):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.userInfo: tuple = userInfo # 로그인 시 사용자 정보
        QMessageBox.information(self, LOG_IN_SUCCESS, LOG_IN_MESSAGE % self.userInfo[2], QMessageBox.StandardButton.Ok)

        ## ==================== 위젯 연결 ==================== ##
        self.pushButtonLogOut: QPushButton
        self.pushButtonBookManagement: QPushButton
        self.pushButtonMemberManagement: QPushButton
        self.pushButtonLoanManagement: QPushButton
        self.labelUserInfo: QLabel

        ## ==================== 시그널 연결 ==================== ##
        self.pushButtonLogOut.clicked.connect(self.logOutFunc)
        self.pushButtonBookManagement.clicked.connect(self.viewBookManagement)
        self.pushButtonMemberManagement.clicked.connect(self.viewUserManagement)
        self.pushButtonLoanManagement.clicked.connect(self.viewLoanManagement)

    ## ==================== 함수 ==================== ##
    # 로그아웃 함수
    def logOutFunc(self):
        reply = QMessageBox.question(self, LOG_OUT_MESSAGE_BOX_TITLE, LOG_OUT_MESSAGE_BOX_CONTENT, 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            self.mainWindow = mainWindow.MainWindowClass()
            self.mainWindow.show()
        else:
            return
        
    # 도서 관리 버튼 클릭 시 작동 함수
    def viewBookManagement(self):
        self.widgetManagerBook = widgetManagerBook.ManagerBookWidgetClass()
        self.widgetManagerBook.show()


    # 회원 관리 버튼 클릭 시 작동 함수
    def viewUserManagement(self):
        self.widgetManagerUser = widgetManagerUser.ManagerUserWidgetClass()
        self.widgetManagerUser.show()

    # 대출 관리 버튼 클릭 시 작동 함수
    def viewLoanManagement(self):
        self.widgetManagerLoan = widgetManagerLoan.ManagerLoanWidgetClass()
        self.widgetManagerLoan.show()