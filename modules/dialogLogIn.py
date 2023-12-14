import pymssql

# PyQt6 모듈
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import *

# 사용자 모듈
import modules.functions as funcs
from defines.paths import *
from defines.strings import *

# ui 연결 변수
form_class = uic.loadUiType(funcs.resourcePath(LOG_IN_UI_PATH))[0]

class LogInDialogClass(QDialog, form_class):
    acceptSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        ## ==================== 위젯 연결 ==================== ##
        self.lineEditUserID: QLineEdit
        self.lineEditUserPassword: QLineEdit
        self.pushButtonAnswer: QPushButton


        ## ==================== 시그널 연결 ==================== ##
        self.pushButtonAnswer.clicked.connect(self.buttonBoxAccepted)
        

    ## ==================== 함수 ==================== ##
    def buttonBoxAccepted(self):
        # 입력 값 추출
        uid = self.lineEditUserID.text()
        password = self.lineEditUserPassword.text()

        # mssql 검색 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 아이디 존재여부 확인 쿼리
        query = "SELECT * FROM Member WHERE uid = %s"
        values = (uid, )
        cursor.execute(query, values)
        get = cursor.fetchall()

        # mssql 연결 해제
        cursor.close()
        connect.close()

        # 아이디 존재여부 확인
        if len(get) == 0: # 아이디가 존재하지 않을 때
            self.acceptSignal.emit(LOG_IN_ERROR_NO_USERID)
        elif get[0][1] != password: # 비밀번호가 틀릴 때
            self.acceptSignal.emit(LOG_IN_ERROR_WRONG_PASSWORD)
        else: # 로그인 성공
            self.acceptSignal.emit(uid)
        
        self.close()