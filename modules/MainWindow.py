import pymssql

# PyQt6 모듈
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon

# 사용자 모듈
import modules.functions as funcs
from defines.paths import *
from defines.strings import *

import modules.logIn as logIn
import modules.signUp as signUp
import modules.mainWindowGeneral as mainWindowGeneral
import modules.mainWindowManager as mainWindowManager
    
# ui 연결 변수
form_class = uic.loadUiType(funcs.resourcePath(MAIN_WINDOW_UI_PATH))[0]



class MainWindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        ## ==================== 위젯 연결 ==================== ##
        self.pushButtonLogIn: QPushButton
        self.pushButtonSignUp: QPushButton
        self.labelNotification: QLabel


        ## ==================== 시그널 연결 ==================== ##
        self.pushButtonLogIn.clicked.connect(self.viewLogInDialog)
        self.pushButtonSignUp.clicked.connect(self.viewSignUpWidget)


    ## ==================== 함수 ==================== ##
    # 로그인 창 띄우는 함수
    def viewLogInDialog(self):
        self.logInDialog = logIn.LogInDialogClass()
        self.logInDialog.acceptSignal.connect(self.getLogInDialogAcceptSignal)
        self.logInDialog.show()

    # 로그인 창에서 확인 버튼 클릭 시 작동하는 함수
    def getLogInDialogAcceptSignal(self, getStr):
        self.labelNotification.setText(getStr)

        # 로그인 실패 시 아무것도 하지 않음
        if getStr == LOG_IN_ERROR_NO_USERID or getStr == LOG_IN_ERROR_WRONG_PASSWORD:
            return

        # mssql 검색 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET_SELECT)
        cursor = connect.cursor()

        # 회원 정보 확인
        query = "SELECT * FROM Member WHERE uid = %s"
        values = (getStr, )
        cursor.execute(query, values)
        userInfo = cursor.fetchone()

        # mssql 연결 해제
        cursor.close()
        connect.close()

        # 로그인한 사용자 권한에 따라 다른 화면 출력
        if userInfo[6] == GENERAL_MEMBER:
            self.close()
            self.generalWindow = mainWindowGeneral.MainWindowGeneralClass(userInfo)
            self.generalWindow.show()
        elif userInfo[6] == MANAGER_MEMBER:
            self.close()
            self.managerWindow = mainWindowManager.MainWindowManagerClass(userInfo)
            self.managerWindow.show()


    
    
    # 회원가입 창 띄우는 함수
    def viewSignUpWidget(self):
        self.signupDialog = signUp.SignUpDialogClass()
        self.signupDialog.acceptSignal.connect(self.getSignUpDialogAcceptSignal)
        self.signupDialog.show()

    # 회원가입 창에서 확인 버튼 클릭 시 작동하는 함수
    def getSignUpDialogAcceptSignal(self, getStr):
        self.labelNotification.setText(getStr)