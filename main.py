import requests
import telebot
import os
import time

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = telebot.TeleBot(TOKEN)

brands = ["uniqlo", "cos", "arket"]

sent_links = set()

def check_items():
    for brand in brands:
        url = f"https://shafa.ua/api/v1/catalog?search={brand}"
        r = requests.get(url)
        data = r.json()

        for item in data.get("items", []):
            price = item["price"]

            if price < 2000:
                link = "https://shafa.ua" + item["url"]

                if link not in sent_links:
                    text = f"{brand.upper()} — {price} грн\n{link}"
                    bot.send_message(CHAT_ID, text)

                    sent_links.add(link)

while True:
    try:
        check_items()
    except Exception as e:
        print(e)

    time.sleep(300)
