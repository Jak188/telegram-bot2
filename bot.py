import telebot
from telebot import types
from openai import OpenAI

BOT_TOKEN = "YOUR_BOT_TOKEN"
API_KEY = "YOUR_OPENAI_API_KEY"

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=API_KEY)

# የተመዘገቡ ዝርዝር
registered_users = {}

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Bot is working! Welcome! 😎\n\nPlease /register first to use AI."
    )

# /register command
@bot.message_handler(commands=['register'])
def register(message):
    msg = bot.reply_to(message, "Send your full name:")
    bot.register_next_step_handler(msg, save_name)

def save_name(message):
    full_name = message.text
    user_id = message.chat.id

    registered_users[user_id] = full_name

    bot.send_message(user_id, f"Registered — thank you, {full_name}!")

# ግብዣ መሞላት ምንጭ AI መልስ
@bot.message_handler(func=lambda message: True)
def ai_chat(message):
    user_id = message.chat.id

    # ካልተመዘገቡ አትፍቀድም
    if user_id not in registered_users:
        bot.send_message(user_id, "🛑 Please /register first to use AI.")
        return

    user_text = message.text

    # GPT መልስ
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful Telegram AI assistant."},
            {"role": "user", "content": user_text}
        ]
    )

    ai_reply = response.choices[0].message.content

    # Bot መልስ
    bot.send_message(user_id, ai_reply)

# polling start
bot.infinity_polling()
