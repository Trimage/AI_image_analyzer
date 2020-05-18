#도움말 창 관련 코드

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

class WindowhelpClass(QDialog) :
    def __init__(self, WindowClass) :
        super(WindowhelpClass,self).__init__(WindowClass)
        help_ui = "help_ui.ui"
        uic.loadUi(help_ui,self)
        self.show()
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('도움말')

        qPixmapicon = QPixmap()
        qPixmapicon.load('icon.png')
        qPixmapicon = qPixmapicon.scaled(100,100)
        
        self.icon_lable.setPixmap(qPixmapicon)
        self.icon_lable.show()

        self.exit_btn.clicked.connect(self.push_exit)

    def push_exit(self) :
        self.close()
