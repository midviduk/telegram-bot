import requests
from bs4 import BeautifulSoup
import telebot
import os
import time

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = telebot.TeleBot(TOKEN)

brands = ["uniqlo", "cos", "arket"]
sent_links = set()

headers = {
    "User-Agent": "Mozilla/5.0"
}

bot.send_message(CHAT_ID, "Бот запустився")

def check_items():

    for brand in brands:

        url = f"https://shafa.ua/uk/clothes?search={brand}"

        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, "html.parser")

        items = soup.find_all("a", href=True)

        for item in items:

            link = item["href"]

            if "/uk/" in link and brand in link:

                full_link = "https://shafa.ua" + link

                if full_link not in sent_links:

                    bot.send_message(
                        CHAT_ID,
                        f"{brand.upper()} знайдено\n{full_link}"
                    )

                    sent_links.add(full_link)


while True:

    try:
        check_items()

    except Exception as e:
        print(e)

    time.sleep(300)
