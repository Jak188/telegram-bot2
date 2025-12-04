import telebot
from flask import Flask, request

TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
DOMAIN = "https://worker-production-cf41a.up.railway.app"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# -----------------------
# Telegram Commands
# -----------------------

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hello! Bot is working successfully!")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"እባክህ የተጻፈው: {message.text}")


# -----------------------
# Flask Webhook
# -----------------------

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route('/', methods=['GET'])
def set_webhook():
    webhook_url = f"{DOMAIN}/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    return f"Webhook set to {webhook_url}", 200


# -----------------------
# Run the server
# -----------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
