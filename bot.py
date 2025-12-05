import os
import telebot
from flask import Flask, request
from openai import OpenAI

# --- Environment Variables (Railway will load these)
API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")
app = Flask(__name__)


# ---------------- START COMMAND ----------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"👋 ሰላም {message.from_user.first_name}!\nAI Bot ተጀምሯል 🚀")


# ---------------- HANDLE USER MESSAGE ----------------
@bot.message_handler(func=lambda msg: True)
def ai_reply(message):
    try:
        answer = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message.text}]
        )

        reply = answer.choices[0].message.content
        bot.send_message(message.chat.id, reply)

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error: {e}")


# ---------------- WEBHOOK HANDLER ----------------
@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


@app.route("/")
def home():
    return "Bot Running OK!", 200


# ---------------- START FLASK SERVER ----------------
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
