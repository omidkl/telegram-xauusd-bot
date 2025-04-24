
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

OWNER_ID = 1715420309
BOT_TOKEN = "7674252396:AAGjYvGRB77VeMdGVwaoABK984LwckQ0i2k"
API_KEY = "goldapi-dch0sm9v4a2tk-io"
GOLD_API_URL = "https://www.goldapi.io/api/XAU/USD"

headers = {
    "x-access-token": API_KEY,
    "Content-Type": "application/json"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Unauthorized access.")
        return
    await update.message.reply_text("Send /m1, /m5, /m15, /m30 or /h1 to get real-time signal.")

async def get_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Unauthorized access.")
        return

    tf = update.message.text.replace("/", "").upper()
    try:
        response = requests.get(GOLD_API_URL, headers=headers)
        data = response.json()
        price = data.get("price")

        signal = f"XAU/USD Signal [{tf}]:\nEntry: {price}\nSL: {round(price - 7, 2)}\nTP: {round(price + 10, 2)}"
        await update.message.reply_text(signal)
    except Exception as e:
        await update.message.reply_text(f"Error fetching data: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["m1", "m5", "m15", "m30", "h1"], get_signal))

    app.run_polling()
