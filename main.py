import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import Qt, QCoreApplication

from datetime import datetime

from windowclass_help import WindowhelpClass            #도움말 창 관련
from windowclass_data_save import WindowsaveClass       #데이터 저장하기 창 관련
from windowclass_data_load import WindowloadClass       #데이터 불러오기 창 관련
from draw_image import face_draw                        #이미지 출력 관련 (이미지 내 얼굴 표시 및 윈도우에 출력)

import celebrity_ai_api
import face_ai_api
import mysql_connection


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
main_form_class = uic.loadUiType("main_ui.ui")[0]


#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, main_form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('얼굴인식 프로그램')
        

        #버튼에 기능을 연결하는 코드
        self.search_btn.clicked.connect(self.search)
        self.init_btn.clicked.connect(self.init)
        self.insert_image_btn.clicked.connect(self.search_image)
        self.help_btn.clicked.connect(self.help)
        self.data_save_btn.clicked.connect(self.save_data)
        self.data_load_btn.clicked.connect(self.load_data)
        self.exit_btn.clicked.connect(QCoreApplication.instance().quit)

        self.photo_info = []    #이미지에 얼굴 표시 하는데 사용

        

    # '사진 찾기' 버튼을 누르면 작동
    def search_image(self):
        fname = QFileDialog.getOpenFileName(self)
        if fname[0] != "" : 
            self.file_name_edit.setText(fname[0])
            self.sign_lable.setText("")



    # '데이터 불러오기' 버튼을 누르면 작동
    def load_data(self) :
        load_dlg = WindowloadClass(self)
        load_dlg.exec_()

        if load_dlg.check is not True :
            return

        date = load_dlg.date
        id = load_dlg.id
        num =load_dlg.num

        person_data = mysql_connection.person_load(date,id,num)
        celeb_data = mysql_connection.celeb_load(date,id,num)


        if person_data == False or celeb_data == False :
            self.sign_lable.setText("등록되지 않은 데이터 값입니다.")
            self.sign_lable.setStyleSheet("Color : Red")

            self.data_info_lable.setText("")
            return

        self.sex_value.setText(person_data[3])
        self.sex_accuracy_value.setText(str(person_data[4]) + " %")
        self.age_value.setText(person_data[5])
        self.age_accuracy_value.setText(str(person_data[6]) + " %")
        self.emotion_value.setText(person_data[7])
        self.emotion_accuracy_value.setText(str(person_data[8]) + " %")
        self.pose_value.setText(person_data[9])
        self.pose_accuracy_value.setText(str(person_data[10]) + " %")

        self.celebrity_num_value.setText(str(celeb_data[3]))        
        self.celebrity_name1_value.setText(celeb_data[4])
        self.celebrity_accuracy1_value.setText(str(celeb_data[5]) + " %")
        self.celebrity_name2_value.setText(celeb_data[6])
        if celeb_data[7] != None :
            self.celebrity_accuracy2_value.setText(str(celeb_data[7]) + " %")
        else :
            self.celebrity_accuracy2_value.setText("")
        self.celebrity_name3_value.setText(celeb_data[8])
        if celeb_data[9] != None :
            self.celebrity_accuracy3_value.setText(str(celeb_data[9]) + " %")
        else :
            self.celebrity_accuracy3_value.setText("")
        

        image_data = mysql_connection.info_load(date,id,num)
        
        qp = face_draw(image_data,"binary")         #이미지 내 인물의 얼굴을 표시하여 반환

        self.photoView.setPixmap(qp)
        self.photoView.show()

        self.data_info_lable.setText("불러오기가 완료되었습니다.")



    # '데이터 저장하기' 버튼을 누르면 작동
    def save_data(self) :
        if self.sex_value.text() == "" :
            self.sign_lable.setText("얼굴조사하기를 먼저 실행해주세요.")
            self.sign_lable.setStyleSheet("Color : Red")
            
        else :
            save_dlg = WindowsaveClass(self)
            save_dlg.exec_()

            if save_dlg.check is not True :
                return

            id = save_dlg.id

            date = datetime.today().strftime("%Y-%m-%d")

            person_data = {'sex_value' : self.sex_value.text(),
                           'sex_accuracy' : self.sex_accuracy_value.text()[:-2],
                           'age_value' : self.age_value.text(),
                           'age_accuracy' : self.age_accuracy_value.text()[:-2],
                           'emotion_value' : self.emotion_value.text(),
                           'emotion_accuracy' : self.emotion_accuracy_value.text()[:-2],
                           'pose_value' : self.pose_value.text(),
                           'pose_accuracy' : self.pose_accuracy_value.text()[:-2]
                           }

            celeb_data = {'celeb_total' : self.celebrity_num_value.text(),
                           'celeb_name1' : self.celebrity_name1_value.text(),
                           'celeb_accuracy1' : self.celebrity_accuracy1_value.text()[:-2],
                           'celeb_name2' : self.celebrity_name2_value.text(),
                           'celeb_accuracy2' : self.celebrity_accuracy1_value.text()[:-2],
                           'celeb_name3' : self.celebrity_name3_value.text(),
                           'celeb_accuracy3' : self.celebrity_accuracy3_value.text()[:-2]
                           }

            num = mysql_connection.info_insert(date,id,self.photo_info)

            mysql_connection.person_insert(date,id,num,person_data)

            mysql_connection.celeb_insert(date,id,num,celeb_data)

            self.data_info_lable.setText("저장이 완료되었습니다\n저장 값 : {0} {1} {2}".format(date,id,num))

        

    # '도움말' 버튼을 누르면 작동
    def help(self) :
        WindowhelpClass(self)
        


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

        self.photoView.setText(" ")
        self.sign_lable.setText("")
        self.data_info_lable.setText("")



    # '얼굴조사하기' 버튼을 누르면 작동
    def search(self) :

        if self.file_name_edit.text() == "" :
            self.sign_lable.setText("※파일을 등록해주세요")
            self.sign_lable.setStyleSheet("Color : red")
            return 

        self.init()

        face_ai_api.insert_file(self.file_name_edit.text())
        celebrity_ai_api.insert_file(self.file_name_edit.text())
        
        face_data = face_ai_api.request_data()
        celebrity_data = celebrity_ai_api.request_data()

        error_msg = { 400 : "파일 오류입니다. 도움말을 확인해주세요.", 500 : "서버 오류입니다. 잠시 후 시도해주세요." }

        if face_data == 400 or face_data == 500 :
            self.sign_lable.setText(error_msg[face_data])
            self.sign_lable.setStyleSheet("Color : red")
            return

        if celebrity_data == 400 or celebrity_data == 500 :
            self.sign_lable.setText(error_msg[celebrity_data])
            self.sign_lable.setStyleSheet("Color : red")
            return 

        self.init()

        if face_data['info']['faceCount'] == 0 :
            self.photoView.setPixmap(qPixmapVar)
            self.sign_lable.setText("※발견 된 얼굴이 없습니다.")
            self.sign_lable.setStyleSheet("Color : red")
            return

        self.photo_info[0:3] = face_data['faces'][0]['roi'].values()
        self.photo_info[4:5] = face_data['info']['size'].values()
        self.photo_info = list(map(int,self.photo_info))       #문자열을 숫자로 전환

        self.photo_info.append(self.file_name_edit.text())


        qp = face_draw(self.photo_info,"path")

        self.photoView.setPixmap(qp)
        self.photoView.show()
        

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