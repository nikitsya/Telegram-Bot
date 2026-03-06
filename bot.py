import json
import logging
import os
from datetime import date, timedelta
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

SCHEDULE_FILE = Path(__file__).with_name("schedule.json")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def load_schedule() -> dict:
    if not SCHEDULE_FILE.exists():
        raise FileNotFoundError(f"Schedule file is missing: {SCHEDULE_FILE}")
    with SCHEDULE_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if "days" not in data or not isinstance(data["days"], dict):
        raise ValueError("Invalid schedule.json format: 'days' object is required.")
    return data


def normalize_day_name(raw_day: str) -> str:
    aliases = {
        "mon": "monday",
        "tue": "tuesday",
        "wed": "wednesday",
        "thu": "thursday",
        "fri": "friday",
        "sat": "saturday",
        "sun": "sunday",
    }
    key = raw_day.strip().lower()
    return aliases.get(key, key)


def format_day(schedule: dict, day_name: str) -> str:
    days = schedule.get("days", {})
    lessons = days.get(day_name, [])
    title = day_name.capitalize()

    if not lessons:
        return f"{title}\nNo classes."

    lines = [title]
    for lesson in lessons:
        time = lesson.get("time", "--:--")
        subject = lesson.get("subject", "Untitled")
        location = lesson.get("location", "No room")
        lines.append(f"{time} - {subject} ({location})")
    return "\n".join(lines)


def day_name_for(target_date: date) -> str:
    return target_date.strftime("%A").lower()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Schedule bot is ready.\n"
        "Commands:\n"
        "/today - today schedule\n"
        "/tomorrow - tomorrow schedule\n"
        "/week - full week\n"
        "/day <weekday> - selected day (example: /day monday)\n"
        "/help - commands list"
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    schedule = load_schedule()
    name = day_name_for(date.today())
    await update.message.reply_text(format_day(schedule, name))


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    schedule = load_schedule()
    name = day_name_for(date.today() + timedelta(days=1))
    await update.message.reply_text(format_day(schedule, name))


async def week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    schedule = load_schedule()
    order = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    output = "\n\n".join(format_day(schedule, day) for day in order)
    await update.message.reply_text(output)


async def day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /day <weekday>, for example: /day monday")
        return

    requested = normalize_day_name(context.args[0])
    valid = {
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    }
    if requested not in valid:
        await update.message.reply_text("Unknown day. Use monday, tuesday, ... sunday.")
        return

    schedule = load_schedule()
    await update.message.reply_text(format_day(schedule, requested))


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN environment variable before start.")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("tomorrow", tomorrow))
    app.add_handler(CommandHandler("week", week))
    app.add_handler(CommandHandler("day", day))

    logger.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
