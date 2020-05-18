#데이터 저장하기 창 관련 코드

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

class WindowsaveClass(QDialog) :
    def __init__(self, WindowClass) :
        super(WindowsaveClass,self).__init__(WindowClass)
        save_ui = "save_ui.ui"
        uic.loadUi(save_ui,self)
        self.show()
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('데이터 저장하기')

        self.confirm_btn.clicked.connect(self.push_confirm)
        self.cancle_btn.clicked.connect(self.push_exit)

        self.check = False

    def push_confirm(self) :
        if self.id_line.text() == "" :
            self.sign_lable.setText("▲아이디를 입력해주세요")
            self.sign_lable.setStyleSheet("Color : red")
        else :
            self.id = self.id_line.text()
            self.check = True
            self.close()

    def push_exit(self) :
        self.close()
