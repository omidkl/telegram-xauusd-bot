import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_ID = int(os.getenv("TELEGRAM_ID"))
GOLD_API_KEY = os.getenv("GOLD_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Send /xauusd to get the live gold price.")

async def xauusd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        "x-access-token": GOLD_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        price = data.get("price")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"XAU/USD price: ${price}")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error fetching price")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("xauusd", xauusd))
    app.run_polling()
