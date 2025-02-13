import sys
import main  # main.py에서 실행 함수 가져오기
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

class ChromeDriverThread(QThread):
    status_signal = pyqtSignal(str)

    def __init__(self, target_func):
        super().__init__()
        self.target_func = target_func

    def run(self):
        result = self.target_func()  # main.py의 실행 함수 호출
        self.status_signal.emit(result)

class ChromeLauncherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chrome 드라이버 실행')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Chrome 드라이버 실행 프로그램')
        layout.addWidget(self.label)

        self.naver_button = QPushButton('네이버 실행')
        self.naver_button.clicked.connect(self.run_naver)
        layout.addWidget(self.naver_button)

        self.vejoa_button = QPushButton('배조아 실행')
        self.vejoa_button.clicked.connect(self.run_vejoa)
        layout.addWidget(self.vejoa_button)

        self.setLayout(layout)

    def run_naver(self):
        """네이버 실행 버튼 클릭 시 실행"""
        self.naver_thread = ChromeDriverThread(main.run_naver)
        self.naver_thread.status_signal.connect(self.update_status)
        self.naver_thread.start()

    def run_vejoa(self):
        """배조아 실행 버튼 클릭 시 실행"""
        self.vejoa_thread = ChromeDriverThread(main.run_vejoa)
        self.vejoa_thread.status_signal.connect(self.update_status)
        self.vejoa_thread.start()

    def update_status(self, message):
        """실행 상태 업데이트"""
        self.label.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChromeLauncherApp()
    ex.show()
    sys.exit(app.exec_())
