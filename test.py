# testing

import uvicorn

from fastapi import FastAPI, Request
import requests
from telehook import TeleClient, Filters


BOT_TOKEN = "6599175207:AAG4Ow1nXH6LvQeQ-w8Pex6ZKJJ6BQ1WPz0"

app = FastAPI()

TeleHook = TeleClient(
    token=BOT_TOKEN,
    url='https://pup-solid-publicly.ngrok-free.app/webhook'
)

@app.get("/")
async def home_endpoint():
    return {"message": "Telegram Bot is running."}

@app.post("/webhook")
async def webhook_endpoint(request: Request):
    try:
        update = await request.json()
        await TeleHook.process_update(update)
    except Exception as e:
        print(e)
        return {"error": str(e)}
    return {"status": "ok"}

@app.get("/run")
async def run_endpoint():
    try:
        result = TeleHook.setup_webhook()
        return {"webhook_setup_result": result}
    except Exception as e:
        return {"error": str(e)}

# ====================================================================

@TeleHook.on_message(Filters.text())
async def start_cmd(client, message):
    name = message.from_user.first_name
    try:
        await message.reply_text(f"hellooo {name}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    uvicorn.run("test:app", port=5000, reload=True)


