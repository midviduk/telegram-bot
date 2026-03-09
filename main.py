import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "ТУТ_ВАШ_ТОКЕН_З_ЛАПКАМИ"  # встав свій токен сюди

CHAT_ID = "ТУТ_ID_ЧАТУ"  # твій Telegram chat_id або для приватного чату

URLS = {
    "Uniqlo": "https://shafa.ua/brand/uniqlo",
    "Cos": "https://shafa.ua/brand/cos",
    "Arket": "https://shafa.ua/brand/arket"
}

async def check_new_items(context: ContextTypes.DEFAULT_TYPE):
    messages = []
    for brand, url in URLS.items():
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            # шукаємо перші 5 товарів
            items = soup.select("a.css-1efcn9i")[:5]
            for item in items:
                name = item.get_text(strip=True)
                link = "https://shafa.ua" + item.get("href")
                messages.append(f"{brand}: {name}\n{link}")
        except Exception as e:
            messages.append(f"{brand}: помилка при отриманні даних ({e})")
    
    if messages:
        for msg in messages:
            await context.bot.send_message(chat_id=CHAT_ID, text=msg)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущений і перевірятиме новинки кожні 2 хвилини!")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # викликаємо функцію кожні 2 хвилини
    async def scheduler():
        while True:
            await check_new_items(app)
            await asyncio.sleep(120)  # 120 секунд = 2 хвилини

    asyncio.create_task(scheduler())

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
