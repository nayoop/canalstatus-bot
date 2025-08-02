import os
import time
import requests
from telegram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
CANAL_STATUS_API = os.getenv("CANAL_STATUS_API", "https://canalstatus.com/api/v1/bridges")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
last_status = ""
message_id = None

def fetch_status():
    try:
        response = requests.get(CANAL_STATUS_API)
        data = response.json()
        status_lines = []
        for bridge in data:
            emoji = "🟢" if bridge["status"] == "open" else ("🔴" if bridge["status"] == "closed" else "🟡")
            status_lines.append(f"{emoji} {bridge['name']} → {bridge['status']}")
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        return "\n".join(status_lines) + f"\n\n⏱ بروزرسانی: {timestamp}"
    except Exception as e:
        return f"⚠️ خطا در دریافت اطلاعات: {e}"

print("ربات در حال اجراست...")

while True:
    status = fetch_status()
    if message_id is None:
        msg = bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=status)
        message_id = msg.message_id
    else:
        try:
            bot.edit_message_text(chat_id=TELEGRAM_CHANNEL_ID, message_id=message_id, text=status)
        except Exception as e:
            print(f"خطا در ویرایش پیام: {e}")
    time.sleep(5)  # هر ۵ ثانیه یک‌بار به‌روزرسانی
