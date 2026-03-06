# Telegram Schedule Bot

Simple Telegram bot to view your class schedule from `schedule.json`.

## Features

- `/today` shows today's schedule
- `/tomorrow` shows tomorrow's schedule
- `/week` shows the full week schedule
- `/day <weekday>` shows a selected day (`monday` ... `sunday`)

## Requirements

- Python 3.10+
- Telegram bot token from [@BotFather](https://t.me/BotFather)

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set bot token:

```bash
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN_HERE"
```

3. Run the bot:

```bash
python bot.py
```

## Run 24/7 with Docker

1. Copy `.env.example` to `.env` and set your token:

```bash
cp .env.example .env
```

2. Start with auto-restart policy:

```bash
docker compose up -d --build
```

3. Check logs:

```bash
docker compose logs -f
```

`docker-compose.yml` already uses `restart: unless-stopped`, so the bot comes back after server reboot.

## Deploy from GitHub to VPS (Auto Deploy)

This project includes GitHub Actions workflow:

- `.github/workflows/deploy.yml`

On every push to `master`, GitHub connects to your VPS and runs:

- `git pull origin master`
- `docker compose up -d --build`

### One-time VPS setup

```bash
sudo apt update
sudo apt install -y git docker.io docker-compose-plugin
sudo mkdir -p /opt/telegram_bot
sudo chown -R $USER:$USER /opt/telegram_bot
git clone https://github.com/nikitsya/telegram_bot /opt/telegram_bot
cd /opt/telegram_bot
cp .env.example .env
# edit .env and set TELEGRAM_BOT_TOKEN
docker compose up -d --build
```

### GitHub repository secrets

In `Settings -> Secrets and variables -> Actions`, add:

- `VPS_HOST` (example: `203.0.113.10`)
- `VPS_USER` (example: `root` or deploy user)
- `VPS_SSH_KEY` (private SSH key content)
- `VPS_PORT` (usually `22`)

## Configure Schedule

Edit `schedule.json` and update `days` entries.

Each lesson item supports:

- `time`
- `subject`
- `location`
- `teacher` (optional)

Example:

```json
{
  "time": "09:00",
  "subject": "Mathematics",
  "location": "Room 101"
}
```
