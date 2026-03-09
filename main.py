import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Твій Telegram токен
TOKEN = 8206782935:AAEk10Lu_RbcyHrPgNA5OWuUJbL7jgcgjvE


# Базова URL Shafa
BASE_URL = "https://shafa.ua/search?search_text={query}&brand_name=Uniqlo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені назву товару від Uniqlo, Cos чи Arket.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Введи назву товару після команди /search")
        return

    url = BASE_URL.format(query=query.replace(" ", "+"))
    response = requests.get(url)
    if response.status_code != 200:
        await update.message.reply_text("Не вдалося отримати дані з Shafa")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("div.catalog__item")[:5]  # беремо максимум 5 результатів

    if not items:
        await update.message.reply_text("Не знайдено товарів 😢")
        return

    messages = []
    for item in items:
        title_tag = item.select_one("a.catalog__item-name")
        price_tag = item.select_one("span.catalog__price")
        link_tag = title_tag.get("href") if title_tag else None

        title = title_tag.get_text(strip=True) if title_tag else "Без назви"
        price = price_tag.get_text(strip=True) if price_tag else "Ціна невідома"
        link = f"https://shafa.ua{link_tag}" if link_tag else "Посилання відсутнє"

        messages.append(f"{title}\n{price}\n{link}")

    await update.message.reply_text("\n\n".join(messages))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    print("Бот запущений...")
    app.run_polling()
  
