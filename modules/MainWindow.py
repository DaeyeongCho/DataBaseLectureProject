# PyQt6 모듈
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon

# 사용자 모듈
from defines.paths import *
import modules.functions as funcs
    
# ui 연결 변수
form_class = uic.loadUiType(funcs.resource_path(MAIN_WINDOW_UI_PATH))[0]



class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(funcs.resource_path(ICON_PATH))) # 아이콘 임포트