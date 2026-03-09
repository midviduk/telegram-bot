import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue

# ----------------------
# Налаштування бота
# ----------------------
TOKEN = "ВАШ_TELEGRAM_BOT_TOKEN"  # <-- встав сюди свій токен
CHAT_ID = "ВАШ_CHAT_ID"           # <-- ID чату куди надсилати повідомлення

# ----------------------
# Листи для відстеження
# ----------------------
last_seen = {
    "uniqlo": set(),
    "cos": set(),
    "arket": set()
}

# ----------------------
# Функція для перевірки нових товарів
# ----------------------
async def check_new_items(context: ContextTypes.DEFAULT_TYPE):
    urls = {
        "uniqlo": "https://shafa.ua/uk/uniqlo",
        "cos": "https://shafa.ua/uk/cos",
        "arket": "https://shafa.ua/uk/arket"
    }
    
    for brand, url in urls.items():
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Всі товари на сторінці
            items = soup.select("div.catalog-product-card__name")  
            new_items = []
            
            for item in items:
                name = item.get_text(strip=True)
                if name not in last_seen[brand]:
                    last_seen[brand].add(name)
                    new_items.append(name)
            
            # Надсилаємо нові товари у Telegram
            for name in new_items:
                await context.bot.send_message(chat_id=CHAT_ID, text=f"{brand.upper()}: {name}")
        
        except Exception as e:
            print(f"Помилка при перевірці {brand}: {e}")

# ----------------------
# Команда /start
# ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Бот запущено і перевіряє нові товари кожні 2 хвилини.")

# ----------------------
# Запуск бота
# ----------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    # Запускаємо перевірку кожні 2 хвилини
    job_queue: JobQueue = app.job_queue
    job_queue.run_repeating(check_new_items, interval=120, first=5)  # 120 сек = 2 хв
    
    print("Бот запущено!")
    app.run_polling()
