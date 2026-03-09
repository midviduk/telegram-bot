import requests
from bs4 import BeautifulSoup
import telebot
import os
import time

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = telebot.TeleBot(TOKEN)
sent_links = set()
headers = {"User-Agent": "Mozilla/5.0"}
brands = ["uniqlo", "cos", "arket"]

bot.send_message(CHAT_ID, "Бот запустився і ловитиме нові товари <2000 грн")

def check_items():
    for brand in brands:
        url = f"https://shafa.ua/uk/clothes?search={brand}"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        # знайдемо всі карточки товарів
        product_cards = soup.find_all("div", {"data-testid": "ProductCard"})

        for card in product_cards:
            # посилання
            a_tag = card.find("a", href=True)
            if not a_tag:
                continue
            full_link = "https://shafa.ua" + a_tag["href"]

            # ціна
            price_tag = card.find("div", {"data-testid": "Price"})
            if not price_tag:
                continue
            price_text = price_tag.get_text().replace("грн", "").replace(" ", "")
            try:
                price = int(price_text)
            except:
                continue

            if price < 2000 and full_link not in sent_links:
                bot.send_message(CHAT_ID, f"{brand.upper()} {price} грн\n{full_link}")
                sent_links.add(full_link)

while True:
    try:
        check_items()
    except Exception as e:
        print(e)
    time.sleep(300)
    
