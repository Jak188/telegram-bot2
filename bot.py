import os
import telebot
from openai import OpenAI
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=API_KEY)

# Store registered users
registered_users = {}

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Welcome!\n\nPlease register first using /register"
    )

# /register
@bot.message_handler(commands=['register'])
def register(message):
    msg = bot.reply_to(message, "Send your full name:")
    bot.register_next_step_handler(msg, save_name)

def save_name(message):
    full_name = message.text
    user_id = message.chat.id
    registered_users[user_id] = full_name
    bot.send_message(user_id, "✅ Registered successfully!")

# AI chat
@bot.message_handler(func=lambda msg: True)
def ai_chat(message):

    user_id = message.chat.id

    if user_id not in registered_users:
        bot.send_message(user_id, "❗ Please /register first.")
        return

    # Send to OpenAI
    ai = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": message.text}
        ]
    )

    reply = ai.choices[0].message["content"]
    bot.send_message(user_id, reply)

# ------------------ Flask Webhook Server ------------------
app = Flask(__name__)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/')
def home():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # AI reply
@bot.message_handler(func=lambda msg: True)
def ai_chat(message):

    user_id = message.chat.id

    if user_id not in registered_users:
        bot.send_message(user_id, "Please /register first!")
        return

    # generate AI response safely
    answer = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message.text}]
    )

    # handle NoneType safely
    reply = answer.choices[0].message["content"] if answer and answer.choices else "⚠️ OpenAI መልስ አልመጣም!"

    # send back to user
    bot.send_message(user_id, reply)
