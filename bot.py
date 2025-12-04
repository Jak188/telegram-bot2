import telebot
from flask import Flask, request

# 🤖 የእርስዎ የቦት እና የዶሜይን መረጃ (TOKEN and DOMAIN Information)
# እነዚህን እንደ ቀድሞው ይጠቀሙ
TOKEN = "8332730337:AAEqwWC-PsmwwOP2KvdWkZhY1Bqvo59b1aU"
DOMAIN = "https://worker-production-cf41a.up.railway.app" # ይህ የእርስዎ Railway ዶሜይን ነው

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- 1. /start command handler ---
@bot.message_handler(commands=['start'])
def start(message):
    """የ'/start' ትዕዛዝ ሲላክ የሚሰራ ተግባር"""
    bot.send_message(message.chat.id, "Bot is now working! Welcome! 😊")

# --- 2. Enhanced Message Handler (Echo and Keywords) ---
@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    """
    ማንኛውም መልእክት ሲመጣ የሚሰራ ተግባር።
    - ለተወሰኑ ቃላት ምላሽ ይሰጣል
    - ለሌሎች መልዕክቶች Echo ያደርጋል
    """
    
    # መልእክቱን ወደ ትናንሽ ፊደላት (lowercase) ይቀይሩት ለትክክለኛ ንጽጽር
    text = message.text.lower()
    chat_id = message.chat.id
    response = None # የመልስ መጀመሪያ

    # የቃላት ምላሽ ሰንጠረዥ (Keyword Response Table)
    if "hi" in text or "selam" in text or "salam" in text:
        response = "ሰላም! እንዴት ልረዳህ እችላለሁ? `/start` የሚለውን በመጠቀም መጀመር ይችላሉ።"
    
    elif "thank you" in text or "thanks" in text or "amesegnalehu" in text:
        response = "በደስታ! ሌላ ጥያቄ ካለህ ጠይቀኝ።"
        
    elif "how are you" in text or "endet nesh" in text:
        response = "እኔ አሁን በጥሩ ሁኔታ ላይ ነኝ። አንተስ/አንቺስ? 😊"

    # ከላይ ከተጠቀሱት ቃላት ውጪ ከሆነ
    if response is None:
        # መልዕክቱ በጣም አጭር ከሆነ መልሰው ይላኩት (Echo)
        if len(message.text) > 0 and len(message.text) < 15: 
            response = message.text
        else:
            # ረጅም ወይም ውስብስብ መልእክት ከሆነ
            response = "መልዕክትህ ደርሶኛል! ይቅርታ፣ እስካሁን ይህንን አልረዳም።"

    bot.send_message(chat_id, response)


# --- 3. Webhook Receiver for Telegram Updates ---
@app.route('/' + TOKEN, methods=['POST'])
def receive_update():
    """ቴሌግራም አዲስ ዝመናዎችን ሲልክ የሚቀበል ዩአርኤል"""
    update = telebot.types.Update.de_json(request.data.decode('utf-8'))
    bot.process_new_updates([update])
    return "OK", 200

# --- 4. Webhook Setter for Initial Setup ---
@app.route('/', methods=['GET'])
def set_webhook():
    """
    Webhookን ለማዘጋጀት የሚጠቅም ዩአርኤል (በአሳሽዎ አንድ ጊዜ መክፈት ያስፈልግዎታል)
    """
    bot.remove_webhook()
    bot.set_webhook(url=f"{DOMAIN}/{TOKEN}")
    return "Webhook set!", 200

# --- 5. Application Runner ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
