import os
import sys
import requests
import json

client_id = "cChJtyEvQH5aVcxJ2GCz"
client_secret = "eUmgWAYvwO"
celebrity_url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식
files = {}
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }

def insert_file(url) :
    files['image'] = open(url,'rb')

def request_data() :
    celebrity_response = requests.post(celebrity_url,  files=files, headers=headers)
    celebrity_rescode = celebrity_response.status_code
    
    if(celebrity_rescode==200):
        celebrity_data = json.loads(celebrity_response.text)
        return celebrity_data
    else:
        print("Error Code:" + str(celebrity_rescode))
        return celebrity_rescode