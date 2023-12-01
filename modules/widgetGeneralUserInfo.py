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
form_class = uic.loadUiType(funcs.resourcePath(WIDGET_GENERAL_USER_INFO))[0]



class GeneralUserInfoWidgetClass(QWidget, form_class):
    acceptSignal = pyqtSignal(str)
    
    def __init__(self, userInfo):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.userID, self.userPassword, self.userName, self.userPhone, self.userAddress, self.userEmail, self.userGrade = userInfo

        self.labelUserName.setText(USER_NAME_INTRODUCTION % self.userName)
        self.lineEditPhone.setText(self.userPhone)
        self.lineEditAddress.setText(self.userAddress)
        self.lineEditEmail.setText(self.userEmail)

        ## ==================== 위젯 연결 ==================== ##
        self.labelUserName: QLabel
        self.lineEditPhone: QLineEdit
        self.lineEditAddress: QLineEdit
        self.lineEditEmail: QLineEdit
        self.lineEditPassword: QLineEdit
        self.lineEditPasswordCheck: QLineEdit
        self.pushButtonUserInformationSet: QPushButton
        self.pushButtonPasswordSet: QPushButton

        ## ==================== 시그널 연결 ==================== ##
        self.pushButtonUserInformationSet.clicked.connect(self.setUserInformation)
        self.pushButtonPasswordSet.clicked.connect(self.setUserPassword)

    ## ==================== 함수 ==================== ##
    # 회원 정보 변경 함수
    def setUserInformation(self):
        reply = self.viewSelectMessageBox(INFORMATION_MESSAGE, SET_USER_INFORMATION_QUESTION_MESSAGE)
        
        if reply == True:
            # mssql 연결
            connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
            cursor = connect.cursor()

            phone, address, email = self.getInputUserInfo()

            # 정보 교체 쿼리 실행
            query = '''
            UPDATE Member
            SET phone = %s, address = %s, email = %s
            WHERE uid = %s
            '''
            values = (phone, address, email, self.userID)
            cursor.execute(query, values)

            connect.commit()

            # mssql 연결 끊기
            cursor.execute(query, values)
            connect.commit()

            self.setRefreshUserInfoSignal()

            self.viewInformationMessageBox(INFORMATION_MESSAGE, SET_USER_INFORMATION_SUCCESS)
        else:
            pass

    # 비밀번호 변경 함수
    def setUserPassword(self):
        reply = self.viewSelectMessageBox(INFORMATION_MESSAGE, SET_USER_PASSWORD_QUESTION_MESSAGE)

        if reply == True:
            password, passwordCheck = self.getInputUserPassword()
            
            if password == "" or passwordCheck == "":
                self.viewWarningMessageBox(WARNING_MESSAGE, SET_USER_PASSWORD_ERROR_NO_INPUT)
                return
            if password != passwordCheck:
                self.viewWarningMessageBox(WARNING_MESSAGE, SET_USER_PASSWORD_ERROR_DIFFERENT_INPUT)
                return
            
            # mssql 연결
            connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
            cursor = connect.cursor()

            # 비밀번호 교체 쿼리 실행
            query = '''
            UPDATE Member
            SET password = %s
            WHERE uid = %s
            '''
            values = (password, self.userID)
            cursor.execute(query, values)

            connect.commit()

            # mssql 연결 끊기
            cursor.execute(query, values)
            connect.commit()

            self.setRefreshUserInfoSignal()

            self.viewInformationMessageBox(INFORMATION_MESSAGE, SET_USER_PASSWORD_SUCCESS)

    # 선택 메세지 박스 출력 함수
    def viewSelectMessageBox(self, title, content) -> bool:
        reply = QMessageBox.question(self, title, content, 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False
        
    # 정보 메세지 박스 출력 함수
    def viewInformationMessageBox(self, title, content) -> None:
        QMessageBox.information(self, title, content, QMessageBox.StandardButton.Ok)

    # 경고 메세지 박스 출력 함수
    def viewWarningMessageBox(self, title, content) -> None:
        QMessageBox.warning(self, title, content, QMessageBox.StandardButton.Ok)
        
    # 입력한 새 사용자 정보 반환
    def getInputUserInfo(self) -> tuple:
        phone = self.lineEditPhone.text()
        address = self.lineEditAddress.text()
        email = self.lineEditEmail.text()

        return (phone, address, email)

    # 입력한 새 비밀번호 반환
    def getInputUserPassword(self) -> tuple:
        password = self.lineEditPassword.text()
        passwordCheck = self.lineEditPasswordCheck.text()

        return (password, passwordCheck)
    

    # 사용자 정보 새로고침
    def setRefreshUserInfoSignal(self):
        self.acceptSignal.emit(self.userID)