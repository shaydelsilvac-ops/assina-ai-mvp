from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def buscar_usuario_por_telefone(telefone):
    response = supabase.table("usuarios").select("*").eq("telefone", telefone).execute()
    return response.data

def criar_usuario(telefone, nome=None, email=None, nascimento=None):
    data = {
        "telefone": telefone,
        "nome": nome,
        "email": email,
        "data_nascimento": nascimento
    }
    return supabase.table("usuarios").insert(data).execute()
