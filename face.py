
import requests
from decouple import config
import pprint

# 1. 네이버 API 설정
def yourface(pic):
    file_url = f'{pic}'
    response = requests.get(file_url, stream = True)
    image = response.raw.read()

    naver_client_id = config('NAVER_CLIENT_ID')
    naver_client_secret = config('NAVER_CLIENT_SECRET')
    naver_url = 'https://openapi.naver.com/v1/vision/celebrity'
    headers = {'X-Naver-Client-Id': naver_client_id, 
            'X-Naver-Client-Secret': naver_client_secret}

    response = requests.post(naver_url,
                            headers = headers,
                            files = {'image': image}).json()
    if response.get('faces'):
        best = response.get('faces')[0].get('celebrity')
        if best.get('confidence')>0.2:
            text = f"{best.get('confidence')*100}만큼 {best.get('value')}를 닮으셨네요~"
            return text
        else:
            text = "연예인을 닮지 않으셨네요"
            return text
    else:
        text = "사람아님"
        return text
