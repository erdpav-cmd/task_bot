import requests

try:
    response = requests.get("https://api.telegram.org", timeout=10)
    print("✅ Telegram доступен!")
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
    print("Проверьте VPN/интернет")