import telebot
from flask import Flask, request

API_TOKEN = "8332730337:AAGSmpyXThEvg11M72biboMo98WWh_1kpYY"
WEBHOOK_URL = "https://worker-production-cf41a.up.railway.app/"  # MUST end with /

bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")
app = Flask(__name__)


# -------------------------------
# /start command
# -------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        f"👋 ሰላም {message.from_user.first_name}!\n🤖 Bot ትክክል ተጀምሯል ✔️"
    )


# -------------------------------
# Normal message reply
# -------------------------------
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, f"📩 ተቀብያለሁ: {message.text}")


# -------------------------------
# Webhook URL
# -------------------------------
@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


@app.route("/")
def home():
    return "Bot is running!", 200


# -------------------------------
# Start Flask + set webhook
# -------------------------------
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=8080)
