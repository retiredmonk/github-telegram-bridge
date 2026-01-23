import requests
from config import CHAT_ID, TELEGRAM_URL, TIMEOUT

def notify(message: str):

    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }

    response = requests.post(TELEGRAM_URL, data=payload, timeout=TIMEOUT)
    response.raise_for_status()