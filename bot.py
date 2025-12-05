import telebot
from flask import Flask, request

# 🤖 የእርስዎ የቦት እና የዶሜይን መረጃ (TOKEN and DOMAIN Information)
TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
# 🔴 አዲሱ DOMAIN
DOMAIN = "https://web-production-47f8f.up.railway.app" 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- 1. /start command handler ---
@bot.message_handler(commands=['start'])
def start(message):
    """የ'/start' ትዕዛዝ ሲላክ የሚሰራ ተግባር"""
    bot.send_message(message.chat.id, "Bot is now working! Welcome! 😊")

# --- 2. /help command handler ---
@bot.message_handler(commands=['help'])
def help_command(message):
    """የ'/help' ትዕዛዝ ሲላክ የሚሰራ ተግባር"""
    help_text = (
        "🤖 እኔ Hanita Bot ነኝ! እነዚህን ትዕዛዞች መጠቀም ትችላለህ:\n\n"
        "*/start*: ቦቱን ለማስጀመር እና ለመቀበያ መልዕክት ለማግኘት።\n"
        "*/help*: ይህንን የመረጃ ዝርዝር ለማየት።\n\n"
        "👉 እንዲሁም ለሚከተሉት ቃላት ምላሽ እሰጣለሁ:\n"
        "• 'Hi', 'Selam', 'Salam'\n"
        "• 'Endet nesh', 'How are you'\n"
        "• 'Thank you', 'Thanks'"
    )
    bot.send_message(message.chat.id, help_text)

# --- 3. Enhanced Message Handler (Echo and Keywords) ---
@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    """
    ማንኛውም መልእክት ሲመጣ የሚሰራ ተግባር።
    """
    
    text = message.text.lower()
    chat_id = message.chat.id
    response = None

    # የቃላት ምላሽ ሰንጠረዥ (Keyword Response Table)
    if "hi" in text or "selam" in text or "salam" in text:
        response = "ሰላም! እንዴት ልረዳህ እችላለሁ? `/help` ብለህ በመላክ የሚገኙ ትዕዛዞችን ማየት ትችላለህ።"
    
    elif "thank you" in text or "thanks" in text or "amesegnalehu" in text:
        response = "በደስታ! ሌላ ጥያቄ ካለህ ጠይቀኝ።"
        
    elif "how are you" in text or "endet nesh" in text:
        response = "እኔ አሁን በጥሩ ሁኔታ ላይ ነኝ። አንተስ/አንቺስ? 😊"

    # ከላይ ከተጠቀሱት ቃላት ውጪ ከሆነ
    if response is None:
        if len(message.text) > 0 and len(message.text) < 15: 
            response = message.text
        else:
            response = "መልዕክትህ ደርሶኛል! ይቅርታ፣ እስካሁን ይህንን አልረዳም። `/help` የሚለውን ተጠቀም።"

    bot.send_message(chat_id, response)


# --- 4. Webhook Receiver for Telegram Updates ---
@app.route('/' + TOKEN, methods=['POST'])
def receive_update():
    """ቴሌግራም አዲስ ዝመናዎችን ሲልክ የሚቀበል ዩአርኤል"""
    update = telebot.types.Update.de_json(request.data.decode('utf-8'))
    bot.process_new_updates([update])
    return "OK", 200

# --- 5. Webhook Setter for Initial Setup ---
@app.route('/', methods=['GET'])
def set_webhook():
    """
    Webhookን ለማዘጋጀት የሚጠቅም ዩአርኤል (በአሳሽዎ አንድ ጊዜ መክፈት ያስፈልግዎታል)
    """
    bot.remove_webhook()
    bot.set_webhook(url=f"{DOMAIN}/{TOKEN}")
    return "Webhook set!", 200

# 🔴 Application Runner (app.run) ተወግዷል ምክንያቱም Gunicorn በ Procfile በኩል ይጠቀማል
