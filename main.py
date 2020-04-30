import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

import celebrity_ai_api
import face_ai_api


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("main_ui.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #버튼에 기능을 연결하는 코드
        self.search_btn.clicked.connect(self.search)
        self.init_btn.clicked.connect(self.init)
        
    # '초기화' 버튼을 누르면 작동
    def init(self) :
        self.sex_value.setText("")
        self.sex_accuracy_value.setText("")
        self.age_value.setText("")
        self.age_accuracy_value.setText("")
        self.emotion_value.setText("")
        self.emotion_accuracy_value.setText("")
        self.pose_value.setText("")
        self.pose_accuracy_value.setText("")
        
        self.celebrity_num_value.setText("")
        self.celebrity_name1_value.setText("")
        self.celebrity_accuracy1_value.setText("")
        self.celebrity_name2_value.setText("")
        self.celebrity_accuracy2_value.setText("")
        self.celebrity_name3_value.setText("")
        self.celebrity_accuracy3_value.setText("")
    
    # '얼굴조사하기' 버튼을 누르면 작동
    def search(self) :
        face_data = face_ai_api.face_data
        celebrity_data = celebrity_ai_api.celebrity_data

        qPixmapVar = QPixmap()
        qPixmapVar.load('슴성_거니.png')
        qPixmapVar = qPixmapVar.scaled(400,500)
        self.photoView.setPixmap(qPixmapVar)
        
        print(face_data)
        print(celebrity_data)

        sex = {'male' : '남성', 'female' : '여자'}
        
        emotion = {
            'angry':'화남', 'disgust':'혐오', 'fear' : '공포',
            'laugh' : '환한 웃음', 'neutral' : '평온', 'sad' : '슬픔', 'surprise' : '놀람',
            'smile' : '미소', 'talking' : '말하는'
            }

        pose = {
            'part_face' : '얼굴 일부', 'false_face' : '얼굴이 아님', 'sunglasses' : '안경을 쓴 얼굴', 'frontal_face' : '정면 얼굴',
            'left_face' : '왼쪽 얼굴', 'right_face' : '오른쪽 얼굴', 'rotate_face' : '회전 된 얼굴'
            }

        self.sex_value.setText(sex[face_data['faces'][0]['gender']['value']])
        self.sex_accuracy_value.setText( str(face_data['faces'][0]['gender']['confidence'] * 100) + ' %')

        self.age_value.setText(face_data['faces'][0]['age']['value'] + ' 세')
        self.age_accuracy_value.setText( str(face_data['faces'][0]['age']['confidence'] * 100) + ' %')

        self.emotion_value.setText(emotion[face_data['faces'][0]['emotion']['value']])
        self.emotion_accuracy_value.setText( str(face_data['faces'][0]['emotion']['confidence'] * 100) + ' %')

        self.pose_value.setText(pose[face_data['faces'][0]['pose']['value']])
        self.pose_accuracy_value.setText( str(face_data['faces'][0]['pose']['confidence'] * 100) + ' %')
        
        self.celebrity_num_value.setText( str(len(celebrity_data['faces'])))

        
        if len(celebrity_data['faces']) == 1 :
            self.celebrity_name1_value.setText(celebrity_data['faces'][0]['celebrity']['value'])
            self.celebrity_accuracy1_value.setText( str( celebrity_data['faces'][0]['celebrity']['confidence'] * 100) + ' %')
        
        elif len(celebrity_data['faces']) == 2 :
            self.celebrity_name1_value.setText(celebrity_data['faces'][0]['celebrity']['value'])
            self.celebrity_accuracy1_value.setText( str( celebrity_data['faces'][0]['celebrity']['confidence'] * 100) + ' %')
            self.celebrity_name2_value.setText(celebrity_data['faces'][1]['celebrity']['value'])
            self.celebrity_accuracy2_value.setText( str( celebrity_data['faces'][1]['celebrity']['confidence'] * 100) + ' %')
         
        else :
            self.celebrity_name1_value.setText(celebrity_data['faces'][0]['celebrity']['value'])
            self.celebrity_accuracy1_value.setText( str( celebrity_data['faces'][0]['celebrity']['confidence'] * 100) + ' %')
            self.celebrity_name2_value.setText(celebrity_data['faces'][1]['celebrity']['value'])
            self.celebrity_accuracy2_value.setText( str( celebrity_data['faces'][1]['celebrity']['confidence'] * 100) + ' %')
            self.celebrity_name3_value.setText(celebrity_data['faces'][2]['celebrity']['value'])
            self.celebrity_accuracy3_value.setText( str( celebrity_data['faces'][2]['celebrity']['confidence'] * 100) + ' %')


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()