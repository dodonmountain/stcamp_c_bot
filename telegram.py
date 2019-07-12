import requests
import pprint
import urllib
from decouple import config #환경 변수 관리 패키지

token = config('TELEGRAM_TOKEN') #.env 설정값 가져오기
base_url = f'https://api.telegram.org/bot{token}/'
# pprint.pprint(response)

# 2.  get Updates 정보 가져오기

response = requests.get(base_url + 'getUpdates').json()

# 3. 나의 chat id 가져오기

my_chat_id = response['result'][0]['message']['from']['id']
# = > 858384799
# print(my_chat_id)

ms = '12124124'
# 4-1. 요청보낼 url 만들기
api_url = f'{base_url}sendMessage?chat_id={my_chat_id}&text={ms}'
requests.get(api_url)