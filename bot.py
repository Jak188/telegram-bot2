import telebot
from flask import Flask, request

TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
DOMAIN = "https://web-production-47f8f.up.railway.app" 

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- 1. Webhook Receiver ---
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.data.decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# --- 2. Webhook Setter ---
@app.route('/', methods=['GET'])
def index():
    bot.remove_webhook()
    bot.set_webhook(url=f"{DOMAIN}/{TOKEN}")
    return "Webhook is set!", 200

# --- 3. Command Handler: /start ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot is working! Welcome! 😎")

# --- 4. Message Handler: Echo ---
@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)

# 🔴🔴🔴 'if __name__ == '__main__': ... app.run(...)' የሚለው ብሎክ መጥፋቱን ያረጋግጡ! 🔴🔴🔴
