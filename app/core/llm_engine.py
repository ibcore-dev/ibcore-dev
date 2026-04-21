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

def build_context_window(history, user_input, system_prompt):

    messages = []

    # 🔥 system prompt (identidade)
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    # 🔥 histórico (últimas 8 interações)
    if history:
        for h in (history or [])[-8:]:
            try:
                if isinstance(h, dict):
                    user_msg = h.get("input")
                    bot_msg = h.get("response")
                elif isinstance(h, tuple):
                    user_msg = h[0] if len(h) > 0 else None
                    bot_msg = h[1] if len(h) > 1 else None
                else:
                    continue

                if user_msg:
                    messages.append({
                        "role": "user",
                        "content": user_msg
                    })

                if bot_msg:
                    messages.append({
                        "role": "assistant",
                        "content": bot_msg
                    })

            except:
                continue

    # 🔥 mensagem atual
    messages.append({
        "role": "user",
        "content": user_input
    })

    return messages

def generate_llm_response(user_input, history=None, system_prompt=None):

    try:
        if not user_input:
            return "Pode me falar melhor o que você quer?"

        if not API_KEY:
            print("⚠️ Sem API KEY - LLM desativado")
            return "Estou com dificuldade de acessar minha inteligência agora. Tenta de novo daqui a pouco."

        print("📡 Enviando para LLM...")

        messages = build_context_window(
            history=history,
            user_input=user_input,
            system_prompt=system_prompt
        )

        # converter pra texto (porque seu provider usa string)
        prompt_final = ""

        for m in messages:
            if m["role"] == "system":
                prompt_final += f"[SISTEMA]: {m['content']}\n"
            elif m["role"] == "user":
                prompt_final += f"[USUÁRIO]: {m['content']}\n"
            elif m["role"] == "assistant":
                prompt_final += f"[ÓRION]: {m['content']}\n"
            if len(prompt_final) > 4000:
                prompt_final = prompt_final[-4000:]
            
            print("📦 TAMANHO CONTEXTO:", len(prompt_final))
        
        response = provider.generate(prompt_final)

        if not response:
            print("⚠️ LLM não retornou resposta")
            return "Deu uma falha aqui ao gerar resposta. Me manda de novo?"

        print("🧠 Resposta LLM:", response)

        return response

    except Exception as e:
        print("❌ Erro LLM Engine:", e)
        return "Ocorreu um erro ao processar sua mensagem."