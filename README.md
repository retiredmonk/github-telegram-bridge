# GitHub → Telegram Commit Monitor

A Python service that polls a GitHub repository for new commits and delivers instant Telegram notifications — with deduplication, retry logic, and structured logging.

## How It Works

GitHub REST API → Fetch latest commit → Check SQLite state → Notify via Telegram

## Setup

**1. Clone and create a virtual environment**
```bash
git clone https://github.com/retiredmonk/github-telegram-bridge.git
cd github-telegram-bridge
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate.bat       # Windows
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment** — create a `.env` file in the project root
```env
GITHUB_TOKEN=your_github_pat
TELEGRAM_TOKEN=your_bot_token
CHAT_ID=your_chat_id
OWNER=github-username
REPO=repository-name
POLL_INTERVAL=60
```

**4. Run**
```bash
python main.py
```

## Architecture

clients/github_client.py — GitHub REST API client with exponential backoff  
clients/telegram_client.py — Telegram Bot API dispatcher  
database/db.py — SQLite persistence and SHA deduplication  
services/monitor_pipeline.py — Orchestration logic  
services/message_builder.py — Notification formatter  
utils/errors.py — Custom exception types  
utils/logger.py — File + console logging  
env.py — Pydantic settings via .env  
main.py — Entry point  

## Key Design Decisions

- **Pydantic BaseSettings** — typed config loaded from .env, validated at startup
- **SQLite deduplication** — commit SHAs persisted locally so restarts don't re-trigger alerts
- **Exponential backoff** — handles GitHub rate limits and transient failures without crashing
- **Pipeline separation** — fetch, persist, and notify are independently isolated layers