import os
import sys
import requests
import json

client_id = "cChJtyEvQH5aVcxJ2GCz"
client_secret = "eUmgWAYvwO"
celebrity_url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식
files = {'image': open('슴성_거니.png', 'rb')}
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }


celebrity_response = requests.post(celebrity_url,  files=files, headers=headers)
celebrity_rescode = celebrity_response.status_code


if(celebrity_rescode==200):
    celebrity_data = json.loads(celebrity_response.text)
else:
    print("Error Code:" + celebrity_rescode)
