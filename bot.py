import telebot
from flask import Flask, request

API_TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
WEBHOOK_URL = "https://worker-production-cf41a.up.railway.app"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Webhook route
@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    json_str = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


# Homepage
@app.route('/')
def index():
    return "Bot is running!", 200


# /start command
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "👋 ሰላም! ቦትዬ ተጀምሯል።")

# Echo handler
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"እነሆ👇\n{message.text}")


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + "/" + API_TOKEN)
    app.run(host="0.0.0.0", port=10000)
