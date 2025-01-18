# testing

import uvicorn

import asyncio
from fastapi import FastAPI, Request
import requests
from telehook import TeleClient, Filters
from telehook.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery


BOT_TOKEN = "6599175207:AAG4Ow1nXH6LvQeQ-w8Pex6ZKJJ6BQ1WPz0"

app = FastAPI()

TeleHook = TeleClient(
    token=BOT_TOKEN,
    url='https://c395d657-c32e-4aee-8fd3-00d9782a42a2-00-13prezhyzp6r1.pike.replit.dev/webhook'
)

@app.get("/")
async def home_endpoint():
    return {"message": "Telegram Bot is running."}

@app.post("/webhook")
async def webhook_endpoint(request: Request):
    try:
        update = await request.json()
        await TeleHook.process_update(update)
        #print(update)
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

@TeleHook.on_message(Filters.command("start"))
async def start_cmd(client, message: Message):
    name = message.from_user.first_name

    try:
        await message.reply_text(
            f"*hellooo* {name}",
            parse_mode="MARKDOWN",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("hello haha", callback_data="hahatext")],
                    [InlineKeyboardButton("hello hahaha", callback_data="hahahatext")],
                    [
                        InlineKeyboardButton("hello", url="https://t.me/ishikki"),
                        InlineKeyboardButton("hello", url="https://t.me/ishikki")
                    ]
                ]
            )
        )
    except Exception as e:
        print(e)


import httpx


@TeleHook.on_callback_query()
async def handle_callback_query(client, callback_query: CallbackQuery):
    if callback_query.data == "hahahatext":
        await callback_query.answer("You pressed hahaha button!", show_alert=True)
    else:
        await callback_query.message.edit_text("Wow")
        await callback_query.answer("You pressed haha button!", show_alert=True)


@TeleHook.on_message(Filters.command("edit"))
async def edit_cmd(client, message):
    a = await message.reply_text(1)
    await asyncio.sleep(3)
    await a.edit_text()


if __name__ == "__main__":
    uvicorn.run("test:app", port=5000, reload=True)


