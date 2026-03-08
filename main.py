import requests
from bs4 import BeautifulSoup
import telebot
import os
import time

TOKEN = os.environ.get("TOKEN")  # твій Telegram TOKEN
CHAT_ID = os.environ.get("CHAT_ID")  # твій Telegram ID
bot = telebot.TeleBot(TOKEN)

def get_items():
    brands = ["uniqlo", "cos", "arket"]
    items = []
    for brand in brands:
        url = f"https://shafa.ua/uk/women?search={brand}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        for el in soup.select(".catalog-card"):
            price_tag = el.select_one(".catalog-card__price")
            if price_tag:
                price_text = price_tag.text.replace(" грн", "").replace(" ", "")
                price = int(price_text)
                if price < 2000:
                    link = "https://shafa.ua" + el.find("a")["href"]
                    items.append((brand, price, link))
    return items

sent_items = set()

while True:
    for brand, price, link in get_items():
        if link not in sent_items:
            bot.send_message(CHAT_ID, f"{brand.upper()} — {price} грн\n{link}")
            sent_items.add(link)
    time.sleep(300)  # перевірка кожні 15 хвилин
