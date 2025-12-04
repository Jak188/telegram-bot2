import os
from flask import Flask, request
import telebot

TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/')
def home():
    return "Telegram bot is running!", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is active!")

# ------------ IMPORTANT --------------
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8080))
    bot.remove_webhook()
    bot.set_webhook(url="https://worker-production-cf41a.up.railway.app/" + TOKEN)
    app.run(host="0.0.0.0", port=PORT)
