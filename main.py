# main.py
import requests
from bs4 import BeautifulSoup
from telegram.ext import ApplicationBuilder
import asyncio

# ----- Твій Telegram токен і chat_id -----
TOKEN = "8206782935:AAEk10Lu_RbcyHrPgNA5OWuUJbL7jgcgjvE"
CHAT_ID = 313800446

# ----- Зберігаємо вже знайдені товари -----
sent_items = set()

# ----- Функція перевірки нових товарів -----
async def check_new_items(app):
    try:
        print("Перевіряємо товари...")
        response = requests.get("https://shafa.ua/ua/shop")  # сайт для перевірки
        soup = BeautifulSoup(response.text, "html.parser")

        # Приклад: шукаємо назви товарів (змінити під реальний селектор)
        items = soup.find_all("a", class_="item-link")

        for item in items:
            name = item.text.strip()
            link = item['href']

            # Перевірка брендів Uniqlo, Cos, Arket
            if any(brand in name for brand in ["Uniqlo", "Cos", "Arket"]):
                # Перевіряємо, чи товар вже надсилали
                if link not in sent_items:
                    await app.bot.send_message(chat_id=CHAT_ID, text=f"Знайдено новий товар:\n{name}\n{link}")
                    sent_items.add(link)
                    print(f"Надіслано: {name}")

    except Exception as e:
        print("Помилка при перевірці:", e)

# ----- Головна функція -----
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # 1️⃣ Перша перевірка одразу
    await check_new_items(app)

    # 2️⃣ Перевірка кожні 2 хвилини
    app.job_queue.run_repeating(check_new_items, interval=120, first=120)

    # Запуск бота
    await app.run_polling()

# ----- Запуск -----
asyncio.run(main())
