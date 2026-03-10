import os
import asyncio
import logging
from telegram import Bot
from telegram.ext import ApplicationBuilder
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID", 0))

if not TOKEN or not CHAT_ID:
    logging.error("TELEGRAM_TOKEN або CHAT_ID не заданий в env!")
    exit(1)

bot = Bot(TOKEN)
BRAND = "Uniqlo"
URL = "https://shafa.ua/brand/uniqlo"
sent_items = set()

def fetch_items():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".css-1g2y0t5")  # заміни на реальний селектор
        new_items = []
        for item in items:
            name = item.get_text().strip()
            link_tag = item.find("a")
            link = "https://shafa.ua" + link_tag["href"] if link_tag else ""
            if name not in sent_items and BRAND.lower() in name.lower():
                sent_items.add(name)
                new_items.append((name, link))
        return new_items
    except Exception as e:
        logging.error("Помилка fetch_items: %s", e)
        return []

async def check_new_items(context):
    new_items = await asyncio.to_thread(fetch_items)
    for name, link in new_items:
        try:
            await bot.send_message(CHAT_ID, f"Знайдено новий товар {BRAND}: {name}\n{link}")
            logging.info("Надіслано: %s — %s", name, link)
        except Exception as e:
            logging.error("Помилка надсилання: %s", e)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Перша перевірка одразу
    app.job_queue.run_once(check_new_items, when=0)

    # Повторювати кожні 2 хвилини
    app.job_queue.run_repeating(check_new_items, interval=120, first=120)

    logging.info("Бот запущено...")
    app.run_polling()  # <-- правильно запускає все і JobQueue

if __name__ == "__main__":
    main()
