import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import ApplicationBuilder

# ----- Налаштування -----
TOKEN = "тут_твій_токен_бота"  # твій Telegram токен
CHAT_ID = 313800446             # твій chat_id
CHECK_INTERVAL = 120            # інтервал перевірки в секундах

# URL для Uniqlo на Shafa.ua
URL = "https://shafa.ua/ua/brand-uniqlo"

# Тут будемо зберігати посилання на вже надіслані товари
sent_items = set()

# ----- Функція перевірки -----
async def check_new_items(app):
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        # Знаходимо всі товари на сторінці
        items = soup.select("a.item-card")  # залежить від HTML Shafa, може бути "a.card-link" тощо

        for item in items:
            title = item.get_text(strip=True)
            link = "https://shafa.ua" + item.get("href")

            # Надсилаємо тільки нові товари
            if link not in sent_items:
                sent_items.add(link)
                message = f"Знайдено новий товар Uniqlo: {title}\nПосилання: {link}"
                await app.bot.send_message(chat_id=CHAT_ID, text=message)
                print(f"Відправлено: {title}")

    except Exception as e:
        print("Помилка при перевірці:", e)

# ----- Головна функція -----
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Перша перевірка відразу
    await check_new_items(app)

    # Перевірка кожні 2 хвилини
    while True:
        await asyncio.sleep(CHECK_INTERVAL)
        await check_new_items(app)

# ----- Запуск -----
if __name__ == "__main__":
    asyncio.run(main())
