FROM python:3.13-slim

# ====== Оновлення та необхідні пакети ======
RUN apt-get update && apt-get install -y \
    wget unzip xvfb curl ca-certificates \
    fonts-liberation libnss3 libx11-xcb1 libxcomposite1 \
    libxrandr2 libxi6 libgtk-3-0 libxss1 gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# ====== Google Chrome ======
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-linux-signing-key.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ====== Робоча директорія ======
WORKDIR /app

# ====== Копіюємо файли ======
COPY main.py .
COPY requirements.txt .

# ====== Встановлення Python пакетів ======
RUN pip install --no-cache-dir -r requirements.txt

# ====== Старт бота ======
CMD ["python", "main.py"]
