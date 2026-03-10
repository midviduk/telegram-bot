import os
import asyncio
from telegram import Bot
from telegram.ext import Application, ApplicationBuilder
import requests
from bs4 import BeautifulSoup

# Перевірка, чи токен і чат_id встановлені
print("TELEGRAM_TOKEN in env:", os.environ.get('TELEGRAM_TOKEN'))
print("CHAT_ID in env:", os.environ.get('CHAT_ID'))

# Telegram
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = int(os.environ['CHAT_ID'])
bot = Bot(TOKEN)

# Бренд та сторінка для перевірки
BRAND = "H&M"
URL = "https://shafa.ua/brand/hm"  # сторінка H&M

# Щоб не надсилати повторно
sent_items = set()

async def check_new_items():
    global sent_items
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        # Знаходимо всі товари на сторінці
        items = soup.select(".css-1g2y0t5")  # заміни на правильний клас, якщо треба
        for item in items:
            name = item.get_text().strip()
            link_tag = item.find("a")
            link = "https://shafa.ua" + link_tag["href"] if link_tag else ""
            if name not in sent_items:
                sent_items.add(name)
                if BRAND.lower() in name.lower():
                    await bot.send_message(CHAT_ID, f"Знайдено новий товар {BRAND}: {name}\n{link}")
                    print(f"Надіслано: {name} — {link}")
    except Exception as e:
        print("Помилка при перевірці товарів:", e)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Перша перевірка одразу
    await check_new_items()

    # Повторювати кожні 2 хвилини
    while True:
        await asyncio.sleep(120)
        await check_new_items()

if __name__ == "__main__":
    asyncio.run(main())
