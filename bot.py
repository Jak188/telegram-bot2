import telebot
from flask import Flask, request
import os

TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
DOMAIN = "https://web-production-47f8f.up.railway.app"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/', methods=['GET'])
def index():
    bot.remove_webhook()
    bot.set_webhook(url=f"{DOMAIN}/{TOKEN}")
    return "Webhook set!", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot is working! 😎")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
