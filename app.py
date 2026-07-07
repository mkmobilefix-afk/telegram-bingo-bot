import os

from config import *
from bingo import generate_card
from game_engine import (
    get_random_card,
    card_to_json,
)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from database import (
    init_db,
    create_user,
    get_user,
    get_current_game,
    get_player_card_count,
    add_prize_pool,
    save_card,
    deduct_balance,
    save_deposit,
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
        "💳 Entry Fee: 20 Birr\n\n"
        "Tap below to open the Mini App.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
# ---------------- BUY CARD ----------------

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    player = get_user(user.id)

    if not player:
        await update.message.reply_text(
            "❌ Please use /start first."
        )
        return

    if player["balance"] < 20:
        await update.message.reply_text(
            "❌ Insufficient balance."
        )
        return

    game = get_current_game()

    if not game:
        await update.message.reply_text(
            "❌ No active game."
        )
        return

    cards = get_player_card_count(
        user.id,
        game["id"]
    )

    if cards >= 5:
        await update.message.reply_text(
            "❌ Maximum 5 cards allowed."
        )
        return

    deduct_balance(user.id, 20)

    add_prize_pool(game["id"], 20)

    card = get_random_card()

    save_card(
        user.id,
        game["id"],
        card_to_json(card)
    )

    await update.message.reply_text(
        f"✅ Card Purchased!\n\n"
        f"Cards: {cards + 1}/5\n"
        f"20 Birr deducted from your balance."
    )


# ---------------- HANDLERS ----------------

bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("join", join))
bot.add_handler(CommandHandler("buy", buy))  
# ---------------- WEBSITE ----------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    card = generate_card()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "card": card,
        },
    )


# ---------------- STARTUP ----------------

@app.on_event("startup")
async def startup():

    init_db()

    await bot.initialize()
    await bot.start()


# ---------------- SHUTDOWN ----------------

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


# ---------------- RUN ----------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
