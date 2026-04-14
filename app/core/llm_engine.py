print("🔥 LLM CHAMADO")
from app.core.groq_provider import GroqProvider
import os
from dotenv import load_dotenv

# carrega .env
load_dotenv()

provider = GroqProvider(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_llm_response(prompt):

    try:
        return provider.generate(prompt)

    except Exception as e:
        print("Erro LLM Engine:", e)
        return None