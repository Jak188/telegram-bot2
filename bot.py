import telebot
import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ---------- OpenAI ----------
def ask_openai(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post(url, json=data, headers=headers)
    return res.json()["choices"][0]["message"]["content"]

# ---------- Gemini ----------
def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    data = {"contents":[{"parts":[{"text": prompt}]}]}
    res = requests.post(url, json=data)
    return res.json()["candidates"][0]["content"]["parts"][0]["text"]

# ---------- HuggingFace (FIXED) ----------
def ask_hf(prompt):
    url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    data = {"inputs": prompt}

    res = requests.post(url, headers=headers, json=data)

    try:
        return res.json()[0]["generated_text"]
    except:
        return "HF error (model busy or invalid key)"

# ---------- Bot Modes ----------
current_mode = {}

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg,
"""
🤖 3 AI available:

🔹 /openai  
🔹 /gemini  
🔹 /hf  

Type anything to chat!
"""
)

@bot.message_handler(commands=['openai'])
def set_openai(msg):
    current_mode[msg.chat.id] = "openai"
    bot.reply_to(msg, "✔ OpenAI activated!")

@bot.message_handler(commands=['gemini'])
def set_gemini(msg):
    current_mode[msg.chat.id] = "gemini"
    bot.reply_to(msg, "✔ Gemini activated!")

@bot.message_handler(commands=['hf'])
def set_hf(msg):
    current_mode[msg.chat.id] = "hf"
    bot.reply_to(msg, "✔ HuggingFace activated!")

@bot.message_handler(func=lambda m: True)
def ai_chat(msg):
    mode = current_mode.get(msg.chat.id, "openai")

    if mode == "openai":
        reply = ask_openai(msg.text)
    elif mode == "gemini":
        reply = ask_gemini(msg.text)
    else:
        reply = ask_hf(msg.text)

    bot.reply_to(msg, reply)

bot.polling()
