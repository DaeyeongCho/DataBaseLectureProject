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
import modules.widgetGeneralBook as widgetGeneralBook
import modules.widgetGeneralLoan as widgetGeneralLoan
import modules.widgetGeneralUserInfo as widgetGeneralUserInfo
    
# ui 연결 변수
form_class = uic.loadUiType(funcs.resourcePath(MAIN_WINDOW_GENERAL_UI_PATH))[0]



class MainWindowGeneralClass(QMainWindow, form_class):
    def __init__(self, userInfo):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.userInfo: tuple = userInfo # 로그인 시 사용자 정보
        QMessageBox.information(self, LOG_IN_SUCCESS, LOG_IN_MESSAGE % self.userInfo[2], QMessageBox.StandardButton.Ok)

        ## ==================== 위젯 연결 ==================== ##
        self.pushButtonLogOut: QPushButton
        self.pushButtonBookList: QPushButton
        self.pushButtonLoanStatus: QPushButton
        self.pushButtonMyInfo: QPushButton
        self.labelUserInfo: QLabel

        ## ==================== 시그널 연결 ==================== ##
        self.pushButtonLogOut.clicked.connect(self.logOutFunc)
        self.pushButtonBookList.clicked.connect(self.viewBookList)
        self.pushButtonLoanStatus.clicked.connect(self.viewLoanStatus)
        self.pushButtonMyInfo.clicked.connect(self.viewUserInfo)

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
        
    # 도서 목록 버튼 클릭 시 작동 함수
    def viewBookList(self):
        self.bookList = widgetGeneralBook.GeneralBookWidgetClass(self.userInfo)
        self.bookList.show()

    # 대출 현황 버튼 클릭 시 작동 함수
    def viewLoanStatus(self):
        self.loanList = widgetGeneralLoan.GeneralLoanWidgetClass(self.userInfo)
        self.loanList.show()

    # 정보 확인 버튼 클릭 시 작동 함수
    def viewUserInfo(self):
        self.userInformation = widgetGeneralUserInfo.GeneralUserInfoWidgetClass(self.userInfo)
        self.userInformation.acceptSignal.connect(self.refreshUserInfo)
        self.userInformation.show()

    # 정보 확인에서 정보 변경 시 사용자 정보 새로고침
    def refreshUserInfo(self, userID):
        # mssql 검색 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 회원 정보 확인
        query = "SELECT * FROM Member WHERE uid = %s"
        values = (userID, )
        cursor.execute(query, values)
        getUserInfo = cursor.fetchone()

        self.userInfo = getUserInfo

        # mssql 연결 해제
        cursor.close()
        connect.close()