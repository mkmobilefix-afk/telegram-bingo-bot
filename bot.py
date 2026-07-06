from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇪🇹 Welcome to Ethio Bingo!\n\n"
        "🎟 Entry Fee : 20 Birr\n"
        "Use /join to join the next game."
    )

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 Pay 20 Birr using Telebirr.\n"
        "After payment send your screenshot."
    )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("join", join))

app.run_polling()
