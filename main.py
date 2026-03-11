import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))

bot = Bot(TOKEN)

URL = "https://shafa.ua/uk/brand/hm"

sent_links = set()


def get_items():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    items = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "/item/" in href:

            link = "https://shafa.ua" + href
            name = a.get_text(strip=True)

            if name:
                items.append((name, link))

    return items


async def check_items():

    print("🔎 Перевіряю нові товари...")

    items = await asyncio.to_thread(get_items)

    for name, link in items:

        if link not in sent_links:

            sent_links.add(link)

            print("Знайдено:", name)

            await bot.send_message(
                CHAT_ID,
                f"🛍 Новий H&M\n\n{name}\n{link}"
            )


async def main():

    print("🚀 Бот запускається")

    await bot.send_message(CHAT_ID, "✅ Бот запущено і шукає H&M")

    while True:

        try:

            await check_items()

        except Exception as e:

            print("❌ Помилка:", e)

        await asyncio.sleep(120)


if __name__ == "__main__":
    asyncio.run(main())
