import telebot
from flask import Flask, request
from openai import OpenAI

API_TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
WEBHOOK_URL = "https://web-production-47f8f.up.railway.app"

client = OpenAI(api_key="YOUR_OPENAI_KEY")

bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")
app = Flask(__name__)

# -------------------------------
# Start Command
# -------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        f"👋 ሰላም {message.from_user.first_name}!\nAI Bot ተዘጋጅቶ ተጀምሯል 🚀"
    )

# -------------------------------
# AI Reply
# -------------------------------
@bot.message_handler(func=lambda msg: True)
def ai_chat(message):
    user_text = message.text

    try:
        answer = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_text}]
        )

        if not answer or not answer.choices:
            bot.send_message(message.chat.id, "⚠️ AI መልስ አልመጣም!")
            return

        reply = answer.choices[0].message["content"]
        bot.send_message(message.chat.id, reply)

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error: {e}")

# -------------------------------
# Webhook
# -------------------------------
@app.route("/", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Bot is running!", 200

# -------------------------------
# Run Flask
# -------------------------------
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=10000)
