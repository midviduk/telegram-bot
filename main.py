import asyncio
from telegram import Bot
from bs4 import BeautifulSoup
import requests

# Вставляю твій токен і chat_id прямо
TOKEN = "8206782935:AAEk10Lu_RbcyHrPgNA5OWuUJbL7jgcgjvE"
CHAT_ID = 313800446

bot = Bot(token=TOKEN)

async def check_new_items():
    urls = {
        "uniqlo": "https://shafa.ua/search?brand=uniqlo",
        "cos": "https://shafa.ua/search?brand=cos",
        "arket": "https://shafa.ua/search?brand=arket"
    }

    for brand, url in urls.items():
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find_all("a", class_="card-link")  # тут можна змінити на актуальний селектор
            if items:
                message = f"Нові товари {brand}: {items[0].text.strip()}"
                await bot.send_message(chat_id=CHAT_ID, text=message)
        except Exception as e:
            print(f"Помилка при перевірці {brand}: {e}")

async def main():
    while True:
        await check_new_items()
        await asyncio.sleep(120)  # чекати 2 хвилини

if __name__ == "__main__":
    asyncio.run(main())
