from groq import Groq
from app.core.llm_provider import LLMProvider


class GroqProvider(LLMProvider):

    def __init__(self, api_key):

        if not api_key:
            print("⚠️ GROQ_API_KEY NÃO DEFINIDA")
            self.client = None
        else:
            self.client = Groq(api_key=api_key)

    def generate(self, prompt):

        if not self.client:
            print("⚠️ LLM desativado (sem API KEY)")
            return None

        try:
            print("📡 Chamando Groq...")

            chat = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.1-8b-instant"
            )

            resposta = chat.choices[0].message.content

            print("🧠 Groq respondeu:", resposta)

            return resposta

        except Exception as e:
            print("❌ Erro Groq:", str(e))
            return None