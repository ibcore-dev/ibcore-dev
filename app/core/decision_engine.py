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
from app.core.intent_engine import detect_intent_llm

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

    text = (text or "").lower()

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

    if any(frase in text for frase in [
        "como faço",
        "como eu faço",
        "qual é",
        "me explica",
        "quero saber",
        "me fala"
    ]):
        return "pergunta"

    if any(word in text for word in ["como", "qual", "quando", "onde", "por que"]):
        return "pergunta"

    if any(word in text for word in ["preciso fazer", "vou fazer", "executar"]):
        return "acao"

    if any(word in text for word in ["analisar", "avaliar", "risco"]):
        return "analise"

    return "conversa"

def detect_time_intent(text: str):

    text = text.lower()

    padrões = [
        "que horas são",
        "me fala a hora",
        "qual a hora",
        "que dia é hoje",
        "data de hoje",
        "me fala a data"
    ]

    return any(p in text for p in padrões)

def should_answer_time(context, topic, intent):

    # NÃO responder se estiver em conversa ativa
    if topic in ["projeto", "negocio", "emocional"]:
        return False

    if intent in ["decisao", "analise"]:
        return False

    return True

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

        text = (user_input or "").lower()

        # =================================
        # CONTROLE DE TEMPO (NOVO)
        # =================================
        if detect_time_intent(user_input):
            if should_answer_time({}, detect_topic(user_input), detect_intent(user_input)):
                return f"Agora são {self.get_time_brasilia()}"

        # ===============================
        # SAFE INIT
        # ===============================
        history = []
        response = ""
        thought = ""

        # ===============================
        # GOAL / PLANNER
        # ===============================
        goal_check = goal_response(username, user_input)
        if goal_check:
            return goal_check

        text = user_input.lower()

        if "plano" in text or "como fazer" in text:
            plan_check = planner_response(username)
            if plan_check:
                return plan_check

        if "próximo passo" in text or "proximo passo" in text:
            progress = get_progress(username)
            if progress:
                return progress

        if "concluí" in text or "finalizei" in text:
            return advance_progress(username)

        # ===============================
        # CONTEXTO
        # ===============================
        try:
            update_context(username, user_input)
        except:
            pass

        # ===============================
        # DETECÇÕES
        # ===============================
        topic = detect_topic(user_input)

        # =================================
        # DETECÇÃO DE INTENÇÃO (COM PROTEÇÃO)
        # =================================
        if len(user_input.split()) < 3:
            intent = detect_intent(user_input)
        else:
            intent = detect_intent_llm(user_input)

            # fallback de segurança
            if not intent:
                intent = detect_intent(user_input)

        if len(user_input.split()) <= 2 and intent == "conversa":
            intent = "resposta"

        history = memory.get_last_messages(username, 50) or []

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
            return continuation

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

        # ===============================
        # BUILD RESPONSE
        # ===============================
        response = build_response(
            user_input=user_input,
            username=username,
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
            thought=thought
        )

        if not response:
            response = "Entendi. Pode me explicar melhor?"

        try:
            memory.save_memory(username, user_input, response, topic)
        except:
            pass

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