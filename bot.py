from fastapi import FastAPI, Request
import httpx
import os

TOKEN = os.getenv("BOT_TOKEN")  # Put this in Railway variables
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
HF_KEY = os.getenv("HF_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

active_model = "openai"  # default model

# -------------------- SEND MESSAGE TO TELEGRAM --------------------
async def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={"chat_id": chat_id, "text": text})

# -------------------- OPENAI MODEL --------------------
async def run_openai(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_KEY}"}

    async with httpx.AsyncClient() as client:
        r = await client.post(url, json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }, headers=headers)

    return r.json()["choices"][0]["message"]["content"]

# -------------------- HUGGINGFACE MODEL --------------------
async def run_hf(prompt):
    url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {HF_KEY}"}

    async with httpx.AsyncClient() as client:
        r = await client.post(url, json={"inputs": prompt}, headers=headers)

    try:
        return r.json()[0]["generated_text"]
    except:
        return "HF error"

# -------------------- GEMINI MODEL --------------------
async def run_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_KEY}"

    async with httpx.AsyncClient() as client:
        r = await client.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        })

    try:
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Gemini error"

# -------------------- HANDLE SWITCH COMMANDS --------------------
async def switch_model(chat_id, text):
    global active_model

    if text == "/openai":
        active_model = "openai"
        await send_message(chat_id, "✓ OpenAI activated!")
        return True

    if text == "/hf":
        active_model = "hf"
        await send_message(chat_id, "✓ HuggingFace activated!")
        return True

    if text == "/gemini":
        active_model = "gemini"
        await send_message(chat_id, "✓ Gemini activated!")
        return True

    return False

# -------------------- MAIN WEBHOOK HANDLER --------------------
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    if "message" not in data:
        return {"ok": True}

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    # Switch model
    if await switch_model(chat_id, text):
        return {"ok": True}

    # Run model
    if active_model == "openai":
        reply = await run_openai(text)

    elif active_model == "hf":
        reply = await run_hf(text)

    elif active_model == "gemini":
        reply = await run_gemini(text)

    else:
        reply = "Model error"

    await send_message(chat_id, reply)
    return {"ok": True}

# -------------------- ROOT FOR TESTING --------------------
@app.get("/")
async def root():
    return {"status": "bot running"}
