import time
import telebot
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

# =================== Налаштування ===================
TOKEN = "тут_твій_токен_бота"
CHAT_ID = "твоє_число_ID"
bot = telebot.TeleBot(TOKEN)

brands = ["uniqlo", "cos", "arket"]  # бренди, за якими шукаємо
sent_links = set()  # щоб не надсилати дублікати

bot.send_message(CHAT_ID, "Бот запустився і ловитиме нові товари <2000 грн")

# =================== Headless Chrome ===================
options = uc.ChromeOptions()
options.headless = True
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = uc.Chrome(options=options)

# =================== Функція перевірки ===================
def check_items():
    for brand in brands:
        url = f"https://shafa.ua/uk/clothes?search={brand}"
        driver.get(url)
        time.sleep(5)  # чекаємо, поки JS підвантажить товари

        soup = BeautifulSoup(driver.page_source, "html.parser")
        product_cards = soup.find_all("div", {"data-testid": "ProductCard"})

        for card in product_cards:
            a_tag = card.find("a", href=True)
            if not a_tag:
                continue
            full_link = "https://shafa.ua" + a_tag["href"]
            if full_link in sent_links:
                continue

            # Назва
            title_tag = card.find("div", {"data-testid": "ProductTitle"})
            title = title_tag.get_text() if title_tag else "Назва відсутня"

            # Ціна
            price_tag = card.find("div", {"data-testid": "Price"})
            if not price_tag:
                continue
            price_text = price_tag.get_text().replace("грн", "").replace(" ", "")
            try:
                price = int(price_text)
            except:
                continue
            if price > 2000:
                continue

            # Фото
            img_tag = card.find("img")
            img_url = img_tag["src"] if img_tag else None

            msg = f"{brand.upper()} | {title} | {price} грн\n{full_link}"
            if img_url:
                bot.send_photo(CHAT_ID, img_url, caption=msg)
            else:
                bot.send_message(CHAT_ID, msg)

            sent_links.add(full_link)

# =================== Цикл перевірки ===================
while True:
    try:
        check_items()
    except Exception as e:
        print("Помилка:", e)
    time.sleep(30)  # перевірка кожні 30 секунд
