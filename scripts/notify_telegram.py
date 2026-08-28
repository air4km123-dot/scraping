"""
Reusable Telegram notifier for anything that scrapes outside the main
GitHub Actions matrix (which has its own aggregated summary — see the
"notify" job in .github/workflows/scrape.yml). Used by the office PC's
Task Scheduler task for `dynamicair`, and meant to be reused the same
way for any future Part 2 (P2W InterPlus) module that also runs
locally instead of on GitHub Actions.

Reads TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID from the environment (.env
locally — same two values as the GitHub Actions secrets of the same
name).

Usage:
    python scripts/notify_telegram.py <module_name> <success|failure>
"""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()


def send(text: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set in .env — skipping notification.")
        return

    resp = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": text},
        timeout=15,
    )
    if not resp.ok or not resp.json().get("ok"):
        print(f"Telegram notification failed: {resp.text}")


def build_message(module_name: str, ok: bool) -> str:
    icon = "✅" if ok else "❌"
    status = "succeeded" if ok else "FAILED"
    return f"{icon} {module_name} ({status}) — run from office PC Task Scheduler"


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in ("success", "failure"):
        print("Usage: python scripts/notify_telegram.py <module_name> <success|failure>")
        sys.exit(1)

    module_name, outcome = sys.argv[1], sys.argv[2]
    send(build_message(module_name, outcome == "success"))
