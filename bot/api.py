import requests
from app.config import Config

config = Config()
TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN

def send_api_request(user_id, text, progress, image_url=None):
    if image_url:
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
        payload = {
            'chat_id': user_id,
            'photo': image_url,
            'caption': text,
            'parse_mode': 'HTML'  
        }
        response = requests.post(url, json=payload)
    else:
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        payload = {
            'chat_id': user_id,
            'text': text,
            'parse_mode': 'HTML' 
        }
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            progress['sent'] += 1
        elif response.status_code == 403:
            progress['blocked'] += 1
        else:
            progress['not_sent'] += 1
     
    return response.json()