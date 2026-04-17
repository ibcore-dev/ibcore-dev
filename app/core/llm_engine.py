print("🔥 LLM ENGINE INICIADO")

from app.core.groq_provider import GroqProvider
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("❌ ERRO: GROQ_API_KEY não encontrada")

provider = GroqProvider(api_key=API_KEY)

def generate_llm_response(prompt):

    try:
        if not API_KEY:
            print("⚠️ Sem API KEY - LLM desativado")
            return None

        print("📡 Enviando para LLM...")

        response = provider.generate(prompt)

        print("🧠 Resposta LLM:", response)

        return response

    except Exception as e:
        print("❌ Erro LLM Engine:", e)
        return None