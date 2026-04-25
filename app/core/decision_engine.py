import app.core.memory_manager as memory
from app.core.response_builder import build_response
from app.core.context_engine import update_context, get_context
from app.core.semantic_engine import detect_semantic_state
from app.core.knowledge_extractor import extract_user_knowledge
from app.core.episodic_memory import save_episode, recall_episode
from app.core.self_evolution import learn_from_conversation
from app.core.thought_engine import generate_thought
from app.core.attention_engine import calculate_attention
from app.core.continuity_engine import detect_continuity
from app.core.reflection_engine import reflect
from app.core.priority_engine import calculate_priority
from app.core.metacognition_engine import metacognitive_check
from app.core.cognitive_loop import cognitive_loop
from app.core.learning_pattern_engine import detect_learning_pattern
from app.core.context_focus_engine import determine_focus
from app.core.technical_memory_engine import check_technical_memory
from app.core.goal_engine import goal_response
from app.core.planner_engine import planner_response
from app.core.progress_engine import get_progress, advance_progress
from app.core.conversation_intelligence_engine import detect_pending_question, continue_conversation
from app.core.conversation_goal_engine import detect_goal
from app.core.dialogue_memory_engine import detect_main_topic, conversation_already_answered
from database.database import SessionLocal
from database.models import Profile, User
from datetime import datetime
from zoneinfo import ZoneInfo
import pytz
from app.core.intent_engine import detect_intent, detect_intent_llm, detect_emotion
from app.core.intent_engine import detect_emotion
import random
from database.database import SessionLocal
from database.models import Message

# =================================================
# BIBLIOTECA EMOCIONAL — ORION
# =================================================

EMOTION_LIBRARY = {

    "forte": [
        "medo", "com medo", "ansioso", "ansiedade",
        "pânico", "desesperado", "desesperada",
        "apavorado", "apavorada",
        "angustiado", "angustiada",
        "sobrecarregado", "sobrecarregada",
        "exausto", "exausta"
    ],

    "media": [
        "inseguro", "insegura",
        "preocupado", "preocupada",
        "desanimado", "desanimada",
        "frustrado", "frustrada",
        "confuso", "confusa",
        "pressionado", "pressionada",
        "tenso", "tensa"
    ],

    "leve": [
        "cansado", "cansada",
        "triste",
        "chateado", "chateada",
        "desmotivado", "desmotivada",
        "irritado", "irritada"
    ]
}

def get_user_profile(username: str):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == username).first()

        if not user:
            return None

        profile = db.query(Profile).filter(Profile.user_id == user.id).first()

        return profile

    finally:
        db.close()
# =================================================
# DETECTAR INTENSIDADE EMOCIONAL
# =================================================

def detect_emotional_intensity(text: str):

    text = text.lower()

    for word in EMOTION_LIBRARY["forte"]:
        if word in text:
            return "forte", 9

    for word in EMOTION_LIBRARY["media"]:
        if word in text:
            return "media", 6

    for word in EMOTION_LIBRARY["leve"]:
        if word in text:
            return "leve", 4

    return None, 0


# =================================================
# CONTEXTO RELACIONAL
# =================================================

def build_relational_context(username: str):

    context = {
        "last_topic": None,
        "last_intent": None,
        "last_emotional_state": None,
        "has_active_episode": False
    }

    previous_state = memory.get_user_state(username)

    if previous_state:
        context["last_topic"] = previous_state[0]
        context["last_emotional_state"] = previous_state[2]
        context["last_intent"] = previous_state[3]

    active_episode = memory.get_active_episode(username)

    if active_episode:
        context["has_active_episode"] = True

    return context


# =================================================
# PADRÕES COMPORTAMENTAIS
# =================================================

