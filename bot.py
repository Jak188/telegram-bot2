import telebot
from flask import Flask, request

TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
DOMAIN = "https://worker-production-cf41a.up.railway.app"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot is now working! 😊")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)

@app.route('/' + TOKEN, methods=['POST'])
def receive_update():
    update = telebot.types.Update.de_json(request.data.decode('utf-8'))
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/', methods=['GET'])
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{DOMAIN}/{TOKEN}")
    return "Webhook set!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
