import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import ApplicationBuilder

# ---- ВСТАВ СВІЙ ТОКЕН І CHAT_ID ----
TOKEN = "8206782935:AAEk10Lu_RbcyHrPgNA5OWuUJbL7jgcgjvE"
CHAT_ID = 313800446
# -------------------------------------

# Сайт, де перевіряємо товари (приклад)
URL = "https://shafa.ua/uk/uniqlo"

# Зберігаємо вже відправлені посилання
sent_links = set()

async def check_new_items(app):
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Приклад: знаходимо всі посилання на товари
        for a in soup.find_all("a", class_="item-card"):
            link = "https://shafa.ua" + a.get("href")
            title = a.get_text(strip=True)
            
            if link not in sent_links:
                sent_links.add(link)
                message = f"Знайдено новий товар Uniqlo:\n{title}\n{link}"
                await app.bot.send_message(chat_id=CHAT_ID, text=message)
                print(message)
    except Exception as e:
        print("Помилка при перевірці:", e)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Перша перевірка одразу
    await check_new_items(app)
    
    # JobQueue: повторюємо кожні 2 хвилини
    app.job_queue.run_repeating(lambda _: asyncio.create_task(check_new_items(app)), interval=120, first=120)
    
    print("Бот запущено...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
    
