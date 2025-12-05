import telebot
from flask import Flask, request
import os
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=API_KEY)

app = Flask(__name__)

# Telegram Webhook endpoint
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_update = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_update)
    bot.process_new_updates([update])
    return "OK", 200


# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 Bot is online and working!")

# Normal text messages → OpenAI
@bot.message_handler(func=lambda m: True)
def chat(message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message.text}]
    )
    bot.reply_to(message, response.choices[0].message.content)


# Flask home
@app.route('/')
def home():
    return "Bot is running!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
