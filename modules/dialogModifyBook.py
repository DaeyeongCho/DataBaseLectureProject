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
form_class = uic.loadUiType(funcs.resourcePath(DIALOG_MODIFY_BOOK))[0]

class ModifyBookDialogClass(QDialog, form_class):
    acceptSignal = pyqtSignal(str)

    def __init__(self, bid):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        self.bid = bid

        # mssql 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
        cursor = connect.cursor()

        # 쿼리 실행
        query = '''
        SELECT *
        FROM Book
        WHERE bid = %d
        '''
        values = (bid, )
        cursor.execute(query, values)

        row = cursor.fetchone()

        # mssql 연결 끊기
        cursor.close()
        connect.close()

        # 불러온 책의 값을 위젯에 적용
        self.lineEditBookName.setText(row[1])
        self.lineEditWriter.setText(row[2])
        self.lineEditPublisher.setText(row[3])
        # datetime.date() 형식의 날짜 값을 QDate()의 날짜 값으로 변환
        qDate = QDate(row[4].year, row[4].month, row[4].day)
        self.dateEditPubDate.setDate(qDate)
        # 카테고리 콤보 박스에서 해당하는 값을 찾아 설정
        self.comboBoxCategory.addItems(ADD_BOOK_CATEGORY_TUPLE)
        index = self.comboBoxCategory.findText(row[5])
        self.comboBoxCategory.setCurrentIndex(index)
        self.spinBoxQuantity.setValue(row[6])
        

        ## ==================== 위젯 연결 ==================== ##
        self.lineEditBookName: QLineEdit
        self.lineEditWriter: QLineEdit
        self.lineEditPublisher: QLineEdit
        self.dateEditPubDate: QDateEdit
        self.comboBoxCategory: QComboBox
        self.spinBoxQuantity: QSpinBox
        self.buttonBoxAccept: QDialogButtonBox

        ## ==================== 시그널 연결 ==================== ##
        self.buttonBoxAccept.accepted.connect(self.modifyBookData)

    ## ==================== 함수 ==================== ##
    def modifyBookData(self):
        reply = QMessageBox.question(self, INFORMATION_MESSAGE, MODIFY_BOOK_QUESTION_MESSAGE,  
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                    QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            bookName = self.lineEditBookName.text()
            writer = self.lineEditWriter.text()
            publisher = self.lineEditPublisher.text()
            pubDate = self.dateEditPubDate.date().toString("yyyy-MM-dd")
            category = self.comboBoxCategory.currentText()
            quantity = self.spinBoxQuantity.value()

            # mssql 연결
            connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET)
            cursor = connect.cursor()

            # 쿼리 실행
            query = '''
            UPDATE Book
            SET bookname = %s, writer = %s, publisher = %s, pubdate = %s, category = %s, quantity = %d
            WHERE bid = %d
            '''
            values = (bookName, writer, publisher, pubDate, category, quantity, self.bid)
            cursor.execute(query, values)

            connect.commit()

            # mssql 연결 끊기
            cursor.close()
            connect.close()
            
            self.acceptSignal.emit(MODIFY_BOOK_SUCCESS)