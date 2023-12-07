import pymssql
import datetime

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
form_class = uic.loadUiType(funcs.resourcePath(WIDGET_MANAGER_LOAN))[0]



class ManagerLoanWidgetClass(QWidget, form_class):
    def __init__(self):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.selectLoanID = None

        self.comboBoxDetail.addItems(LOAN_DETAILS_LIST)

        self.refreshUserList()

        ## ==================== 위젯 연결 ==================== ##
        self.treeWidgetLoanList: QTreeWidget
        self.comboBoxDetail: QComboBox
        self.lineEditSearch: QLineEdit
        self.checkBoxNotReturn: QCheckBox
        self.pushButtonSearch: QPushButton
        self.pushButtonDeleteOverdue: QPushButton

        ## ==================== 시그널 연결 ==================== ##
        self.pushButtonSearch.clicked.connect(self.refreshUserList)
        self.treeWidgetLoanList.itemClicked.connect(self.selectItem)
        self.pushButtonDeleteOverdue.clicked.connect(self.deleteOverdue)

    ## ==================== 함수 ==================== ##
    def refreshUserList(self):
        self.treeWidgetLoanList.clear()

        detailIndex = self.comboBoxDetail.currentIndex()
        inputValue = "%" + self.lineEditSearch.text() + "%"
        if self.checkBoxNotReturn.isChecked():
            boolReturned = "AND returnstatus = '미반납'"
        else:
            boolReturned = ""


        # mssql 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 전체 대츨 내역 검색
        query = f'''
        SELECT lid, username, bookname, loandate, returndate, returnstatus
        FROM Member, Book, Loan
        WHERE Member.uid = Loan.uid
        AND Book.bid = Loan.bid
        AND {LOAN_DETAILS_FIELD_LIST[detailIndex]} LIKE %s
        {boolReturned}
        ORDER BY loandate DESC, returndate DESC
        '''
        values = (inputValue, )
        cursor.execute(query, values)

        row = cursor.fetchone()
        while row:
            if row[5] == LOAN_NOT_RETURN and row[4] < datetime.date.today():
                overdue = LOAN_OVERDUE
            else:
                overdue = LOAN_NOT_OVERDUE

            item = QTreeWidgetItem((row[1], row[2], row[3].strftime("%Y-%m-%d"), row[4].strftime("%Y-%m-%d"), row[5], overdue))
            item.setData(0, Qt.ItemDataRole.UserRole, row[0])
            self.treeWidgetLoanList.addTopLevelItem(item)

            row = cursor.fetchone()

        # mssql 연결 끊기
        cursor.close()
        connect.close()

    def selectItem(self, item):
        self.selectLoanID = item.data(0, Qt.ItemDataRole.UserRole)

        if item.text(5) == LOAN_OVERDUE:
            self.pushButtonDeleteOverdue.setEnabled(True)
        else:
            self.pushButtonDeleteOverdue.setEnabled(False)

    def deleteOverdue(self):
        reply = QMessageBox.question(self, INFORMATION_MESSAGE, DELETE_OVERDUE_MESSAGE,  
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                    QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # mssql 연결
            connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
            cursor = connect.cursor()

            # 쿼리 실행
            query = '''
            UPDATE Loan
            SET returnstatus = %s
            WHERE lid = %d
            '''
            values = (LOAN_RETURNED, self.selectLoanID)
            cursor.execute(query, values)

            connect.commit()

            # mssql 연결 끊기
            cursor.close()
            connect.close()

            QMessageBox.information(self, INFORMATION_MESSAGE, DELETE_OVERDUE_SUCCESS, QMessageBox.StandardButton.Ok)
            self.refreshUserList()