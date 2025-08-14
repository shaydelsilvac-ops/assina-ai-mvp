import requests
import os

WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")

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
    return response.status_code, response.json()
