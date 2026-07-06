import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from database import init_db, create_user
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

bot = Application.builder().token(BOT_TOKEN).build()


# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(
        user.id,
        user.username or ""
    )

    await update.message.reply_text(
        "🇪🇹 Welcome to Ethio Bingo!\n\n"
        "✅ Account created successfully.\n\n"
        "Use /join to continue."
    )


# ---------------- JOIN ----------------

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
        "💳 Entry Fee: 20 Birr\n\nTap below to open the Mini App.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("join", join))


# ---------------- WEBSITE ----------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


# ---------------- STARTUP ----------------

@app.on_event("startup")
async def startup():
    init_db()

    await bot.initialize()
    await bot.start()


@app.on_event("shutdown")
async def shutdown():
    await bot.stop()
    await bot.shutdown()


# ---------------- WEBHOOK ----------------

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    update = Update.de_json(data, bot.bot)

    await bot.process_update(update)

    return {"ok": True}
