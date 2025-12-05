import os
import telebot
from flask import Flask, request
from db import DB
from ai import ask_ai
from utils import send_long_message, track_user

TOKEN = os.environ.get("TOKEN")
DOMAIN = os.environ.get("DOMAIN")  # e.g. https://web-production-xxxx.up.railway.app
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)
db = DB("bot.db")   # sqlite file

# webhook receiver
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.data.decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# set webhook (visit once)
@app.route('/', methods=['GET'])
def index():
    bot.remove_webhook()
    bot.set_webhook(url=f"{DOMAIN}/{TOKEN}")
    return "Webhook is set!", 200

# /start
@bot.message_handler(commands=['start'])
def start(message):
    track_user(message.from_user.id)
    bot.send_message(message.chat.id, "Bot is working! Welcome! 😎")

# /register simple example
@bot.message_handler(commands=['register'])
def register_cmd(message):
    user_id = message.from_user.id
    if db.user_exists(user_id):
        bot.send_message(message.chat.id, "You are already registered.")
        return
    msg = bot.send_message(message.chat.id, "Send your full name:")
    bot.register_next_step_handler(msg, save_name)

def save_name(message):
    user_id = message.from_user.id
    name = message.text
    db.add_user(user_id, name)
    bot.send_message(message.chat.id, "Registered — thank you!")

# AI handler (non-command)
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    track_user(message.from_user.id)
    text = message.text
    # simple local reply path: if user registered -> AI, else ask to register
    if not db.user_exists(message.from_user.id):
        bot.send_message(message.chat.id, "Please /register first to use AI.")
        return
    # send to AI (ask_ai is stub/wrapper)
    try:
        reply = ask_ai(text, user_id=str(message.from_user.id))
    except Exception as e:
        reply = "Sorry, AI error: " + str(e)
    # ensure we don't exceed Telegram message length
    send_long_message(bot, message.chat.id, reply)

# photo handler
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    user_id = message.from_user.id
    if not db.user_exists(user_id):
        bot.send_message(message.chat.id, "Please /register first before sending photos.")
        return
    file_id = message.photo[-1].file_id
    # forward to admin
    bot.send_photo(ADMIN_ID, file_id, caption=f"Photo from {message.from_user.username or user_id}")

if __name__ == "__main__":
    # DO NOT call bot.polling() when using webhook
    # Use app.run only for local debugging. Production uses gunicorn
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
