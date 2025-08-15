import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def interpretar_mensagem(mensagem: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que ajuda usuários com assinatura de documentos"},
                {"role": "user", "content": mensagem}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"[ERRO OPENAI] {e}")
        return "Desculpe, tivemos um problema ao processar sua mensagem. Tente novamente em instantes."
