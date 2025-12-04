import telebot
import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ----------------------------- AI FUNCTIONS ---------------------------------

def ask_openai(prompt):
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
        }
        r = requests.post(url, json=data, headers=headers)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"OpenAI Error: {e}"


def ask_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        data = {"contents":[{"parts":[{"text": prompt}]}]}
        r = requests.post(url, json=data)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini Error: {e}"


def ask_hf(prompt):
    try:
        url = "https://api-inference.huggingface.co/models/google/flan-t5-small"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        data = {"inputs": prompt}
        r = requests.post(url, headers=headers, json=data)
        return r.json()[0]["generated_text"]
    except Exception as e:
        return f"HF Error: {e}"

# ---------------------------------------------------------------------------

current_mode = {}  # openai / gemini / hf


@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg,
"""
🤖 **3 AI MODELS READY**

🔹 /openai — OpenAI GPT  
🔹 /gemini — Google Gemini  
🔹 /hf — HuggingFace (flan-t5)

Type anything to chat!
"""
)


@bot.message_handler(commands=['openai'])
def set_openai(msg):
    current_mode[msg.chat.id] = "openai"
    bot.reply_to(msg, "✔ OpenAI Mode Activated!")


@bot.message_handler(commands=['gemini'])
def set_gemini(msg):
    current_mode[msg.chat.id] = "gemini"
    bot.reply_to(msg, "✔ Gemini Mode Activated!")


@bot.message_handler(commands=['hf'])
def set_hf(msg):
    current_mode[msg.chat.id] = "hf"
    bot.reply_to(msg, "✔ HuggingFace Mode Activated!")


@bot.message_handler(func=lambda msg: True)
def chat(msg):
    mode = current_mode.get(msg.chat.id, "openai")

    if mode == "openai":
        reply = ask_openai(msg.text)
    elif mode == "gemini":
        reply = ask_gemini(msg.text)
    else:
        reply = ask_hf(msg.text)

    bot.reply_to(msg, reply)


# ----------------------------- RUN BOT -------------------------------------

bot.polling()
