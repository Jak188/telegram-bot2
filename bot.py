import telebot
from fastapi import FastAPI, Request
import os

API_TOKEN = os.getenv("BOT_TOKEN")  # Railway env ውስጥ BOT_TOKEN ይጨምሩ

bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")
app = FastAPI()

# -----------------------------------
# Start command
# -----------------------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        f"👋 ሰላም {message.from_user.first_name}!\n🤖 Bot ትክክል ተጀምሯል!"
    )

# -----------------------------------
# All messages
# -----------------------------------
@bot.message_handler(func=lambda message: True)
def reply_all(message):
    bot.reply_to(message, f"🤖 ተቀብያለሁ: {message.text}")

# -----------------------------------
# Webhook route for Telegram
# -----------------------------------
@app.post("/")
async def webhook(request: Request):
    json_data = await request.json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return {"ok": True}

# -----------------------------------
# Home route (optional)
# -----------------------------------
@app.get("/")
async def home():
    return {"status": "Bot is running!"}
