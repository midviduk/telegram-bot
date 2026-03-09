import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder

# Токен твого бота
TOKEN = "8206782935:AAEk10Lu_RbcyHrPgNA5OWuUJbL7jgcgjvE"
CHAT_ID = 313800446

# Список брендів — тільки Uniqlo
BRANDS = ["Uniqlo"]

# Приклад функції, яка перевіряє нові товари
async def check_new_items(app):
    # Тут вставляй свій код парсера з Shafa
    # Для прикладу — список нових товарів
    items = [
        "Uniqlo Червона сорочка",
        "Cos Синя сумка",
        "Arket Джинси",
        "Uniqlo Світшот"
    ]

    for item_name in items:
        if "uniqlo" in item_name.lower():
            await app.bot.send_message(chat_id=CHAT_ID, text=f"Знайдено новий товар Uniqlo: {item_name}")
            print(f"Надіслано повідомлення: {item_name}")

async def main():
    # Створюємо додаток бота
    app = ApplicationBuilder().token(TOKEN).build()

    # Перша перевірка відразу при запуску
    await check_new_items(app)

    # JobQueue для повторної перевірки кожні 120 секунд (2 хв)
    app.job_queue.run_repeating(check_new_items, interval=120, first=120)

    print("Бот запущено, перевірка Uniqlo кожні 2 хвилини...")
    
    # Запускаємо бота
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()  # Зупиняє програму, бот працює постійно

if __name__ == "__main__":
    asyncio.run(main())
