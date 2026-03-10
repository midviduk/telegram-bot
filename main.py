import os
import asyncio
import logging
from telegram import Bot
from telegram.ext import ApplicationBuilder, JobQueue
import requests
from bs4 import BeautifulSoup

# Логи для дебагу
logging.basicConfig(level=logging.INFO)

# Твій токен і чат
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID", 0))

if not TOKEN or not CHAT_ID:
    logging.error("TELEGRAM_TOKEN або CHAT_ID не заданий в env!")
    exit(1)

bot = Bot(TOKEN)

# Бренд і сторінка для перевірки
BRAND = "Uniqlo"
URL = "https://shafa.ua/brand/uniqlo"

# Щоб не надсилати повторно
sent_items = set()

# Функція перевірки товарів
def fetch_items():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")
        # Замінити на правильний селектор під сайт
        items = soup.select(".css-1g2y0t5")  
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
        logging.error("Помилка при fetch_items: %s", e)
        return []

# Асинхронна функція JobQueue
async def check_new_items(context):
    new_items = await asyncio.to_thread(fetch_items)
    for name, link in new_items:
        try:
            await bot.send_message(CHAT_ID, f"Знайдено новий товар {BRAND}: {name}\n{link}")
            logging.info("Надіслано: %s — %s", name, link)
        except Exception as e:
            logging.error("Помилка при надсиланні повідомлення: %s", e)

async def main():
    # Створюємо додаток з JobQueue
    app = ApplicationBuilder().token(TOKEN).build()
    job_queue: JobQueue = app.job_queue

    # Перша перевірка одразу
    await check_new_items(None)

    # Додаємо JobQueue для повторної перевірки кожні 120 секунд
    job_queue.run_repeating(check_new_items, interval=120, first=120)

    # Запускаємо бота
    await app.start()
    logging.info("Бот запущено...")
    await app.updater.start_polling()
    await app.idle()

if __name__ == "__main__":
    asyncio.run(main())
