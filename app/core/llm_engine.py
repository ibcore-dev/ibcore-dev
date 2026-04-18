print("🔥 LLM ENGINE INICIADO")

import os
from dotenv import load_dotenv
from app.core.groq_provider import GroqProvider

# 🔑 FORÇA CARREGAMENTO DO .env (funciona em qualquer estrutura)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=dotenv_path)

# 🔑 BUSCAR KEY
API_KEY = os.getenv("GROQ_API_KEY")

print("🔍 DEBUG KEY:", API_KEY if API_KEY else "NÃO ENCONTRADA")

# 🔧 CRIAR PROVIDER
provider = GroqProvider(api_key=API_KEY)


def generate_llm_response(prompt):

    try:
        if not API_KEY:
            print("⚠️ Sem API KEY - LLM desativado")
            return "Estou com dificuldade de acessar minha inteligência agora. Tenta de novo daqui a pouco."

        print("📡 Enviando para LLM...")

        response = provider.generate(prompt)

        if not response:
            print("⚠️ LLM não retornou resposta")
            return "Deu uma falha aqui ao gerar resposta. Me manda de novo?"

        print("🧠 Resposta LLM:", response)

        return response

    except Exception as e:
        print("❌ Erro LLM Engine:", e)
        return "Ocorreu um erro ao processar sua mensagem."