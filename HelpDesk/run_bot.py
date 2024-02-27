import requests
from django.conf import settings
bot_token = settings.TOKEN
bot_proxy = settings.PROXY_URL

def send_telegram_message(chat_id, text):
    api_url = f"{bot_proxy}{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(api_url, json=payload)
    return response.json()