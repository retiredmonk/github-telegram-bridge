import logging, random, time, requests
from env import get_settings

def notify(message: str):
    config = get_settings()

    url = f'https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage'
    payload = {
        "chat_id": config.CHAT_ID,
        "text": message
    }

    max_retries, base = 3, 2

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, data=payload, timeout=10)

            response.raise_for_status()
            logging.info("Telegram notification sent successfully")
            return

        except requests.exceptions.RequestException:

            wait = random.uniform(0, base * 2 ** attempt)
            logging.warning(
                f"Telegram notification failed, attempt: {attempt}/{max_retries}"
                f"Retrying in {wait}s..."
            )

            time.sleep(wait)

    logging.error("Failed to send Telegram message after maximum retries")
