import telebot
import os

TOKEN = os.environ.get("TOKEN")  # Твій токен бота

bot = telebot.TeleBot(TOKEN)

# Цей хендлер ловить будь-яке повідомлення і виводить твій CHAT_ID
@bot.message_handler(func=lambda message: True)
def get_chat_id(message):
    bot.reply_to(message, f"Твій CHAT_ID: {message.chat.id}")
    print(f"CHAT_ID = {message.chat.id}")  # ще в логи

bot.polling()
