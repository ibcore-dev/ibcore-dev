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

    if any(word in text for word in [
        "acho que", "estou pensando", "quero decidir",
        "preciso decidir", "tenho que decidir", "devo decidir"
    ]):
        return "decisao"

    if any(word in text for word in ["como", "qual", "quando", "onde", "por que"]):
        return "pergunta"

    if any(word in text for word in ["preciso fazer", "vou fazer", "executar"]):
        return "acao"

    if any(word in text for word in ["analisar", "avaliar", "risco"]):
        return "analise"

    return "conversa"


# =================================================
# ENGINE PRINCIPAL
# =================================================

class DecisionEngine:

    def process(self, username: str, user_input: str):
        nome = memory.get_profile(username, "nome")

        if not nome:
            nome = username  # fallback
        
        if not username:
            raise ValueError("Username não pode ser vazio")

        user_input = user_input or ""
        # =================================================
        # SAFE VARIABLES (ANTI-CRASH)
        # =================================================

        history = []
        main_topic = None

        goal_check = goal_response(username, user_input)

        if goal_check:
            return goal_check

        text = user_input.lower()

        if "plano" in text or "como fazer" in text:

            plan_check = planner_response(username)

            if plan_check:
                return plan_check
        # =====================================
        # PROGRESS ENGINE
        # =====================================

        if "próximo passo" in text or "proximo passo" in text:

            progress = get_progress(username)

            if progress:
                return progress

        if "concluí" in text or "finalizei" in text:

            return advance_progress(username)
        
        response = ""

        thought = ""

        # =================================================
        # EXTRAÇÃO DE CONHECIMENTO
        # =================================================

        try:
            extract_user_knowledge(username, user_input)
        except Exception:
            pass

        # =================================================
        # CONTEXT ENGINE
        # =================================================

        try:
            update_context(username, user_input)
            conversation_context = get_context(username)
        except Exception:
            conversation_context = {}

        # =================================================
        # DETECÇÕES PRINCIPAIS
        # =================================================

        topic = detect_topic(user_input)
        intent = detect_intent(user_input)

        if len(user_input.split()) <= 2 and intent == "conversa":
            intent = "resposta"
        
        # =================================================
        # HISTORY + MAIN TOPIC
        # =================================================
        history = memory.get_last_messages(username, 25) or []

        main_topic = detect_main_topic(history)

        if main_topic and topic == "geral":
            topic = main_topic
        
        # detectar emoção primeiro
        _, emotional_value = detect_emotional_intensity(user_input)

        # semantic state
        try:
            semantic_state = detect_semantic_state(user_input)
        except Exception:
            semantic_state = None

        active_episode = memory.get_active_episode(username)

        # CONTINUITY ENGINE
        continuity = detect_continuity(username, topic, intent)
        # =================================================
        # COGNITIVE LOOP
        # =================================================

        cognitive_state = cognitive_loop(
            topic,
            intent,
            emotional_value,
            continuity
        )

        thought = cognitive_state["thought"]
        reflection = cognitive_state["reflection"]
        meta_analysis = cognitive_state["meta"] 
        
        # PRIORITY ENGINE
        priority = calculate_priority(intent, emotional_value, active_episode)
        focus_context = determine_focus(
            topic,
            emotional_value,
            intent,
            active_episode
        )
        
        # =================================================
        # IDENTIDADE COGNITIVA BASE
        # =================================================

        try:
            cognitive_identity = memory.detect_cognitive_identity(username, intent, topic)
        except Exception:
            cognitive_identity = "mentor_equilibrado"
        try:
            current_style = memory.detect_user_style(username)
            memory.save_profile(username, "personality", current_style)
        except Exception:
            current_style = None

        history = memory.get_last_messages(username, 25) or []

        # =================================================
        # DIALOGUE MEMORY ENGINE
        # =================================================

        main_topic = detect_main_topic(history)

        already_asked = conversation_already_answered(history, user_input)

        if already_asked:
            thought = "Já falamos sobre isso, mas vamos aprofundar."
        
        # =================================================
        # CONVERSATION INTELLIGENCE ENGINE
        # =================================================

        pending_question = detect_pending_question(history)

        continuation = continue_conversation(pending_question, user_input)

        if continuation:
            return continuation
        # =================================================
        # CONVERSATION GOAL ENGINE
        # =================================================

        goal = detect_goal(history)

        profile = get_user_profile(username)

        if profile and profile.nome:
           nome_real = profile.nome
        else:
            nome_real = username
        
        mode = "normal"
        # priority já definido pelo priority_engine

        active_episode = memory.get_active_episode(username)

        if active_episode:
            priority = "alta"
        
        # =================================================
        # SELF EVOLUTION
        # =================================================

        try:
            learn_from_conversation(username, user_input)
        except Exception:
            pass

        
        # =================================================
        # ATTENTION ENGINE
        # =================================================

        dominant_context, attention_weights = calculate_attention(
            topic=topic,
            intent=intent,
            emotional_score=emotional_value,
            active_episode=active_episode,
            semantic_state=semantic_state
        )
        
        # =================================================
        # AJUSTE SEMÂNTICO
        # =================================================

        if semantic_state == "fadiga":
            emotional_value = max(emotional_value or 0, 5)

        elif semantic_state == "ansiedade":
            emotional_value = max(emotional_value or 0, 7)

        elif semantic_state == "duvida":
            intent = intent or "analise"

        if dominant_context == "emocional":
            mode = "reflexivo"

        elif dominant_context == "execucao":
            mode = "execucao"

        elif dominant_context == "decisao":
            mode = "diretivo"

        elif dominant_context == "episodio":
            mode = "estrategico"

        # =================================================
        # MEMÓRIA
        # =================================================

        memory.update_user_state(
            username,
            topic,
            mode,
            emotional_value,
            intent
        )
        try:
            save_episode(username, topic, emotional_value, intent, user_input)
        except Exception:
            pass
        relational_context = build_relational_context(username)

        behavior_pattern = detect_behavior_pattern(username)
        learning_pattern = detect_learning_pattern(username)
        if not cognitive_identity:
            cognitive_identity = "mentor_equilibrado"
        cognitive_identity = adapt_cognitive_identity(
            cognitive_identity,
            behavior_pattern
        )
        if learning_pattern == "analitico":
            cognitive_identity = "mentor_equilibrado"

        elif learning_pattern == "executor":
            cognitive_identity = "executor_pragmatico"

        elif learning_pattern == "decisor":
            cognitive_identity = "estrategico_firme"

        elif learning_pattern == "emocional":
            cognitive_identity = "apoio_emocional"
        
        # =================================================
        # GERAR RESPOSTA
        # =================================================
        
        episode = recall_episode(username)

        tech_response = check_technical_memory(username, user_input)

        if tech_response:
            return tech_response

        # =================================================
        # TECHNICAL MEMORY RECALL
        # =================================================

        peso = None
        # =================================================
        # MEMORY RECALL TRIGGER
        # =================================================

        memory_hint = ""

        try:
            previous_state = memory.get_user_state(username)
        except:
            previous_state = None

        last_topic = None

        if previous_state:
            last_topic = previous_state[0]

        if last_topic == topic and topic != "geral":
            memory_hint = "Você mencionou isso anteriormente."

        elif last_topic and topic == "projeto":
            memory_hint = "Na última conversa você comentou sobre isso."
        if memory_hint:
            thought = (memory_hint + " " + (thought or "")).strip()
        
        # =================================================
        # TECHNICAL MEMORY RECALL
        # =================================================

        peso = memory.get_profile(username, "spec_peso")

        if peso and "peso" in user_input.lower():

            response = f"O peso do drone está definido como {peso}."

            try:
                memory.save_memory(username, user_input, response, topic)
            except Exception:
                pass

            return response
        
        # =================================================
        # CONTEXT FOCUS ENGINE
        # =================================================

        if focus_context == "emocional":
            thought = "Vamos focar primeiro no que você está sentindo."

        elif focus_context == "execucao":
            thought = "Vamos transformar isso em ação prática."

        elif focus_context == "episodio":
            thought = "Esse assunto parece importante na sua jornada."

        elif focus_context == "projeto":
            thought = "Vamos analisar o projeto com clareza."

        elif focus_context == "financeiro":
            thought = "Vamos olhar isso com visão estratégica."
       
        # =================================================
        # INTELIGÊNCIA CONTEXTUAL
        # =================================================

        if not thought:

            if topic == "projeto" and intent == "pergunta":
                thought = "Vamos analisar o projeto com clareza."

            elif topic == "projeto" and intent == "decisao":
                thought = "Essa decisão pode impactar o desenvolvimento do sistema."

            elif topic == "emocional":
                thought = "O foco agora deve ser o equilíbrio emocional."

            elif intent == "analise":
                thought = "Vamos analisar os cenários possíveis."
        
        # =================================================
        # STRATEGIC QUESTION ENGINE
        # =================================================

        strategic_question = ""

        if intent == "pergunta" and topic in ["projeto", "negocio", "financeiro"]:
            thought += " Vamos estruturar isso com clareza."
            strategic_question = " Qual parte disso você considera mais crítica agora?"

        elif intent == "analise":
            strategic_question = " Quais cenários você acredita que precisam ser analisados primeiro?"

        elif intent == "decisao":
            strategic_question = " Qual fator pesa mais nessa decisão agora?"

        elif topic == "negocio":
            strategic_question = " Qual resultado você espera alcançar com isso?"
    
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

        # garantir resposta mínima
        if not response:
            response = "Entendi. Pode me explicar um pouco mais sobre isso?"

        # adicionar pergunta estratégica
        if strategic_question:
            response = response + strategic_question

        # salvar memória
        try:
            memory.save_memory(username, user_input, response, topic)
        except Exception:
            pass

        return response