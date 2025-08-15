from fastapi import FastAPI, Request
from openai_client import interpretar_mensagem
from supabase_client import buscar_usuario_por_telefone, criar_usuario
from whatsapp import enviar_mensagem

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    try:
        mensagem = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        telefone = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    except (KeyError, IndexError):
        return {"erro": "formato de mensagem inválido"}

    usuario = buscar_usuario_por_telefone(telefone)

    if not usuario:
        resposta = "Por favor, envie seu nome completo, e-mail e data de nascimento para cadastro."
        enviar_mensagem(telefone, resposta)
        return {
            "status": "novo_usuario",
            "mensagem": resposta
        }

    resposta = interpretar_mensagem(mensagem)
    enviar_mensagem(telefone, resposta)

    return {"resposta": resposta}


@app.get("/webhook")
def verificar(token: str = "", challenge: str = "", mode: str = ""):
    VERIFY_TOKEN = "assinaai2024"  # Esse é o token que você define no app da Meta
    if token == VERIFY_TOKEN and mode == "subscribe":
        return int(challenge)
    return {"erro": "Token de verificação inválido"}
