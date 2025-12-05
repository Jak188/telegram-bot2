import os
import telebot
from flask import Flask, request
from openai import OpenAI

# -----------------------------
# TOKENS (Replace these)
# -----------------------------
API_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"      # 🔥 Change this
WEBHOOK_URL = "https://your-domain.up.railway.app"   # 🔥 Replace with Railway domain

# -----------------------------
# OpenAI Client (Environment)
# -----------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")
app = Flask(__name__)

# -----------------------------
# Start command
# -----------------------------
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(
        message,
        f"👋 ሰላም {message.from_user.first_name}!\nAI Bot ተጀምሯል 🚀"
    )

# -----------------------------
# Main Chat Handler
# -----------------------------
@bot.message_handler(func=lambda msg: True)
def chat_with_ai(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )

        # ✅ Correct Response Extract
        reply = response.choices[0].message.content

        bot.send_message(message.chat.id, reply)

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠ Error: {e}")

# -----------------------------
# Webhook Receiver
# -----------------------------
@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/')
def home():
    return "Bot Running OK ✔", 200

# -----------------------------
# Run Webhook
# -----------------------------
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=10000)
