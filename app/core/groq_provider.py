from groq import Groq
from app.core.llm_provider import LLMProvider


class GroqProvider(LLMProvider):

    def __init__(self, api_key):

        if not api_key:
            print("❌ GROQ_API_KEY NÃO DEFINIDA")
            self.client = None
        else:
            try:
                self.client = Groq(api_key=api_key)
                print("✅ Groq Provider conectado")
            except Exception as e:
                print("❌ Erro ao iniciar Groq:", e)
                self.client = None

    def generate(self, prompt):

        if not self.client:
            print("❌ LLM CLIENT NÃO INICIALIZADO")
            return None

        try:
            chat = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-8b-instant",
                temperature=0.5
            )

            if not chat or not chat.choices:
                print("⚠️ LLM sem resposta válida")
                return None

            return chat.choices[0].message.content

        except Exception as e:
            print("❌ Erro Groq:", e)
            return None