from fastapi import FastAPI, Request
import os
from supabase_client import buscar_usuario_por_telefone, criar_usuario
from openai_client import interpretar_mensagem

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    mensagem = data.get("mensagem")
    telefone = data.get("telefone")

    if not telefone or not mensagem:
        return {"erro": "mensagem ou telefone ausente"}

    usuario = buscar_usuario_por_telefone(telefone)

    if not usuario:
        return {
            "status": "novo_usuario",
            "mensagem": "Por favor, envie seu nome completo, e-mail e data de nascimento para cadastro."
        }

    resposta = interpretar_mensagem(mensagem)
    return {"resposta": resposta}
