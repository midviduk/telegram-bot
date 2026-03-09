# Використовуємо стабільний Python з distutils
FROM python:3.12-slim

# Робоча папка
WORKDIR /app

# Встановлюємо системні залежності для Chrome та Selenium
RUN apt-get update && apt-get install -y \
    wget unzip xvfb curl ca-certificates gnupg2 fonts-liberation \
    libnss3 libx11-xcb1 libxcomposite1 libxrandr2 libxi6 libgtk-3-0 libxss1 gpg \
    && rm -rf /var/lib/apt/lists/*

# Додаємо репозиторій Google Chrome
RUN wget -q -O /usr/share/keyrings/google-linux-signing-key.gpg https://dl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо файли проєкту
COPY requirements.txt .
COPY main.py .

# Оновлюємо pip та встановлюємо Python-залежності
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Запуск бота
CMD ["python", "main.py"]
