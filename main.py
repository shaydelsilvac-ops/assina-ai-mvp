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
async def verificar(request: Request):
    params = request.query_params
    if (
        params.get("hub.mode") == "subscribe" and
        params.get("hub.verify_token") == "assinaai2024"
    ):
        return int(params.get("hub.challenge"))
    return {"erro": "Token inválido"}

