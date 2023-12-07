import pymssql
from datetime import datetime

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
form_class = uic.loadUiType(funcs.resourcePath(DIALOG_LOAN_BOOK))[0]


class LoanBookDialogClass(QDialog, form_class):
    acceptSignal = pyqtSignal(str)

    def __init__(self, bid: int, bookname: str, uid: str):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.bid = bid
        self.bookName = bookname
        self.uid = uid

        # 대출 가능 기간 범위 설정. 현재로부터 LOAN_PERMISSION_RANGE까지
        self.currentDateQ = QDate.currentDate()
        self.afterWeekDateQ = self.currentDateQ.addDays(LOAN_PERMISSION_RANGE)
        
        self.calendarWidgetReturnDate.setMinimumDate(self.currentDateQ)
        self.calendarWidgetReturnDate.setMaximumDate(self.afterWeekDateQ)

        ## ==================== 위젯 연결 ==================== ##
        self.labelBookName: QLabel
        self.calendarWidgetReturnDate: QCalendarWidget
        self.buttonBoxAccept: QDialogButtonBox

        ## ==================== 시그널 연결 ==================== ##
        self.buttonBoxAccept.accepted.connect(self.loanBookFunc)

    ## ==================== 함수 ==================== ##
    def loanBookFunc(self):
                # mssql 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 회원의 연체 도서 유무 검색
        query = '''
        SELECT lid
        FROM Loan
        WHERE uid = %s
        AND returndate < %s
        AND returnstatus = %s
        '''
        values = (self.uid, datetime.now().strftime("%Y-%m-%d"), LOAN_NOT_RETURN)
        cursor.execute(query, values)
        get = cursor.fetchall()

        if len(get) != 0:
            self.acceptSignal.emit(LOAN_ERROR_ARREARS)
            return

        # 현재 책의 재고가 있는지 확인하는 쿼리 실행
        query = '''
        SELECT quantity
        FROM Book
        WHERE bid = %d
        '''
        values = (self.bid, )
        cursor.execute(query, values)

        row = cursor.fetchone()


        if 0 < row[0]:
            loanDate = datetime.now().strftime("%Y-%m-%d")
            returnDate = self.calendarWidgetReturnDate.selectedDate().toString("yyyy-MM-dd")
            newQuantity = row[0] - 1
            
            # 도서 대출 쿼리 실행
            query = '''
            INSERT INTO Loan (uid, bid, loandate, returndate, returnstatus) 
            VALUES (%s, %d, %s, %s, %s);
            '''
            values = (self.uid, self.bid, loanDate, returnDate, LOAN_NOT_RETURN)
            cursor.execute(query, values)

            connect.commit()

            # 재고 - 1 쿼리
            query = '''
            UPDATE Book
            SET quantity = %d
            WHERE bid = %d;
            '''
            values = (newQuantity, self.bid)

            cursor.execute(query, values)

            connect.commit()

            self.acceptSignal.emit(LOAN_SUCCESS)
        else:
            self.acceptSignal.emit(LOAN_ERROR_NO_QUANTITY)

        # mssql 연결 끊기
        cursor.close()
        connect.close()