# Official Playwright Python image
FROM mcr.microsoft.com/playwright/python:v1.54.0-jammy

# Uygulama dizini oluştur
WORKDIR /app

# requirements.txt kopyala ve yükle
COPY requirements.txt .
RUN pip install -r requirements.txt

# playwright install komutunu çalıştır
RUN playwright install chromium

# Python dosyalarını kopyala
COPY . .

# Sunucuyu başlat
CMD ["python", "api.py"]