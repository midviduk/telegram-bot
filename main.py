import telebot
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

# Встав свій токен бота
TOKEN = "ТУТ_ТОКЕН_БОТА"
bot = telebot.TeleBot(TOKEN)

# Простий тест на старт
bot.send_message(chat_id="ТУТ_ID_ЧАТУ", text="Бот запустився ✅")

# Запуск Chrome через undetected_chromedriver
options = uc.ChromeOptions()
options.headless = True  # Запуск без вікна
driver = uc.Chrome(options=options)

# Проста перевірка Shafa
driver.get("https://shafa.ua")
time.sleep(3)
title = driver.title
driver.quit()

# Надсилаємо назву сторінки у Telegram
bot.send_message(chat_id="ТУТ_ID_ЧАТУ", text=f"Shafa відкрито: {title}")
