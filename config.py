import os
from pathlib import Path
from dotenv import load_dotenv

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR/"github.db"

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR/"github.log"

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
GITHUB_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')

GITHUB_URL = 'https://api.github.com'
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {GITHUB_TOKEN}',
    'User-Agent': 'github-telegram-bridge/1.0'
}

BACKOFF_BASE = 2
MAX_RETRIES = 3
TIMEOUT = 10

PARAMS = {
    'per_page': 5,
}
