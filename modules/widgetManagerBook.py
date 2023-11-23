import pymssql

# PyQt6 모듈
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# 사용자 모듈
import modules.functions as funcs
from defines.paths import *
from defines.strings import *

import modules.dialogAddBook as dialogAddBook
import modules.dialogModifyBook as dialogModify
    
# ui 연결 변수
form_class = uic.loadUiType(funcs.resourcePath(WIDGET_MANAGER_BOOK))[0]



class ManagerBookWidgetClass(QWidget, form_class):
    def __init__(self):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        # 선택 도서 정보
        self.selectedBookID: int = None
        self.selectedBookName: str = None

        self.comboBoxDetails.addItems(BOOK_DETAILS_TUPLE_MESSAGE)
        self.comboBoxCategory.addItems(BOOK_CATEGORY_TUPLE)
        self.comboBoxDetails.removeItem(4)

        self.showBookList()

        ## ==================== 위젯 연결 ==================== ##
        self.listWidgetBooks: QListWidget
        self.comboBoxDetails: QComboBox
        self.comboBoxCategory: QComboBox
        self.lineEditSearch: QLineEdit
        self.pushButtonSearch: QPushButton
        self.pushButtonAddBook: QPushButton
        self.pushButtonModifyBook: QPushButton
        self.pushButtonDeleteBook: QPushButton
        self.labelDetailInfo: QLabel

        ## ==================== 시그널 연결 ==================== ##
        self.pushButtonSearch.clicked.connect(self.showBookList)
        self.listWidgetBooks.itemClicked.connect(self.showDetailInfo)
        self.pushButtonAddBook.clicked.connect(self.viewBookAddDialog)
        self.pushButtonModifyBook.clicked.connect(self.viewBookModifyDialog)
        self.pushButtonDeleteBook.clicked.connect(self.deleteBookFunc)

    ## ==================== 함수 ==================== ##
    # 책 검색하여 리스트 위젯에 표시
    def showBookList(self):
        # 리스트 위젯 초기화
        self.listWidgetBooks.clear()

        # 입력 값 추출
        bookDetail = BOOK_DETAILS_TUPLE[self.comboBoxDetails.currentIndex()] # 컬럼명 추출
        bookCategory = self.comboBoxCategory.currentText() # 카테고리 추출
        if bookCategory == BOOK_CATEGORY_TUPLE[0]: # 카테고리가 전체이면 쿼리 X
            bookCategory = ""
        else:
            bookCategory = f" AND category = '{bookCategory}'"

        searchValue = self.lineEditSearch.text() # 텍스트박스 입력 값 추출

        # mssql 검색 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 모든 책을 입력 값에 따라 도서명 오름차순으로 출력하는 쿼리
        query = f'''
        SELECT * 
        FROM Book 
        WHERE {bookDetail} LIKE '%{searchValue}%'
        {bookCategory}
        ORDER BY bookname ASC;
        '''
        cursor.execute(query)

        num = 1
        row = cursor.fetchone() # 쿼리 결과의 다음 행을 가져와 리턴
        while row:
            item = QListWidgetItem(str(num) + ". " + row[1]) # 아이템의 문구
            item.setData(Qt.ItemDataRole.UserRole, row[0]) # 아이템 도서의 bid를 안보이게 저장
            self.listWidgetBooks.addItem(item)
            row = cursor.fetchone()
            num = num + 1

        # mssql 연결 끊기
        cursor.close()
        connect.close()


    # 리스트 위젯에서 도서 클릭 시 상세정보 표시
    def showDetailInfo(self, item: QListWidgetItem):
        # mssql 검색 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 도서 1권 검색 쿼리
        query = '''
        SELECT *
        FROM Book
        WHERE bid = %d
        '''
        values = (item.data(Qt.ItemDataRole.UserRole), )
        cursor.execute(query, values)

        row = cursor.fetchone()

        # 검색 된 도서 정보 출력
        printInfo = f'''
        {BOOK_DETAILS_TUPLE_MESSAGE[0]}: {row[1]}
        {BOOK_DETAILS_TUPLE_MESSAGE[1]}: {row[2]}
        {BOOK_DETAILS_TUPLE_MESSAGE[2]}: {row[3]}
        {BOOK_DETAILS_TUPLE_MESSAGE[3]}: {row[4]}
        {BOOK_DETAILS_TUPLE_MESSAGE[4]}: {row[5]}
        {BOOK_DETAILS_TUPLE_MESSAGE[5]}: {row[6]}
        '''
        self.labelDetailInfo.setText(printInfo)

        # 도서 수정, 삭제 버튼 활성화
        self.pushButtonModifyBook.setEnabled(True)
        self.pushButtonDeleteBook.setEnabled(True)

        # 멤버 변수에 도서 정보 저장
        self.selectedBookID = row[0]
        self.selectedBookName = row[1]

    # 도서 추가 시 작동 함수
    def viewBookAddDialog(self):
        self.addBookDialog = dialogAddBook.AddBookDialogClass()
        self.addBookDialog.acceptSignal.connect(self.getBookAddAcceptSignal)
        self.addBookDialog.show()

    # 도서 추가 확인 버튼 클릭 시 작동 함수
    def getBookAddAcceptSignal(self, getStr):
        if getStr == ADD_BOOK_ERROR_NO_INPUT:
            QMessageBox.information(self, WARNING_MESSAGE, getStr, QMessageBox.StandardButton.Ok)
        elif getStr == ADD_BOOK_SUCCESS:
            QMessageBox.information(self, INFORMATION_MESSAGE, getStr, QMessageBox.StandardButton.Ok)
            self.showBookList()

    # 도서 수정 시 작동 함수
    def viewBookModifyDialog(self):
        self.modifyBookDialog = dialogModify.ModifyBookDialogClass(self.selectedBookID)
        self.modifyBookDialog.acceptSignal.connect(self.bookModifySignal)
        self.modifyBookDialog.show()

    def bookModifySignal(self, getStr):
        if getStr == MODIFY_BOOK_SUCCESS:
            QMessageBox.information(self, INFORMATION_MESSAGE, getStr, QMessageBox.StandardButton.Ok)
            self.showBookList()
            self.pushButtonModifyBook.setEnabled(False)
            self.pushButtonDeleteBook.setEnabled(False)
            self.labelDetailInfo.setText("")

    # 도서 삭제 시 작동 함수
    def deleteBookFunc(self):
        reply = QMessageBox.question(self, INFORMATION_MESSAGE, DELETE_BOOK_QUESTION_MESSAGE % self.selectedBookName, 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                    QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # db 연결
            connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
            cursor = connect.cursor()

            query = '''
            SELECT *
            FROM Loan
            WHERE bid = %d
            '''
            values = (self.selectedBookID, )
            cursor.execute(query, values)

            get = cursor.fetchall()
            
            # 해당 도서를 빌리고 있는 회원 존재 시 무결성을 위해 도서 삭제 불가능
            if len(get) != 0:
                QMessageBox.information(self, WARNING_MESSAGE, DELETE_BOOK_ERROR_ON_LOAN, QMessageBox.StandardButton.Ok)
                cursor.close()
                connect.close()
                return

            # 도서를 삭제하는 쿼리
            query = '''
            DELETE FROM Book
            WHERE bid = %d
            '''
            values = (self.selectedBookID, )
            cursor.execute(query, values)

            connect.commit()

            # mssql 연결 끊기
            cursor.close()
            connect.close()
            
            QMessageBox.information(self, INFORMATION_MESSAGE, DELETE_SUCCESS_MESSAGE, QMessageBox.StandardButton.Ok)
            self.showBookList()
            # 도서 수정, 삭제 버튼 비활성화
            self.pushButtonModifyBook.setEnabled(False)
            self.pushButtonDeleteBook.setEnabled(False)
            self.labelDetailInfo.setText("")