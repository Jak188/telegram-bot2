import telebot
from telebot import types
from openai import OpenAI
from flask import Flask, request

BOT_TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
API_KEY = "-proj-vfRQkQ0LTyoHx2NGM5DsuTHvZcjOg-tKbc4CPK3uYHjx2z1kQFrRh1DpgzvV8whH3Q7zfqR02GT3BlbkFJ3AanY2Bbui8wE5MdIEOAZjJ2bm4Y4PiAfUmDOEXXC9w85ircJ09j30FMFpFwiSJOsichwuqy4A"

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=API_KEY)

# save user names
registered_users = {}

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Bot is working! Welcome! 😎\n\nPlease /register first to use AI."
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

    bot.send_message(user_id, "Registered — thank you! 🙌")

# AI reply
@bot.message_handler(func=lambda msg: True)
def ai_chat(message):

    user_id = message.chat.id

    if user_id not in registered_users:
        bot.send_message(user_id, "Please /register first.")
        return

    # generate AI response
    answer = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": message.text}
        ]
    )

    bot.send_message(user_id, answer.choices[0].message["content"])


# ---------- Webhook Server ----------
app = Flask(__name__)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/')
def index():
    return "Bot is running!", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
