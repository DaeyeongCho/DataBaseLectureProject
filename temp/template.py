import pymssql

# PyQt6 모듈
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon

# 사용자 모듈
import modules.functions as funcs
from defines.paths import *
from defines.strings import *
    
# ui 연결 변수
form_class = uic.loadUiType(funcs.resourcePath('ui 파일 경로'))[0]



class WidgetManagerBook(QWidget, form_class):
    def __init__(self):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resourcePath(ICON_PATH))) # 아이콘 임포트

        ## ==================== 위젯 연결 ==================== ##


        ## ==================== 시그널 연결 ==================== ##


    ## ==================== 함수 ==================== ##








        # mssql 검색 연결
        connect = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset=CHARSET_SELECT)
        cursor = connect.cursor()

        # 입력한 아이디가 이미 존재하는 지 확인하는 쿼리 실행
        query = "SELECT * FROM  WHERE %s ;"
        values = ('값 리스트', )
        cursor.execute(query, values)

        get = cursor.fetchall()

        # mssql 연결 끊기
        cursor.execute(query, values)
        connect.commit()