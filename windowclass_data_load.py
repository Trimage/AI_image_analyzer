#데이터 불러오기 창 관련 코드

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

class WindowloadClass(QDialog) :
    def __init__(self, WindowClass) :
        super(WindowloadClass,self).__init__(WindowClass)
        load_ui = "load_ui.ui"
        uic.loadUi(load_ui,self)
        self.show()
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('데이터 불러오기')

        self.confirm_btn.clicked.connect(self.push_confirm)
        self.cancle_btn.clicked.connect(self.push_exit)

        self.check = False

    def push_confirm(self) :
        if self.date_line.text() == "" or self.id_line.text() == "" or self.num_line.text() == "" :
            self.sign_lable.setText("▲모든 칸을 입력해주세요.")
            self.sign_lable.setStyleSheet("Color : red")
        else :
            self.date = self.date_line.text()
            self.id = self.id_line.text()
            self.num = self.num_line.text()
            self.check = True
            self.close()

    def push_exit(self) :
        self.close()
