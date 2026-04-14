from groq import Groq
from app.core.llm_provider import LLMProvider


class GroqProvider(LLMProvider):

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def generate(self, prompt):

        try:
            chat = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-8b-instant"
            )

            return chat.choices[0].message.content

        except Exception as e:
            print("Erro Groq:", e)
            return None