import os
import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder
import requests
from bs4 import BeautifulSoup

# Лог, щоб перевірити токени
print("TELEGRAM_TOKEN in env:", os.environ.get('TELEGRAM_TOKEN'))
print("CHAT_ID in env:", os.environ.get('CHAT_ID'))

# Перевірка токена і чату
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

if not TOKEN or not CHAT_ID:
    print("Помилка: TELEGRAM_TOKEN або CHAT_ID не встановлені у змінних середовища!")
    exit(1)

CHAT_ID = int(CHAT_ID)
bot = Bot(TOKEN)

# Налаштування
BRAND = "Uniqlo"
URL = "https://shafa.ua/brand/uniqlo"
sent_items = set()

async def check_new_items():
    global sent_items
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        # Знайти товари на сторінці — заміни на реальний клас сайту
        items = soup.select(".css-1g2y0t5")  
        for item in items:
            name = item.get_text().strip()
            link_tag = item.find("a")
            link = "https://shafa.ua" + link_tag["href"] if link_tag else ""
            if name not in sent_items and BRAND.lower() in name.lower():
                sent_items.add(name)
                await bot.send_message(CHAT_ID, f"Знайдено новий товар {BRAND}: {name}\n{link}")
                print(f"Надіслано: {name} — {link}")
    except Exception as e:
        print("Помилка при перевірці товарів:", e)

async def main():
    print("Бот запущено...")
    # Перша перевірка відразу
    await check_new_items()
    # Повторювати кожні 2 хвилини
    while True:
        await asyncio.sleep(120)
        await check_new_items()

if __name__ == "__main__":
    asyncio.run(main())
