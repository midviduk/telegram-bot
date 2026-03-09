FROM python:3.12-slim

WORKDIR /app

# Оновлюємо pip і встановлюємо бібліотеки
RUN pip install --upgrade pip
RUN pip install "python-telegram-bot[job-queue]" requests beautifulsoup4

# Копіюємо твій код
COPY main.py .

# Запуск бота
CMD ["python", "main.py"]
