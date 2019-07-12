import pprint
import requests
import random
from decouple import config
from flask import Flask, render_template, request
# 개인 모듈 로드
import papago
import face

app = Flask(__name__)
token = config('TELEGRAM_TOKEN')
base_url = f'https://api.telegram.org/bot{token}'

naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')
naver_url = 'https://openapi.naver.com/v1/papago/n2mt'


@app.route(f'/{token}', methods=['POST'])
def telegram():
    response = request.get_json()
    # 사진일 경우
    if response.get('message').get('photo'):
        chat_id = response.get('message').get('chat').get('id')
        # 사진 파일의 id를 가져온다.
        file_id = response.get('message').get('photo')[-1].get('file_id')
        # 텔레그램 서버에 파일의 경로를 받아온다.
        file_response = requests.get(f'{base_url}/getFile?file_id={file_id}').json()
        #파일 경로를 통해 url을 만든다.
        file_path = file_response.get('result').get('file_path')
        file_url = f'https://api.telegram.org/file/bot{token}/{file_path}' #파일 url
        text = face.yourface(file_url)
        api_url = f'{base_url}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(api_url)



    elif response.get('message'):
        text = response.get('message').get('text')
        chat_id = response.get('message').get('chat').get('id')
        # 번역모듈 로드==========================================================================================
        if '/번역 ' in text[0:4]:
            text = papago.papa(text[4:])

        # 인사===================================================================================================
        elif '안녕' in text or 'hi' in text:
            text = '안녕?안녕?안녕?안녕?'

        # 로또====================================================================================================

        elif '로또' in text:
            text = sorted(random.sample(range(1,46),6))

        # 피드백==================================================================================================

        api_url = f'{base_url}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(api_url)
    return '' , 200








if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host ='0.0.0.0', debug = True)
