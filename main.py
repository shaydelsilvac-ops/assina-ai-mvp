from fastapi import FastAPI, Request
from pydantic import BaseModel

from supabase_client import buscar_usuario_por_telefone, criar_usuario
from openai_client import interpretar_mensagem
from whatsapp import enviar_mensagem

app = FastAPI()

class WebhookPayload(BaseModel):
    mensagem: str
    telefone: str

@app.post("/webhook")
async def webhook(payload: WebhookPayload):
    mensagem = payload.mensagem
    telefone = payload.telefone

    if not telefone or not mensagem:
        return {"erro": "mensagem ou telefone ausente"}

    usuario = buscar_usuario_por_telefone(telefone)

    if not usuario:
        texto = "Por favor, envie seu nome completo, e-mail e data de nascimento para cadastro."
        enviar_mensagem(telefone, texto)
        return {
            "status": "novo_usuario",
            "mensagem": texto
        }

    resposta = interpretar_mensagem(mensagem)
    enviar_mensagem(telefone, resposta)

    return {"resposta": resposta}

@app.get("/webhook")
def verificar():
    return "Endpoint de verificação GET (Meta)"
