# GitHub → Telegram Commit Monitor Bot

A Python automation tool that monitors a GitHub repository for new commits and sends instant alerts to Telegram. Built with resilient API polling, SQLite-based state tracking, and clean modular architecture for reliable long-running execution.

## Features

- Monitors latest commits using GitHub REST API  
- Retry logic with exponential backoff  
- SQLite persistence to avoid duplicate alerts  
- Telegram bot notifications for new commits  
- Modular design (API, DB, notifier, orchestrator)  
- File + console logging  
- Secure API key handling using environment variables  

## Architecture

config.py        → environment & constants  
github_fetch.py → GitHub API client with retries  
storage.py      → SQLite persistence & deduplication  
notifier.py     → Telegram message sender  
main.py         → app orchestrator & polling loop  

Flow:  
GitHub API → Fetch → Compare with DB → Save → Notify Telegram

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/github-telegram-bridge.git
cd github-telegram-bridge
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

PowerShell:
```powershell
venv\Scripts\Activate.ps1
```

CMD:
```cmd
venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env File

Create a file named `.env` in project root:

```env
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_chat_id_here

USER_NAME = "github-username"
REPO_NAME = "repository-name"
```

Never commit `.env` — it is ignored via `.gitignore`.

### 5. Configure Repo to Monitor

Edit `config.py`:

### 6. Run the Bot

```bash
python main.py
```

You should see logs like:

Fetching latest commit...  
No new commit detected  
Sleeping for 60 seconds...

Push a new commit to the repo → Telegram alert will trigger.

## Database

SQLite file: `data/github.db`  
Stores commit SHAs to prevent duplicate alerts  
Automatically created on first run

## Error Handling

Handles:
- GitHub API rate limits
- Network failures
- Server errors (5xx)
- Invalid API responses

Bot continues running unless a fatal error occurs.

## Future Improvements

- Multi-repo monitoring  
- Configurable polling interval  
- First-run silent mode  
- Cloud deployment  
- Webhook-based version  