def detect_behavior_pattern(username: str):

    history = memory.get_last_messages(username, 25) or []

    if not isinstance(history, list):
        history = []

    decision_count = 0
    action_count = 0
    emotional_high = 0
    emotional_sequence = 0
    last_emotion = 0

    for h in history:

        if isinstance(h, tuple):

            topic = h[0] if len(h) > 0 else None
            mode = h[1] if len(h) > 1 else None
            emotional_score = h[2] if len(h) > 2 else 0
            intent = h[3] if len(h) > 3 else None

        else:
            continue

        if intent == "decisao":
            decision_count += 1

        if intent == "acao":
            action_count += 1

        if emotional_score and emotional_score >= 6:
            emotional_high += 1

        if emotional_score and last_emotion:
            if abs(emotional_score - last_emotion) >= 5:
                emotional_sequence += 1

        last_emotion = emotional_score or 0

    if emotional_high >= 3:
        return "emocional_recorrente"

    if action_count >= 3:
        return "impulsividade_execucao"

    if decision_count >= 3:
        return "busca_validacao"

    if emotional_sequence >= 3:
        return "instabilidade_emocional"

    return None


# =================================================
# ADAPTAÇÃO COGNITIVA
# =================================================

def adapt_cognitive_identity(base_identity: str, behavior_pattern: str):

    if not behavior_pattern:
        return base_identity

    if behavior_pattern == "busca_validacao":
        return "estrategico_firme"

    if behavior_pattern == "emocional_recorrente":
        return "apoio_emocional"

    if behavior_pattern == "impulsividade_execucao":
        return "mentor_equilibrado"

    if behavior_pattern == "instabilidade_emocional":
        return "mentor_equilibrado"

    return base_identity


# =================================================
# DETECTAR TEMA
# =================================================

def detect_topic(text: str):

    text = (text or "").lower()

    if any(word in text for word in ["dinheiro", "finança", "vender", "lucro"]):
        return "financeiro"

    if any(word in text for word in ["projeto", "orion", "sistema", "codigo"]):
        return "projeto"

    if any(word in text for word in [
        "cansado", "feliz", "animado", "triste",
        "inseguro", "ansioso", "preocupado",
        "medo", "desanimado"
    ]):
        return "emocional"

    if any(word in text for word in ["empresa", "negócio", "cliente"]):
        return "negocio"

    return "geral"


# =================================================
# DETECTAR INTENÇÃO
# =================================================

def detect_intent(text: str):

    text = (text or "").lower()
    texto_limpo = text.strip()
    palavras = texto_limpo.split()

    despedidas = [
        "tchau", "até mais", "falou", "vou ali",
        "fui", "até logo", "valeu", "flw", "bye"
    ]

    # 🔥 bloqueio de falso positivo (ex: "ela falou comigo")
    if any(p in texto_limpo for p in ["falou", "fui", "vou"]) and len(palavras) > 3:
        pass  # NÃO retorna despedida, continua fluxo

    # ✅ despedida real
    elif len(palavras) <= 3 and any(p in texto_limpo for p in despedidas):
        return "despedida"

    # 🔹 pergunta
    if any(frase in text for frase in [
        "como faço", "como eu faço", "qual é",
        "me explica", "quero saber", "me fala"
    ]):
        return "pergunta"

    if any(word in text for word in ["como", "qual", "quando", "onde", "por que"]):
        return "pergunta"

    # 🔹 ação
    if any(word in text for word in ["preciso fazer", "vou fazer", "executar"]):
        return "acao"

    # 🔹 análise
    if any(word in text for word in ["analisar", "avaliar", "risco"]):
        return "analise"

    return "conversa"

def resolve_self_reference(user_input):

    text = user_input.lower()

    referencias_orion = [
        "você",
        "vc",
        "tu",
        "seu",
        "sua",
        "teu",
        "orion",
        "órion"
    ]

    for ref in referencias_orion:
        if ref in text:
            return True

    return False
