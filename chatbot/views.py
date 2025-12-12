from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json
from django.shortcuts import render

# Token del bot
TELEGRAM_TOKEN = '8229620787:AAEUBwMAqkXuqWNusyFAtws_YwToQWWLObk'
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

# Diccionario para guardar el estado de cada usuario
usuarios_estado = {}  # chat_id: estado_actual
usuarios_data = {}    # chat_id: datos temporales (para formularios)

# Estados posibles
ESTADO_MENU = "MENU"
ESTADO_INFORMACION = "INFORMACION"
ESTADO_INFORMACION_DETALLE = "INFORMACION_DETALLE"
ESTADO_SOPORTE = "SOPORTE"
ESTADO_SOPORTE_FORM = "SOPORTE_FORM"
ESTADO_CONTACTO = "CONTACTO"
ESTADO_FINAL = "FINAL"

# Función para crear menú principal
def generar_menu():
    return {
        "keyboard": [
            [{"text": "Información"}],
            [{"text": "Soporte"}],
            [{"text": "Contacto"}],
            [{"text": "Salir"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }

# Submenú de información
def generar_submenu_informacion():
    return {
        "keyboard": [
            [{"text": "Productos"}],
            [{"text": "Servicios"}],
            [{"text": "Volver al menú"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }

# Función para procesar opciones según estado
def procesar_opcion(chat_id, opcion):
    opcion = opcion.lower()
    estado_actual = usuarios_estado.get(chat_id, ESTADO_MENU)
    
    # Salir
    if opcion == "salir":
        usuarios_estado[chat_id] = ESTADO_FINAL
        usuarios_data.pop(chat_id, None)
        return "Gracias por usar el asistente. ¡Hasta luego!", None

    # Menú principal
    if estado_actual == ESTADO_MENU:
        if opcion in ["información", "informacion"]:
            usuarios_estado[chat_id] = ESTADO_INFORMACION
            return "Selecciona una categoría de información:", generar_submenu_informacion()
        elif opcion == "soporte":
            usuarios_estado[chat_id] = ESTADO_SOPORTE_FORM
            usuarios_data[chat_id] = {"ticket": ""}
            return "Por favor describe tu problema para generar un ticket:", None
        elif opcion == "contacto":
            usuarios_estado[chat_id] = ESTADO_CONTACTO
            return "Puedes contactarnos al correo pedrazasantiago837@ejemplo.com o al teléfono 123456789.", generar_menu()
        else:
            return "No entendí tu elección. Por favor selecciona una opción del menú:", generar_menu()

    # Submenú de información
    if estado_actual == ESTADO_INFORMACION:
        if opcion == "productos":
            return "Nuestros productos incluyen A, B y C. ¿Deseas volver al menú principal?", generar_menu()
        elif opcion == "servicios":
            return "Ofrecemos servicios de X, Y y Z. ¿Deseas volver al menú principal?", generar_menu()
        elif opcion == "volver al menú":
            usuarios_estado[chat_id] = ESTADO_MENU
            return "Volviendo al menú principal:", generar_menu()
        else:
            return "Opción no válida en información. Elige Productos, Servicios o Volver al menú:", generar_submenu_informacion()

    # Soporte - formulario
    if estado_actual == ESTADO_SOPORTE_FORM:
        usuarios_data[chat_id]["ticket"] = opcion
        usuarios_estado[chat_id] = ESTADO_SOPORTE
        return f"Gracias, tu ticket ha sido recibido:\n'{opcion}'\nNuestro equipo de soporte se pondrá en contacto pronto.", generar_menu()

    return "No entendí tu elección. Volviendo al menú principal:", generar_menu()

@api_view(['POST'])
def telegram_webhook(request):
    data = request.data
    message = data.get('message')
    if not message:
        return Response({"status": "no message"}, status=200)

    chat = message.get('chat')
    text = message.get('text')
    if not chat or not text:
        return Response({"status": "no chat or text"}, status=200)

    chat_id = chat['id']
    text_lower = text.lower()

    # Inicio flexible
    if text_lower in ["/start", "hola"]:
        usuarios_estado[chat_id] = ESTADO_MENU
        respuesta = (
            "¡Hola! Soy tu asistente virtual.\n"
            "Puedes iniciar la conversación usando los botones o escribiendo las opciones directamente:\n"
            "- Información\n"
            "- Soporte\n"
            "- Contacto\n"
            "- Salir\n\n"
            "Selecciona una opción para continuar:"
        )
        menu = generar_menu()
    else:
        respuesta, menu = procesar_opcion(chat_id, text)

    payload = {"chat_id": chat_id, "text": respuesta}
    if menu:
        payload["reply_markup"] = json.dumps(menu)

    requests.post(TELEGRAM_URL, data=payload)
    return Response({"status": "ok"})

def chatbot_page(request):
    return render(request, 'chatbot/chatbot.html')
