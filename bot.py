import telebot
from flask import Flask, request
import os # 'os' አሁን አያስፈልግም, ግን መተው ይችላሉ

TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
DOMAIN = "https://web-production-47f8f.up.railway.app"

# 'threaded=False' ለ Webhook በትክክል ስለሚያስፈልግ በጣም ጥሩ ነው!
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- 1. Webhook Receiver for Telegram Updates ---
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    """ቴሌግራም አዲስ ዝመናዎችን ሲልክ የሚቀበል ዩአርኤል"""
    json_str = request.data.decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# --- 2. Webhook Setter for Initial Setup ---
@app.route('/', methods=['GET'])
def index():
    """
    Webhookን ለማዘጋጀት የሚጠቅም ዩአርኤል
    """
    bot.remove_webhook()
    # Railway የ DOMAIN ተለዋዋጮችን በራስ ሰር ያስቀምጣል።
    bot.set_webhook(url=f"{DOMAIN}/{TOKEN}")
    return "Webhook is set!", 200

# --- 3. Command Handlers ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot is working! Welcome! 😎")

# --- 4. Message Handler (Echo) ---
@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)

# 🔴🔴🔴 Development Server (app.run) ሙሉ በሙሉ ተወግዷል! 🔴🔴🔴
