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
from defines.values import *
    
# ui 연결 변수
form_class = uic.loadUiType(funcs.resourcePath(WIDGET_MANAGER_USER))[0]



class ManagerUserWidgetClass(QWidget, form_class):
    def __init__(self):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.comboBoxDetail.addItems(USER_DETAILS_LIST)

        self.selectedUserID = None
        self.selectedUserName = None

        self.refreshUserList()

        ## ==================== 위젯 연결 ==================== ##
        self.treeWidgetUserList: QTreeWidget
        self.comboBoxDetail: QComboBox
        self.lineEditSearch: QLineEdit
        self.pushButtonSearch: QPushButton
        self.pushButtonInitialization: QPushButton

        ## ==================== 시그널 연결 ==================== ##
        self.pushButtonSearch.clicked.connect(self.refreshUserList)
        self.treeWidgetUserList.itemClicked.connect(self.selectItem)
        self.pushButtonInitialization.clicked.connect(self.initUserPassword)

    ## ==================== 함수 ==================== ##
    def refreshUserList(self):
        self.treeWidgetUserList.clear()

        detailIndex = self.comboBoxDetail.currentIndex()
        inputValue = "%" + self.lineEditSearch.text() + "%"


        # mssql 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 쿼리 실행
        query = f'''
        SELECT uid, username, phone, address, email
        FROM Member
        WHERE {USER_DETAILS_FIELD_LIST[detailIndex]} LIKE %s
        '''
        values = (inputValue, )
        cursor.execute(query, values)

        row = cursor.fetchone()

        while row:
            item = QTreeWidgetItem(row)
            self.treeWidgetUserList.addTopLevelItem(item)
            row = cursor.fetchone()

        # mssql 연결 끊기
        cursor.close()
        connect.close()

    def selectItem(self, item):
        self.pushButtonInitialization.setEnabled(True)
        self.selectedUserID = item.text(0)
        self.selectedUserName = item.text(1)

    def initUserPassword(self):
        reply = QMessageBox.question(self, INFORMATION_MESSAGE, INIT_USER_PASSWORD_MESSAGE % self.selectedUserName,  
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                    QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # mssql 연결
            connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
            cursor = connect.cursor()

            # 쿼리 실행
            query = '''
            UPDATE Member
            SET password = %s
            WHERE uid = %s
            '''
            values = (INIT_PASSWORD_VALUE, self.selectedUserID)
            cursor.execute(query, values)

            connect.commit()

            # mssql 연결 끊기
            cursor.close()
            connect.close()

            QMessageBox.information(self, INFORMATION_MESSAGE, INIT_USER_PASSWORD_SUCCESS % (self.selectedUserName, INIT_PASSWORD_VALUE), QMessageBox.StandardButton.Ok)