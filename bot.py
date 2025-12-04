import os
import telebot
from flask import Flask, request
import requests

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, threaded=False)
app = Flask(__name__)

# -----------------------------
# AI Functions
# -----------------------------

def ask_openai(prompt):
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
        res = requests.post(url, json=data, headers=headers)
        return res.json()["choices"][0]["message"]["content"]
    except:
        return "❌ OpenAI error"

def ask_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        data = {"contents":[{"parts":[{"text": prompt}]}]}
        res = requests.post(url, json=data)
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "❌ Gemini error"

def ask_hf(prompt):
    try:
        url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        data = {"inputs": prompt}
        res = requests.post(url, headers=headers, json=data)
        return res.json()[0]["generated_text"]
    except:
        return "❌ HuggingFace error"


# User mode memory
current_mode = {}


# -----------------------------
# COMMANDS
# -----------------------------
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


# -----------------------------
# MAIN CHAT HANDLER
# -----------------------------
@bot.message_handler(func=lambda m: True)
def chat(msg):
    mode = current_mode.get(msg.chat.id, "openai")

    if mode == "openai":
        resp = ask_openai(msg.text)
    elif mode == "gemini":
        resp = ask_gemini(msg.text)
    else:
        resp = ask_hf(msg.text)

    bot.reply_to(msg, resp)


# -----------------------------
# WEBHOOK HANDLER
# -----------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200


# -----------------------------
# START FLASK
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
