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
form_class = uic.loadUiType(funcs.resourcePath(SIGN_UP_UI_PATH))[0]

class SignUpDialogClass(QDialog, form_class):
    acceptSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        ## ==================== 위젯 연결 ==================== ##
        self.lineEditID: QLineEdit
        self.lineEditPassword: QLineEdit
        self.lineEditName: QLineEdit
        self.lineEditPhone: QLineEdit
        self.lineEditAddress: QLineEdit
        self.lineEditEmail: QLineEdit
        self.comboBoxGrade: QComboBox
        self.buttonBoxAnswer: QDialogButtonBox


        ## ==================== 시그널 연결 ==================== ##
        self.buttonBoxAnswer.accepted.connect(self.buttonBoxAccepted) # OK 버튼 클릭 시그널 연결


    ## ==================== 함수 ==================== ##
    def buttonBoxAccepted(self):
        # 입력 값 추출
        uid = self.lineEditID.text()
        password = self.lineEditPassword.text()
        username = self.lineEditName.text()
        phone = self.lineEditPhone.text()
        address = self.lineEditAddress.text()
        email = self.lineEditEmail.text()
        grade = self.comboBoxGrade.currentText()

        # 필수 입력 항목 체크
        if (uid == "" or password == "" or username == ""):
            self.acceptSignal.emit(SIGN_UP_ERROR_NO_INPUT)
            return
        
        # mssql 검색 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET_SELECT)
        cursor = connect.cursor()

        # 입력한 아이디가 이미 존재하는 지 확인하는 쿼리 실행
        query = "SELECT uid FROM Member WHERE uid = %s"
        values = (uid, )
        cursor.execute(query, values)

        get = cursor.fetchall()

        cursor.execute(query, values)
        connect.commit()


        # 이미 존재하는 아이디인 경우 가입 불가/아니면 가입 등록 쿼리 실행
        if len(get) != 0:
            self.acceptSignal.emit(SIGN_UP_ERROR_ALREADY_EXIST)
        else:
            # mssql 삽입 연결
            connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET_INSERT)
            cursor = connect.cursor()

            query = "INSERT INTO Member VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (uid, password, username, phone, address, email, grade)
            cursor.execute(query, values)
            connect.commit()

            cursor.close()
            connect.close()

            self.acceptSignal.emit(SIGN_UP_SUCCESS)
