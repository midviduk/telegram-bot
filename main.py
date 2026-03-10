import os
import asyncio
from telegram import Bot
from telegram.ext import Application, ApplicationBuilder
import requests
from bs4 import BeautifulSoup

# Перевіряємо змінні середовища
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

if not TOKEN or not CHAT_ID:
    print("⚠️ TELEGRAM_TOKEN або CHAT_ID не знайдено в змінних середовища!")
    print("Будь ласка, додай ці змінні через Railway Settings → Variables")
    print(f"TELEGRAM_TOKEN: {TOKEN}")
    print(f"CHAT_ID: {CHAT_ID}")
    # Додаємо заглушку, щоб код не падав
    CHAT_ID = 0
    TOKEN = "DUMMY_TOKEN"

else:
    CHAT_ID = int(CHAT_ID)
    print("✅ TELEGRAM_TOKEN та CHAT_ID знайдено, бот готовий до роботи")

bot = Bot(TOKEN)

# Товар для перевірки
BRAND = "Uniqlo"
URL = "https://shafa.ua/brand/uniqlo"  # приклад сторінки бренду

# Щоб не надсилати повторно
sent_items = set()

async def check_new_items():
    global sent_items
    if TOKEN == "DUMMY_TOKEN":
        print("🔹 Пропускаємо перевірку, бо немає токена")
        return

    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        # Знайти всі товари на сторінці (підставити правильний селектор)
        items = soup.select(".css-1g2y0t5")  # заміни на правильний клас
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
    print("🚀 Бот запущено...")
    app = ApplicationBuilder().token(TOKEN).build()

    # Перша перевірка одразу
    await check_new_items()

    # Повторювати кожні 2 хвилини
    while True:
        await asyncio.sleep(120)
        await check_new_items()

if __name__ == "__main__":
    asyncio.run(main())
