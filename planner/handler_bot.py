import requests
from django.conf import settings

bot_token = settings.TOKEN
proxy_url = settings.PROXY_URL

url = f'{proxy_url}{bot_token}/sendMessage'

def sendMessageTG(user_id, message_text):
    if user_id:
        params = {
            'chat_id': int(user_id),
            'text': message_text
        }
        print(params)
        response = requests.post(url, json=params)
