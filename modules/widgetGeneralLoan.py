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

import modules.dialogProlongLoan as dialogProlongLoan
    
# ui 연결 변수
form_class = uic.loadUiType(funcs.resourcePath(WIDGET_GENERAL_LOAN))[0]



class GeneralLoanWidgetClass(QWidget, form_class):
    def __init__(self, userInfo):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.userInfo = userInfo
        # 트리 위젯에서 선택한 항목
        self.selectLoan: list = None
        
        self.LoanListRefresh()

        ## ==================== 위젯 연결 ==================== ##
        self.treeWidgetLoanList: QTreeWidget
        self.pushButtonBookReturn: QPushButton
        self.pushButtonBookProlong: QPushButton

        ## ==================== 시그널 연결 ==================== ##
        self.treeWidgetLoanList.itemClicked.connect(self.selectItemFunc)
        self.pushButtonBookReturn.clicked.connect(self.returnBookFunc)
        self.pushButtonBookProlong.clicked.connect(self.prologBookFunc)

    ## ==================== 함수 ==================== ##
    # 대출 리스트 위젯 새로고침 함수
    def LoanListRefresh(self):
        self.treeWidgetLoanList.clear()

        # mssql 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 대출 테이블에서 대출 도서 찾기 쿼리
        query = '''
        SELECT bookname, loandate, returndate, returnstatus, lid
        FROM Loan, Book
        WHERE Loan.bid = Book.bid
        AND Loan.uid = %s
        ORDER BY loandate DESC, lid DESC
        '''
        values = (self.userInfo[0], )
        cursor.execute(query, values)

        row = cursor.fetchone()

        while row:
            # 트리 위젯에 각 레코드를 추가하고, 비밀 데이터 lid를 추가함.
            item = QTreeWidgetItem(self.treeWidgetLoanList, [str(row[0]), row[1].strftime("%Y-%m-%d"), row[2].strftime("%Y-%m-%d"), row[3]])
            item.setData(0, Qt.ItemDataRole.UserRole, row[4])
            # print(item.data(0, Qt.ItemDataRole.UserRole)) 비밀 데이터 lid 추출 방법
            row = cursor.fetchone()

        # mssql 연결 끊기
        cursor.close()
        connect.close()


    # 트리 위젯에서 항목 선택 시 실행 함수
    def selectItemFunc(self, item):
        self.selectLoan = [item.data(0, Qt.ItemDataRole.UserRole), 
                           item.text(0), item.text(1), item.text(2), item.text(3)]
        
        # 이미 반납 된 책이면 버튼 비활성화
        if self.selectLoan[4] == LOAN_RETURNED:
            self.pushButtonBookReturn.setEnabled(False)
            self.pushButtonBookProlong.setEnabled(False)
        else:
            self.pushButtonBookReturn.setEnabled(True)
            self.pushButtonBookProlong.setEnabled(True)


    # 도서 반납 시 실행 함수
    def returnBookFunc(self):
        reply = QMessageBox.question(self, INFORMATION_MESSAGE, LOAN_RETURN_QUESTION % self.selectLoan[1], 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # mssql 연결
            connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
            cursor = connect.cursor()

            # 반납하는 쿼리
            query = '''
            UPDATE Loan
            SET returnstatus = %s
            WHERE lid = %d
            '''
            values = (LOAN_RETURNED, self.selectLoan[0])
            cursor.execute(query, values)


            # 도서 재고 + 1 추가
            query = '''
            SELECT Book.bid, quantity
            FROM Book, Loan
            WHERE Book.bid = Loan.bid
            AND lid = %d
            '''
            values = (self.selectLoan[0], )
            cursor.execute(query, values)

            selectBid, selectQuantity = cursor.fetchone()
            selectQuantity = selectQuantity + 1

            query = '''
            UPDATE Book
            SET quantity = %d
            WHERE bid = %d
            '''
            values = (selectQuantity, selectBid)
            cursor.execute(query, values)

            connect.commit()

            # mssql 연결 끊기
            cursor.close()
            connect.close()

            self.LoanListRefresh()
            self.pushButtonBookReturn.setEnabled(False)
            self.pushButtonBookProlong.setEnabled(False)
        else:
            pass

    # 도서 연장하기 시 작동 함수
    def prologBookFunc(self):
        self.prolongLoan = dialogProlongLoan.ProlongLoanDialogClass(self.selectLoan)
        self.prolongLoan.signal.connect(self.LoanListRefresh)
        self.prolongLoan.show()