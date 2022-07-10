import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QVBoxLayout, QApplication, QGraphicsOpacityEffect, QHBoxLayout)
from PyQt5.QtGui import QFont


class Flag:
    REST: str = 'rest'
    WORK: str = 'work'


class Focus(QWidget):
    period = 60
    total_seconds: int = 0
    work_times: int = 0
    flag: str
    start_flag: int = 0

    # settings
    long_rest_after_times: int = 4
    work_seconds: int = 25 * period
    rest_seconds: int = 5 * period
    long_rest_seconds: int = 15 * period

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        create the ui or reflash the ui
        :return:
        """
        self.showFullScreen()
        self.setWindowTitle('Yan Focus!!!')
        self.setStyleSheet("background-color:#000000;")
        self.show()

        self.lcd = QLabel()
        self.lcd.setAlignment(Qt.AlignCenter)
        self.lcd.setText('燕燕儿, 新的一天开始啦~\n 今天也要记得保护眼睛哦~.~')
        lcd_font = QFont()
        lcd_font.setPointSize(90)
        self.lcd.setFont(lcd_font)

        self.start_btn = QPushButton('开始工作!', self)
        btn_font = QFont()
        btn_font.setPointSize(40)
        self.start_btn.setFont(btn_font)
        self.start_btn.clicked.connect(self.start_to_work)

        #start button
        self.skip_sleep_btn = QPushButton('开工!', self)
        self.skip_sleep_btn.clicked.connect(self.work)
        self.skip_sleep_btn.setFont(btn_font)
        self.skip_sleep_btn.hide()

        #parse button
        self.exit_btn = QPushButton('退出', self)
        self.exit_btn.setFont(btn_font)
        self.exit_btn.clicked.connect(self.exit)

        btn_box = QHBoxLayout()
        btn_box.addWidget(self.start_btn)
        btn_box.addWidget(self.skip_sleep_btn)
        btn_box.addWidget(self.exit_btn)
        btn_weight = QWidget()
        btn_weight.setLayout(btn_box)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)
        vbox.addWidget(btn_weight)
        self.setLayout(vbox)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)

    def show_time(self):
        if not self.start_flag:
            return
        self.total_seconds -= 1
        op = QGraphicsOpacityEffect()
        if self.total_seconds > 0:
            minutes = self.total_seconds // 60
            seconds = self.total_seconds % 60
            self.lcd.setText(f'燕燕儿, {"快去休息" if self.flag == Flag.REST else "继续工作"}吧~. {str(minutes).zfill(2)}:{str(seconds).zfill(2)}')
        elif self.flag == Flag.WORK:
            self.rest()
        else:
            self.lcd.setText(f'燕燕儿, 开始新的工作吧~')

    def start_to_work(self):
        self.start_flag = 1
        self.start_btn.hide()
        self.skip_sleep_btn.show()
        self.work()

    def work(self):
        self.flag = Flag.WORK
        self.work_times += 1
        self.window().showMinimized()
        self.total_seconds = self.work_seconds

    def rest(self):
        self.flag = Flag.REST
        self.window().showFullScreen()
        need_long_rest = self.work_times % self.long_rest_after_times == 0
        self.total_seconds = self.long_rest_seconds if need_long_rest else self.rest_seconds

    def exit(self):
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Focus()
    sys.exit(app.exec_())
