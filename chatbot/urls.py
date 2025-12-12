from django.urls import path
from .views import telegram_webhook, chatbot_page
urlpatterns = [
    path('webhook/', telegram_webhook, name='telegram-webhook'),
    path('', chatbot_page, name='chatbot-page'),  # raíz de la app: /chatbot/

]


