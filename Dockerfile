# Базовий образ з Python 3.13
FROM python:3.13-slim

# Встановлюємо потрібні пакети для Chrome
RUN apt-get update && apt-get install -y \
    wget unzip xvfb gnupg2 curl ca-certificates \
    fonts-liberation libnss3 libx11-xcb1 libxcomposite1 libxrandr2 libxi6 libgtk-3-0 libxss1 \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Google Chrome stable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Створюємо робочу директорію
WORKDIR /app

# Копіюємо файли
COPY requirements.txt .
COPY main.py .

# Встановлюємо Python пакети
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Запуск бота
CMD ["python", "main.py"]
