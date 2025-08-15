import requests
import os

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

WHATSAPP_API_URL = f"https://graph.facebook.com/v22.0/{PHONE_ID}/messages"

def enviar_mensagem(numero_destino: str, mensagem: str):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "text",
        "text": {"body": mensagem}
    }

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)

    print("Enviando mensagem:", payload)
    print("Status:", response.status_code)
    print("Resposta:", response.text)

    return response.status_code, response.json()
