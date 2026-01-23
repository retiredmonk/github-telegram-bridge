import logging
import random
import time
import requests
from config import CHAT_ID, TELEGRAM_URL, TIMEOUT, MAX_RETRIES, BACKOFF_BASE

def notify(message: str):
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(
                TELEGRAM_URL,
                data=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            logging.info("Telegram notification sent successfully")
            return

        except requests.exceptions.RequestException as e:
            wait = random.uniform(0, BACKOFF_BASE * 2 ** attempt )
            logging.warning(
                f"Telegram send failed (attempt {attempt}/{MAX_RETRIES}): {e}. "
                f"Retrying in {wait}s..."
            )
            time.sleep(wait)

    logging.error("Failed to send Telegram message after retries")