# =================================
# 🧠 MEMÓRIA INTELIGENTE
# =================================
def gerar_memoria_inteligente(history):
    if not history:
        return ""

    pontos = []

    for msg in history:
        texto = (
            (msg.get("input") or "") + " " +
            (msg.get("response") or "")
        ).lower()

        if "reinici" in texto:
            pontos.append("O sistema do Órion foi reiniciado recentemente")

        if "erro" in texto:
            pontos.append("Houve erros recentes no sistema")

        if "memoria" in texto or "memória" in texto:
            pontos.append("Usuário está trabalhando na memória do Órion")

        if "projeto" in texto:
            pontos.append("Usuário está desenvolvendo o projeto Órion")

    return "\n".join(set(pontos))
# =================================================
# ENGINE PRINCIPAL
# =================================================

class DecisionEngine:

    def process(self, username: str, user_input: str):

        nome = memory.get_profile(username, "nome") 
        if not nome:
            nome = username

        if not username:
            raise ValueError("Username não pode ser vazio")

        ctx = update_context(username, user_input)
        text = user_input.lower()

        texto_limpo = text.strip()
        palavras = texto_limpo.split()
        
        is_about_orion = resolve_self_reference(user_input)

        intent = detect_intent(user_input)

        # 🔹 despedida
        if intent == "despedida":
            respostas = [
                f"Falou, {nome}. Até mais 👊",
                f"Beleza, {nome}. Até depois",
                f"Tamo junto, {nome}",
                f"Até mais, {nome}. Qualquer coisa chama"
            ]
            return random.choice(respostas)

        # 🔹 risada
        if any(p in texto_limpo for p in ["kkk", "kkkk", "kakaka"]):
            respostas = [
                f"kkk boa, {nome}. Manda aí",
                f"kkkk tô contigo, {nome}. O que foi?",
                f"kkk aí sim 😄 fala comigo"
            ]
            return random.choice(respostas)

        # 🔹 zoeira
        if len(palavras) <= 6 and any(p in texto_limpo for p in ["zoeira", "brincando"]):
            respostas = [
                f"kkk beleza, {nome}. Mas manda o que você quer de verdade",
                f"tá zoando né 😄 fala sério agora",
                f"boa kkk, mas e aí, qual é a real?"
            ]
            return random.choice(respostas)

        # 🔹 problema
        if any(p in texto_limpo for p in ["deu ruim", "fbi", "policia aqui"]):
            respostas = [
                f"calma aí, {nome}. O que aconteceu?",
                f"opa, {nome}… deu ruim como?",
                f"fala comigo, {nome}. Qual foi o problema?"
            ]
            return random.choice(respostas)

        # =================================
        # DETECTAR MODO EXECUTOR
        # =================================
        is_execution = False

        if ctx.get("state") == "criacao":
            if any(p in user_input.lower() for p in [
                "me ajuda com post",
                "faz um post",
                "cria um post",
                "faz pra mim",
                "gera um post"
            ]):
                is_execution = True
        state = ctx.get("state", "conversa")
        intent = ctx.get("intent", "conversa")

        # =========================
        # MODO DO ÓRION (CÉREBRO)
        # =========================
        mode = "normal"

        if state == "criacao":
            mode = "criador"

        elif state == "duvida":
            mode = "explicador"

        elif state == "planejamento":
            mode = "estrategico"
        state = ctx.get("state", "conversa")
        

        # PEGAR ESTADO E INTENT PRIMEIRO
        intent = ctx.get("intent", "conversa")
        state = ctx.get("state", "conversa")

        text = (user_input or "").lower()
        emotion = detect_emotion(user_input)

        # ===============================   
        # DETECÇÃO DE INTENT
        # ===============================
        intent = ctx.get("intent")

        if not intent:
           if len(user_input.split()) < 3:
                intent = detect_intent(user_input)
           else:
             intent = detect_intent_llm(user_input)

        if not intent:
           intent = "conversa"
            
        # =================================
        # RESPOSTAS DIRETAS (ANTES DE TUDO)
        # =================================
        if intent == "saudacao":

            respostas = [
                f"Fala {nome}, tudo certo?",
                f"Opa {nome}, tranquilo?",
                f"E aí {nome}, como você tá?",
                f"Salve {nome}, manda aí",
                f"Boa, {nome}. Chegou chegando hein"
            ]

            return random.choice(respostas)

        if intent == "positivo":
            return f"Boa, {nome}. Bora então."

        if intent == "negativo":
            return f"Tranquilo, {nome}. Sem problema."

        if intent == "incerto":
            return f"Sem pressão, {nome}. Pensa com calma."
        
        if intent == "despedida":

            respostas = [
                "Até mais, meu amigo 😎",
                "Falou, qualquer coisa chama 👊",
                "Tamo junto, até a próxima",
                "Hasta la vista, baby 😏"
            ]

            return random.choice(respostas)
        
        # =================================
        # DEFINIR USO DO LLM
        # =================================
        use_llm = False

        if state in ["criacao", "duvida", "planejamento"]:
            use_llm = True

        elif intent in ["pergunta", "analise"]:
            use_llm = True
        
        # =================================
        # RESPOSTA DIRETA PARA TEMPO
        # =================================
        if intent == "hora":
            return f"Agora são {self.get_time_brasilia()}"

        if intent == "data":
            return f"Hoje é {self.get_date_brasilia()}"
        # ===============================
        # MEMÓRIA REAL (BANCO)
        # ===============================
        db = SessionLocal()

        history_db = db.query(Message)\
            .filter(Message.username == username)\
            .order_by(Message.created_at.desc())\
            .limit(10)\
            .all()[::-1]

        history = []
        for msg in history_db:
        memory_hint = gerar_memoria_inteligente(history)    
            history.append({
                "input": msg.content if msg.role == "user" else "",
                "response": msg.content if msg.role == "assistant" else ""
            })
        memory_hint = gerar_memoria_inteligente(history)
        
        # ===============================
        # GOAL / PLANNER (CONTROLADO POR CONTEXTO)
        # ===============================
        if ctx.get("state") in ["planejamento", "objetivo"] and len(user_input.split()) > 4:
            goal_check = goal_response(username, user_input)
            if goal_check:
                return goal_check

        if ctx.get("state") == "planejamento" and intent in ["planejar", "estrategia"]:
            plan_check = planner_response(username)
            if plan_check:
                return plan_check

        if ctx.get("intent") == "progresso":
            progress = get_progress(username)
            if progress:
                return progress

        if ctx.get("intent") == "conclusao":
            return advance_progress(username)
        # ===============================
        # DETECÇÕES
        # ===============================
        topic = detect_topic(user_input)

        # =================================
        # DETECÇÃO DE INTENÇÃO (COM PROTEÇÃO)
        # =================================
        if not ctx.get("intent"):
            if len(user_input.split()) < 3:
                intent = detect_intent(user_input)
            else:
                intent = detect_intent_llm(user_input)

            # fallback de segurança
            if not intent:
                intent = detect_intent(user_input)
        # =================================
        # RESPOSTA DIRETA PARA TEMPO (CORRETO)
        # =================================
        if intent == "hora":
            return f"Agora são {self.get_time_brasilia()}"

        if intent == "data":
            return f"Hoje é {self.get_date_brasilia()}"
        
        if len(user_input.split()) <= 2 and intent == "conversa":
            intent = "resposta"

        main_topic = detect_main_topic(history)
        if main_topic and topic == "geral":
            topic = main_topic

        _, emotional_value = detect_emotional_intensity(user_input)

        try:
            semantic_state = detect_semantic_state(user_input)
        except:
            semantic_state = None

        active_episode = memory.get_active_episode(username)

        continuity = detect_continuity(username, topic, intent)

        # ===============================
        # COGNITIVE LOOP
        # ===============================
        cognitive_state = cognitive_loop(
            topic,
            intent,
            emotional_value,
            continuity
        )

        thought = cognitive_state.get("thought", "")

        priority = calculate_priority(intent, emotional_value, active_episode)

        focus_context = determine_focus(
            topic,
            emotional_value,
            intent,
            active_episode
        )

        # ===============================
        # IDENTIDADE
        # ===============================
        try:
            cognitive_identity = memory.detect_cognitive_identity(username, intent, topic)
        except:
            cognitive_identity = "mentor_equilibrado"

        # ===============================
        # CONTINUAÇÃO AUTOMÁTICA
        # ===============================
        pending_question = detect_pending_question(history)
        continuation = continue_conversation(pending_question, user_input)

        if continuation:
            response = continuation
        else:
            response = None

        # ===============================
        # PERFIL
        # ===============================
        profile = get_user_profile(username)

        if profile and profile.nome:
            nome_real = profile.nome
        else:
            nome_real = username

        mode = "normal"

        if active_episode:
            priority = "alta"

        # ===============================
        # MEMÓRIA
        # ===============================
        memory.update_user_state(
            username,
            topic,
            mode,
            emotional_value,
            intent
        )

        try:
            save_episode(username, topic, emotional_value, intent, user_input)
        except:
            pass

        relational_context = build_relational_context(username)
        behavior_pattern = detect_behavior_pattern(username)
        conversation_context = ""

        if history:
            mensagens = []

            for h in history:
                if isinstance(h, dict):
                    msg = h.get("input", "")
                    if msg:
                        mensagens.append(msg)

            conversation_context = " ".join(mensagens[-10:])
        
        print("ANTES:", response)
        
        if not response or not str(response).strip():
            response = build_response(
                user_input=user_input,
                username=username,
                response=None,
                mode=mode,
                topic=topic,
                nome_real=nome_real,
                emotional_score=emotional_value,
                history=history,
                priority=priority,
                intent=intent,
                cognitive_identity=cognitive_identity,
                relational_context=relational_context,
                behavior_pattern=behavior_pattern,
                thought=thought,
                self_reference=is_about_orion,
                memory_hint=memory_hint,
                conversation_context=conversation_context  # 🔥 NOVO
            )
       
        # =================================
        # 🔥 FALLBACK FINAL (OBRIGATÓRIO)
        # =================================
        if not response or not response.strip():
            response = "Hmm, não consegui responder agora."
        # =================================
        # 🧠 FILTRO DE MEMÓRIA (ANTES DE SALVAR)
        # =================================

        bloquear_memoria = False

        # 🔹 não salvar fallback
        if response and any(frase in response.lower() for frase in [
           "tô contigo",
           "explica melhor",
           "não peguei",
           "continua aí",
           "quase entendi"
        ]):
           bloquear_memoria = True

        # 🔹 não salvar resposta muito curta
        if response and len(response.strip()) < 20:
           bloquear_memoria = True

        # 🔹 não salvar mensagens muito vagas do usuário
        if user_input and len(user_input.strip()) < 5:
           bloquear_memoria = True


        # ===============================
        # 💾 SALVAR MEMÓRIA (AGORA SIM FUNCIONA)
        # ===============================

        if response and not bloquear_memoria:
            try:
                db.add(Message(username=username, role="user", content=user_input))
                db.add(Message(username=username, role="assistant", content=response))
                db.commit()
            except Exception as e:
                print("Erro ao salvar memória:", e)
        return response
    # ===============================
    # UTILITÁRIOS (FORA DO PROCESS)
    # ===============================

    def get_time_brasilia(self):
        from datetime import datetime
        from zoneinfo import ZoneInfo
        now = datetime.now(ZoneInfo("America/Sao_Paulo"))
        return now.strftime("%H:%M")

    def get_date_brasilia(self):
        from datetime import datetime
        from zoneinfo import ZoneInfo
        now = datetime.now(ZoneInfo("America/Sao_Paulo"))
        return now.strftime("%d de %B de %Y")
