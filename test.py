import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

class MainWindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindowClass")
        self.show()  # 현재 창을 보이게 함

    def open_other_window(self):
        self.close()  # 현재 창 닫기
        self.other_window = MainWindowClass2()  # MainWindowClass2 인스턴스 생성
        self.other_window.show()  # MainWindowClass2 창 보이기

class MainWindowClass2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindowClass2")

class MainApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.main_window = MainWindowClass()

    def run(self):
        self.main_window.open_other_window()  # 다른 창 열기
        sys.exit(self.exec())

if __name__ == "__main__":
    app = MainApplication(sys.argv)
    app.run()
