#이미지 출력 관련 (이미지 내 얼굴 표시 및 윈도우에 출력)

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import Qt, QCoreApplication

def face_draw(image_data,kind) :
    qp = QPixmap()
    
    if kind == "path" :
        qp.load(image_data[6])              #load는 경로를 사용해 이미지를 등록
    elif kind == "binary" :
        qp.loadFromData(image_data[6])      #loadFromData는 바이너리데이터를 사용해 이미지를 등록

    qp = qp.scaled(400,500)
    
    x,y,w,h = image_data[0:4]
    width, height = image_data[4:6]
    width_ratio = width / 400
    height_ratio = height / 500
    
    x = x / width_ratio
    y = y / height_ratio
    w = w / width_ratio
    h = h / height_ratio
    
        #비율 구하는 법
        # 기존비율 가로1:세로1  , 변경된 비율 가로2:세로2 인 경우
        # 가로1 / 가로2 = A , 세로1/A = 세로2가 나옴
        # 기존idx 가좌1 / A = 변좌1
        # 기존idx 세좌1 / A = 세좌1

    qPixpaint = QPainter(qp)
    qPixpaint.setPen(QPen(Qt.red, 3))
    qPixpaint.drawRect(x,y,w,h)
    qPixpaint.end()

    return qp


