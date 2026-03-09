import time
import json
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import telebot

# ====== Налаштування бота ======
TOKEN = "ТУТ_ВСТАВ_СВІЙ_BOT_TOKEN"
CHAT_ID_FILE = "my_chat_id.txt"

if os.path.exists(CHAT_ID_FILE):
    with open(CHAT_ID_FILE, "r") as f:
        CHAT_ID = int(f.read().strip())
else:
    CHAT_ID = None

bot = telebot.TeleBot(TOKEN)

# ====== Автоотримання CHAT_ID ======
if CHAT_ID is None:
    print("Відправ свій ID у бот у Telegram...")
    updates = bot.get_updates()
    if updates:
        CHAT_ID = updates[-1].message.chat.id
        with open(CHAT_ID_FILE, "w") as f:
            f.write(str(CHAT_ID))
        bot.send_message(CHAT_ID, "Бот запустився ✅")
    else:
        print("Надішли будь-яке повідомлення боту у Telegram і перезапусти контейнер")
        exit()

# ====== Налаштування Shafa ======
BRANDS = ["uniqlo", "cos", "arket"]
URL_TEMPLATE = "https://shafa.ua/{brand}?page={page}"

# Файл для збереження вже надісланих позицій
SENT_FILE = "sent_items.json"
if os.path.exists(SENT_FILE):
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        sent_items = set(json.load(f))
else:
    sent_items = set()

# ====== Запуск Chrome ======
options = uc.ChromeOptions()
options.headless = True
driver = uc.Chrome(options=options)

def fetch_items():
    new_items = []
    for brand in BRANDS:
        url = URL_TEMPLATE.format(brand=brand, page=1)
        driver.get(url)
        time.sleep(3)

        products = driver.find_elements(By.CSS_SELECTOR, "div.catalog-tile__inner")
        for p in products:
            try:
                name = p.find_element(By.CSS_SELECTOR, "a.catalog-tile__title").text.strip()
                price_text = p.find_element(By.CSS_SELECTOR, "span.catalog-tile__price-value").text.strip()
                price = int(price_text.replace("₴", "").replace(",", "").strip())
                link = p.find_element(By.CSS_SELECTOR, "a.catalog-tile__title").get_attribute("href")
                uid = link.split("/")[-1]

                if uid not in sent_items and price < 2000:
                    new_items.append((name, price, link))
                    sent_items.add(uid)
            except:
                continue
    return new_items

# ====== Основний цикл ======
try:
    while True:
        items = fetch_items()
        if items:
            for name, price, link in items:
                bot.send_message(CHAT_ID, f"{name} — {price}₴\n{link}")
            with open(SENT_FILE, "w", encoding="utf-8") as f:
                json.dump(list(sent_items), f, ensure_ascii=False)
        time.sleep(60)
except KeyboardInterrupt:
    driver.quit()
    bot.send_message(CHAT_ID, "Бот зупинений ✋")
