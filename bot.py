import telebot
from flask import Flask, request
from openai import OpenAI
import os

TOKEN = os.getenv("BOT_TOKEN")  # Railway Settings → Variables
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

app = Flask(__name__)

# የTelegram webhook መቀበያ
@app.route("/" + TOKEN, methods=["POST"])
def receive_update():
    json_update = request.get_json(force=True)
    update = telebot.types.Update.de_json(json_update)
    bot.process_new_updates([update])
    return "OK", 200

# የተጠቃሚ መልዕክት ሲመጣ
@bot.message_handler(func=lambda message: True)
def reply_user(message):
    user_text = message.text

    try:
        # OpenAI መልስ መፍጠር
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_text}]
        )

        if response and response.choices:
            reply = response.choices[0].message["content"]
        else:
            reply = "⚠️ OpenAI መልስ አልመጣም! እንደገና ይሞክሩ."

    except Exception as e:
        reply = f"⚠️ ስህተት ተፈጥሯል: {str(e)}"

    bot.send_message(message.chat.id, reply)


@app.route("/", methods=["GET"])
def home():
    return "BOT RUNNING!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
