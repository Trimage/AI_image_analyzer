import os
import sys
import requests
import json

client_id = "cChJtyEvQH5aVcxJ2GCz"
client_secret = "eUmgWAYvwO"
face_url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
files = {'image': open('슴성_거니.png', 'rb')}
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }

face_response = requests.post(face_url,  files=files, headers=headers)
face_rescode = face_response.status_code


if(face_rescode==200):
    face_data = json.loads(face_response.text)
else:
    print("Error Code:" + face_rescode)