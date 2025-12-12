import requests

TOKEN = "8229620787:AAEUBwMAqkXuqWNusyFAtws_YwToQWWLObk"
# En set_webhook.py, usa esta URL EXACTA:
WEBHOOK_URL = "https://particia-unpromotable-generically.ngrok-free.dev/chatbot/webhook/"


url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
r = requests.get(url)
print(r.text)
