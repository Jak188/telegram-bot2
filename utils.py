def send_long_message(bot, chat_id, text):
    # split to 4096 char chunks
    max_len = 4000
    if len(text) <= max_len:
        bot.send_message(chat_id, text)
        return
    for i in range(0, len(text), max_len):
        bot.send_message(chat_id, text[i:i+max_len])

def track_user(uid):
    # placeholder: you can log last seen, etc.
    pass
