import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = os.environ.get("GROUP_ID")

app = FastAPI()

API_URL = f"https://api.telegram.org/bot{TOKEN}"

# -------------------------
# Send Message Function
# -------------------------
def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)


# -------------------------
# Root
# -------------------------
@app.get("/")
def home():
    return {"status": "Bot is running..."}


# -------------------------
# Telegram Webhook Handler
# -------------------------
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    # Ignore empty updates (avoid NoneType errors)
    if not data:
        return JSONResponse({"ok": True})

    message = data.get("message")
    if not message:
        return JSONResponse({"ok": True})

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    # -------------------------
    # Bot Commands Logic
    # -------------------------

    if text == "/start":
        send_message(chat_id,
                     f"👋 Hello! Bot is working successfully on Railway.")
        return {"ok": True}

    # Example custom reply
    if "hi" in text.lower():
        send_message(chat_id, "Hello! 😊")
        return {"ok": True}

    # Default echo
    send_message(chat_id, f"You said: {text}")

    return {"ok": True}
