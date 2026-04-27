import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_FILE = os.getenv("DATABASE_FILE", "tasks.db")

if not BOT_TOKEN:
    raise ValueError("❌ Токен бота не найден в .env файле!")