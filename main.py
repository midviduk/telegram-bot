import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import ApplicationBuilder, ContextTypes

TOKEN = "твій_токен_сюди"  # <- твій Telegram токен
CHAT_ID = 313800446         # <- твій chat_id
URL = "https://shafa.ua/ua/brand-uniqlo"

# Список вже відправлених товарів
sent_items = set()

async def check_new_items(app):
    global sent_items
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Правильний селектор для лінків на товари
    items = soup.select("a.card-link")  

    for item in items:
        title = item.get_text(strip=True)
        link = "https://shafa.ua" + item.get("href")

        if link not in sent_items:
            sent_items.add(link)
            print(f"Надсилаємо новий товар: {title} -> {link}")
            await app.bot.send_message(chat_id=CHAT_ID, text=f"{title}\n{link}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    await app.initialize()
    
    # Перша перевірка одразу
    await check_new_items(app)
    
    # Повторювати кожні 120 секунд
    job_queue = app.job_queue
    job_queue.run_repeating(lambda _: asyncio.create_task(check_new_items(app)), interval=120, first=120)
    
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
    
