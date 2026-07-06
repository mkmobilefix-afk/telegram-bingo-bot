import os
import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

bot = Application.builder().token(BOT_TOKEN).build()


from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🎮 Open Ethio Bingo",
                web_app=WebAppInfo(
                    url="https://telegram-bingo-bot-f79o.onrender.com"
                ),
            )
        ]
    ]

    await update.message.reply_text(
        "💳 Entry Fee: 20 Birr\n\nTap the button below to open the Mini App.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 Pay 20 Birr using Telebirr.\n"
        "After payment open the Mini App."
    )


bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("join", join))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
@app.on_event("startup")
async def startup():
    await bot.initialize()
    await bot.start()


@app.on_event("shutdown")
async def shutdown():
    await bot.stop()
    await bot.shutdown()


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    update = Update.de_json(data, bot.bot)

    await bot.process_update(update)

    return {"ok": True}
