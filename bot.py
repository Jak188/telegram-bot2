import telebot
from flask import Flask, request

TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
DOMAIN = "https://worker-production-cf41a.up.railway.app"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_data = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/', methods=['GET'])
def home():
    return "Bot is running!", 200

# Handlers
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot is alive on Railway! 🚀")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)

# ▶️ DO NOT USE app.run() on Railway
# Railway will run it automatically using Gunicorn (Procfile)
