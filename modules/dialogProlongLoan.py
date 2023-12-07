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
form_class = uic.loadUiType(funcs.resourcePath(DIALOG_PROLONG_LOAN))[0]



class ProlongLoanDialogClass(QDialog, form_class):
    signal = pyqtSignal()

    def __init__(self, selectLoan):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.loanID, self.loanBookName, self.loanDate, self.returnDate, self.returnStatus = selectLoan

        QReturnDate = QDate.fromString(self.returnDate, "yyyy-MM-dd")
        QMaximumProlongDate = QDate.currentDate().addDays(7)

        self.calendarWidget.setMinimumDate(QReturnDate)
        self.calendarWidget.setMaximumDate(QMaximumProlongDate)

        ## ==================== 위젯 연결 ==================== ##
        self.calendarWidget: QCalendarWidget
        self.buttonBox: QDialogButtonBox

        ## ==================== 시그널 연결 ==================== ##
        self.buttonBox.accepted.connect(self.setProlongLoanFunc)

    ## ==================== 함수 ==================== ##
    def setProlongLoanFunc(self):
        # 선택한 날짜를 "yyyy-mm-dd" 형식의 문자열로 반환
        selectedDate = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")

        # mssql 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 쿼리 실행
        query = '''
        UPDATE Loan
        SET returndate = %s
        WHERE lid = %d
        '''
        values = (selectedDate, self.loanID)
        cursor.execute(query, values)

        connect.commit()

        # mssql 연결 끊기
        cursor.close()
        connect.close()

        self.signal.emit()

        QMessageBox.information(self, INFORMATION_MESSAGE, PROLONG_RETURN_DATE_MESSAGE, QMessageBox.StandardButton.Ok)