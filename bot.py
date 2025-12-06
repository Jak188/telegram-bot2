import telebot
from flask import Flask, request

API_TOKEN = "8332730337:AAGSmpyXThEvg11M72biboMo98WWh_1kpYY"
WEBHOOK_URL = "https://cf41a.up.railway.app"

bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Bot is working!")

@bot.message_handler(func=lambda msg: True)
def echo(message):
    bot.reply_to(message, "Received: " + message.text)

@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Bot is running!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
