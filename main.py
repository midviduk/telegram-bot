import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import asyncio

# ====== Налаштування бота ======
TOKEN = "8206782935:AAEk10Lu_RbcyHrPgNA5OWuUJbL7jgcgjvE"
CHAT_ID = 313800446

bot = Bot(TOKEN)

# ====== Налаштування фірм ======
TARGET_BRANDS = ["Uniqlo", "Cos", "Arket"]
URL = "https://shafa.ua/uk/odezhda"

# ====== Список вже відправлених товарів ======
sent_items = set()

# ====== Функція перевірки нових товарів ======
async def check_new_items(context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # шукаємо блоки товарів
        products = soup.find_all("div", class_="product-card__main")
        for product in products:
            title_tag = product.find("a", class_="product-card__title")
            if not title_tag:
                continue
            title = title_tag.text.strip()

            # перевірка на фірму
            if any(brand.lower() in title.lower() for brand in TARGET_BRANDS):
                link_tag = product.find("a", class_="product-card__title")
                link = "https://shafa.ua" + link_tag["href"]

                # відправка тільки нових товарів
                if link not in sent_items:
                    sent_items.add(link)
                    await bot.send_message(chat_id=CHAT_ID, text=f"{title}\n{link}")
    except Exception as e:
        print("Помилка при перевірці:", e)

# ====== Функція старту бота ======
async def start(update, context):
    await update.message.reply_text("Бот запущено! Перевірка нових товарів кожні 2 хвилини.")

# ====== Основний блок запуску ======
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Запуск перевірки кожні 2 хвилини (120 сек)
    app.job_queue.run_repeating(check_new_items, interval=120, first=5)

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()  # щоб програма працювала безкінечно

if __name__ == "__main__":
    asyncio.run(main())
    
