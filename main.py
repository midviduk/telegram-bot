import os
import asyncio
from telegram import Bot
from telegram.ext import Application, ApplicationBuilder
import requests
from bs4 import BeautifulSoup

# Telegram
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = int(os.environ['CHAT_ID'])
bot = Bot(TOKEN)

# Бренд для перевірки
BRAND = "H&M"
URL = "https://shafa.ua/brand/h-m"  # приклад сторінки бренду

# Щоб не надсилати повторно
sent_items = set()

async def check_new_items():
    global sent_items
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        # Знайти всі товари на сторінці (підправити селектор під реальний сайт)
        items = soup.select(".css-1g2y0t5")  # заміни на правильний клас для товарів
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

    # Вступне повідомлення, що бот працює
    await bot.send_message(CHAT_ID, f"Бот запущено і готовий шукати {BRAND} 🛍️")
    print(f"Вступне повідомлення надіслано: Бот запущено і готовий шукати {BRAND}")

    # Повторювати перевірку кожні 2 хвилини
    while True:
        await asyncio.sleep(120)
        await check_new_items()

if __name__ == "__main__":
    asyncio.run(main())
