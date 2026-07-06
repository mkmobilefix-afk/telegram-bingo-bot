from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from contextlib import asynccontextmanager
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇪🇹 Welcome to Ethio Bingo!\n\n"
        "🎟 Entry Fee: 20 Birr\n"
        "Press the Mini App button to play."
    )

bot.add_handler(CommandHandler("start", start))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.initialize()
    await bot.start()
    yield
    await bot.stop()
    await bot.shutdown()


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )
