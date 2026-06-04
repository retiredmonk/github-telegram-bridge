# GitHub → Telegram Commit Monitor

A lightweight Python service that polls a GitHub repository for new commits and delivers instant Telegram notifications — with deduplication, retry logic, and structured logging built in.

---

## How It Works

```
GitHub REST API → Fetch latest commit → Compare against SQLite state → Notify via Telegram
```

Runs as a long-lived polling loop. On each cycle, it fetches the latest commit SHA, checks it against a local SQLite store, and fires a Telegram alert only if the commit is new.

---

## Architecture

```
github-telegram-bridge/
├── clients/
│   ├── github_fetch.py       # GitHub REST API client with exponential backoff
│   └── telegram_notifier.py  # Telegram Bot API message dispatcher
├── database/
│   └── db.py                 # SQLite persistence & SHA deduplication
├── services/
│   └── ...                   # Orchestration logic
├── utils/
│   ├── build_message.py      # Notification message formatter
│   ├── errors.py             # Custom exception types
│   └── logger.py             # Structured file + console logging
├── env.py                    # Pydantic settings (loaded from .env)
└── main.py                   # Entry point
```

---

## Setup

**1. Clone and create a virtual environment**

```bash
git clone https://github.com/retiredmonk/github-telegram-bridge.git
cd github-telegram-bridge
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate.bat       # Windows CMD
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment**

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_pat
TELEGRAM_TOKEN=your_bot_token
CHAT_ID=your_chat_id
OWNER_NAME=github-username
REPO_NAME=repository-name
```

**4. Run**

```bash
python main.py
```

The bot will begin polling. Push a commit to the configured repo — a Telegram alert fires within the polling interval.

---

## Key Design Decisions

- **Pydantic `BaseSettings`** for config — typed, validated, loaded from `.env` with no manual parsing.
- **SQLite deduplication** — commit SHAs are persisted locally so restarts don't re-trigger old alerts.
- **Exponential backoff** on GitHub API calls — handles rate limits and transient failures without crashing.
- **Modular layer separation** — API clients, DB, services, and utils are independently testable.

---

## Potential Extensions

- Multi-repo monitoring
- Webhook-based trigger (replace polling)
- Configurable polling interval via env
- Cloud deployment (Railway / Render)