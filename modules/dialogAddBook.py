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
form_class = uic.loadUiType(funcs.resourcePath(DIALOG_ADD_BOOK))[0]

class AddBookDialogClass(QDialog, form_class):
    acceptSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.comboBoxCategory.addItems(ADD_BOOK_CATEGORY_TUPLE)

        ## ==================== 위젯 연결 ==================== ##
        self.lineEditBookName: QLineEdit
        self.lineEditWriter: QLineEdit
        self.lineEditPublisher: QLineEdit
        self.dateEditPubDate:QDateEdit
        self.comboBoxCategory: QComboBox
        self.spinBoxQuantity: QSpinBox
        self.buttonBoxAccept: QDialogButtonBox

        ## ==================== 시그널 연결 ==================== ##
        self.buttonBoxAccept.accepted.connect(self.addBookFunc)
        

    ## ==================== 함수 ==================== ##
    def addBookFunc(self):
        # 입력 값 추출
        bookName = self.lineEditBookName.text()
        writer = self.lineEditWriter.text()
        publisher = self.lineEditPublisher.text()
        pubDate = self.dateEditPubDate.date()
        # 날짜를 쿼리를 위해 문자열 형식으로 변환
        strPubDate = pubDate.toString("yyyy-MM-dd")
        category = self.comboBoxCategory.currentText()
        # 카테고리 설정 안하는 경우를 대비
        if category == ADD_BOOK_CATEGORY_TUPLE[0]:
            category = ''
        quantity = self.spinBoxQuantity.value()

        # 미입력 항목 존재 시
        if bookName == "" or writer == "" or publisher == "":
            self.acceptSignal.emit(ADD_BOOK_ERROR_NO_INPUT)
            return
        
        # db 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 중복 도서 확인
        query = "SELECT * FROM Book WHERE bookname = %s"
        values = (bookName, )
        cursor.execute(query, values)
        bookInfo = cursor.fetchall()

        # 중복 도서 발견 시 조치
        if len(bookInfo) != 0:
            reply = QMessageBox.question(self, INFORMATION_MESSAGE, ADD_BOOK_INFO_SAME_BOOK, 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                pass
            else:
                cursor.close()
                connect.close()
                return
            
        # 도서 추가하는 쿼리
        query = '''
        INSERT INTO Book (bookname, writer, publisher, pubdate, category, quantity) 
        VALUES (%s, %s, %s, %s, %s, %d);
        '''
        values = (bookName, writer, publisher, strPubDate, category, quantity)
        cursor.execute(query, values)
        connect.commit()

        # mssql 연결 해제
        cursor.close()
        connect.close()

        self.acceptSignal.emit(ADD_BOOK_SUCCESS)
