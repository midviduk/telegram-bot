import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import ApplicationBuilder

TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = int(os.environ['CHAT_ID'])

bot = Bot(TOKEN)

BRAND = "h&m"
URL = "https://shafa.ua/uk/brand/hm"

sent_links = set()

def get_items():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    items = []

    for a in soup.select("a[href*='/uk/']"):
        href = a.get("href")

        if "/uk/" in href and "/item/" in href:
            link = "https://shafa.ua" + href
            name = a.get_text(strip=True)

            if name:
                items.append((name, link))

    return items


async def check_new_items():

    items = await asyncio.to_thread(get_items)

    for name, link in items:

        if link not in sent_links:

            sent_links.add(link)

            if BRAND in name.lower():

                await bot.send_message(
                    CHAT_ID,
                    f"🛍 Новий H&M на Shafa\n\n{name}\n{link}"
                )


async def main():

    app = ApplicationBuilder().token(TOKEN).build()

    await bot.send_message(CHAT_ID, "✅ Бот запущено і шукає H&M")

    while True:

        await check_new_items()

        await asyncio.sleep(120)


if __name__ == "__main__":
    asyncio.run(main())
    
