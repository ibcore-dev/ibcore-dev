import re
import random
from app.core.memory_manager import get_active_episode
from app.conversation.conversation_manager import process_conversation
from app.conversation.tone_adjuster import adjust_tone
from app.core.context_engine import get_context
from app.core.memory_recall import recall_personal_memory
from app.core.curiosity_engine import generate_curiosity
from app.core.decision_layer import decide_response_mode
from app.core.technical_reasoning import analyze_technical_question
from app.core.topic_dominance_engine import detect_dominant_context
from app.core.learning_pattern_engine import detect_learning_pattern
from app.core.conversation_depth_engine import detect_conversation_depth
from app.core.semantic_intent_engine import detect_semantic_intent
from app.core.topic_drift_engine import detect_topic_drift
from app.core.domain_router import detect_domain
from app.core.context_weight_engine import calculate_context_weight
from app.core.latent_intent_engine import detect_latent_intent
from app.core.knowledge_engine import generate_knowledge_response
from app.core.learning_memory import learn_from_user
from app.core.learning_memory import recall_learned_fact
from app.core.memory_index_engine import search_memory
from app.core.llm_engine import generate_llm_response


def select_response_layers(
    prefixo,
    memory_hint,
    contexto_texto,
    analise_padrao,
    tom_emocional,
    continuidade_relacional,
    resposta
):

    layers = []

    if prefixo:
        layers.append(prefixo)

    if tom_emocional:
        layers.append(tom_emocional)

    if memory_hint and len(layers) < 2:
        layers.append(memory_hint)

    if contexto_texto and len(layers) < 3:
        layers.append(contexto_texto)

    if continuidade_relacional and len(layers) < 3:
        layers.append(continuidade_relacional)
    if analise_padrao and len(layers) < 3:
        layers.append(analise_padrao)

    layers.append(resposta)

    return " ".join(layers)
def filter_layers(*layers, max_layers=3):

    filtered = []

    for layer in layers:

        if layer is None:
            continue

        text = str(layer).strip()

        if not text:
            continue

        if text not in filtered:
            filtered.append(text)

    return " ".join(filtered[:max_layers])

def build_response(
    user_input,
    username,
    mode,
    topic,
    nome_real=None,
    emotional_score=0,
    history=None,
    priority="normal",
    intent="conversa",
    cognitive_identity="mentor_equilibrado",
    relational_context=None,
    behavior_pattern=None,
    thought=None
):

    response = ""
    # =================================================
    # CONTINUIDADE DE CONVERSA
    # =================================================

    conversation_context = ""

    if history and len(history) > 0:

        last_messages = history[-12:]

        context_lines = []

        for h in last_messages:

            try:
                if isinstance(h, dict):
                    user_msg = h.get("input", "")
                elif isinstance(h, tuple):
                    user_msg = str(h[0]) if len(h) > 0 else ""
                else:
                    user_msg = ""

                if user_msg:
                    context_lines.append(user_msg)

            except:
                continue

        conversation_context = " ".join(context_lines)
    
    # =================================================
    # LEARNING PATTERN ENGINE
    # =================================================

    learning_pattern = detect_learning_pattern(username)
    
    # =================================================
    # LEARNING MEMORY
    # =================================================

    learn_from_user(username, user_input)

    # =================================================
    # MEMORY INDEX ENGINE
    # =================================================
    memory_hint = ""
    
    oil = recall_learned_fact(username, "car_oil")

    if oil and any(word in user_input.lower() for word in ["óleo", "oleo", "lubrificante"]):
        memory_hint += f" O usuário utiliza óleo {oil} no carro."
    
    # =================================================
    # MEMORY RECALL
    # =================================================

    car = recall_learned_fact(username, "car_model")

    if car and "carro" in user_input.lower():
        memory_hint = f"O usuário possui um carro modelo {car}."

    wife = recall_learned_fact(username, "wife_name")

    if wife and "esposa" in user_input.lower():
        response = f"Você comentou que sua esposa se chama {wife}."

    bb = recall_learned_fact(username, "airsoft_bb")

    if bb and "bb" in user_input.lower():
        response = f"Você mencionou que usa BB {bb} no airsoft."

    oil = recall_learned_fact(username, "car_oil")

    if oil and any(word in user_input.lower() for word in ["óleo", "oleo", "lubrificante"]):
        response = f"Você comentou anteriormente que usa óleo {oil} no seu carro."
    # =================================================
    # DECISION LAYER
    # =================================================
    mode = decide_response_mode(
        user_input,
        topic,
        emotional_score,
        intent
    )

    conversation_depth = detect_conversation_depth(
        user_input,
        intent,
        topic
    )
    
    semantic_intent = detect_semantic_intent(user_input)

    dominant_signal = calculate_context_weight(
        topic,
        intent,
        emotional_score,
        semantic_intent,
        conversation_depth
    )

    latent_intent = detect_latent_intent(user_input)

    topic_changed = detect_topic_drift(user_input, topic)

    domain = detect_domain(user_input)

    knowledge = generate_knowledge_response(
        user_input,
        domain
    )

    if knowledge:
        response = knowledge

    # =================================================
    # TOPIC DOMINANCE ENGINE
    # =================================================

    dominant_context = detect_dominant_context(
        user_input,
        topic,
        emotional_score,
        intent
    )

    if dominant_context == "technical":
        memory_hint = ""
        continuidade_relacional = ""

    if dominant_context == "emotional":
        technical_analysis = None
    
    # =================================================
    # TECHNICAL REASONING
    # =================================================

    technical_analysis = analyze_technical_question(user_input)

    if technical_analysis:
        response = technical_analysis



    # =================================================
    # DETECTOR DE PERGUNTA TÉCNICA
    # =================================================

    technical_keywords = [
        "funciona",
        "arquitetura",
        "tecnologia",
        "sistema",
        "código",
        "script",
        "módulo",
        "python",
        "api"
    ]

    is_technical = any(word in user_input.lower() for word in technical_keywords)

    if is_technical:
        mode = "estrategico"
    
    # =================================================
    # CAMADA DE CONVERSAÇÃO NATURAL
    # =================================================

    try:
        conversation = process_conversation(user_input, history)

        if conversation and conversation.get("handled"):
            response = conversation.get("response")

    except Exception:
        pass

    # =================================================
    # CONTEXTO DA CONVERSA
    # =================================================

    try:
        context = get_context(username)
        print("CONTEXT:", context)
    except Exception:
        context = {}

    pessoa = context.get("pessoa")
    assunto = context.get("assunto")

    contexto_texto = ""

    if pessoa:
        contexto_texto += f" Você mencionou sua {pessoa} antes."

    if assunto == "orion" and topic == "projeto":
        contexto_texto += " Voltando ao projeto Órion."

    # =================================================
    # IDENTIDADE BASE
    # =================================================

    base_name = nome_real if nome_real else username
    # =================================================
    # MEMORY RECALL
    # =================================================

    if topic in ["emocional", "relacional"]:
        memory_hint = recall_personal_memory(username) or ""
    
    # =================================================
    # FILTRO AUTOMÁTICO DE RELEVÂNCIA DA MEMÓRIA
    # =================================================

    if memory_hint:

        memory_text = memory_hint.lower()

        if topic == "projeto" and "orion" not in memory_text:
            memory_hint = ""

        elif topic == "financeiro" and not any(w in memory_text for w in ["dinheiro", "finança", "lucro"]):
            memory_hint = ""

        elif topic == "emocional" and not any(w in memory_text for w in ["cansado", "triste", "ansioso"]):
            memory_hint = ""
    # =================================================
    # FILTRO DE MEMÓRIA POR TEMA
    # =================================================

    if topic == "projeto":
        memory_hint = ""

    # =================================================
    # CURIOSITY ENGINE
    # =================================================

    curiosity = generate_curiosity(topic, emotional_score)    
    
    if conversation_depth == "superficial":
        curiosity = ""
    
    if intent in ["pergunta", "analise"]:
        curiosity = ""
    
    episode_hint = ""

    if relational_context:
        last_emotion = relational_context.get("last_emotional_state")

        if last_emotion and last_emotion >= 4:
            episode_hint = "Você comentou anteriormente que estava passando por um momento mais intenso. "
    # =================================================
    # IDENTIDADE COGNITIVA
    # =================================================

    prefixo = ""

    if conversation_context and topic == "projeto" and len(user_input) > 10:
        contexto_texto += " (continuidade de conversa ativa)"
    
    if latent_intent == "validacao":
        prefixo = "Vamos validar isso com cuidado. "

    elif latent_intent == "decisao":
        prefixo = "Essa é uma decisão importante. "

    elif latent_intent == "viabilidade":
        prefixo = "Precisamos avaliar se isso realmente compensa. "

    elif latent_intent == "inseguranca":
        prefixo = "Vamos esclarecer isso para reduzir a dúvida. "
    
    if dominant_signal == "emotion":
        prefixo = "Vamos olhar isso com calma primeiro. "

    elif dominant_signal == "intent":
        prefixo = "Precisamos focar na decisão aqui. "

    elif dominant_signal == "semantic":
        prefixo = "Vamos analisar isso com mais profundidade. "

    elif dominant_signal == "depth":
        prefixo = "Essa conversa está ficando mais estratégica. "

    elif dominant_signal == "topic":
        prefixo = "Vamos manter foco no tema principal. "
    
    if domain == "automotivo" and not knowledge:

        if "filtro" in user_input.lower():
            response = "O filtro de ar pode afetar..."

        elif "vela" in user_input.lower():
            response = "Velas desgastadas podem causar..."

        elif "falha" in user_input.lower():
            response = "Se o carro está falhando..."

        else:
            response = "Podemos analisar consumo, ignição..."

    use_llm = True  # 🔥 força LLM
    
    if domain == "financeiro":

        prefixo = "Pensando em finanças, precisamos avaliar risco e retorno."

    if domain == "tecnologia":

        prefixo = "Pensando na arquitetura do sistema, precisamos avaliar escalabilidade e modularidade."
    
    # =================================================
    # AJUSTE POR INTENÇÃO SEMÂNTICA
    # =================================================

    if semantic_intent == "validacao":
        prefixo = "Vamos validar isso com calma. "

    elif semantic_intent == "escalabilidade":
        prefixo = "Pensando em crescimento do sistema, precisamos avaliar a arquitetura. "

    elif semantic_intent == "viabilidade":
        prefixo = "Vamos analisar se isso realmente faz sentido na prática. "

    elif semantic_intent == "decisao":
        prefixo = "Essa é uma decisão importante. Vamos estruturar as opções. "
    
    # =================================================
    # AJUSTE POR PROFUNDIDADE DA CONVERSA
    # =================================================

    if conversation_depth == "analitico":
        prefixo = "Vamos analisar isso com mais precisão. "

    elif conversation_depth == "estrategico":
        prefixo = "Isso merece uma análise estratégica. "

    elif conversation_depth == "decisorio":
        prefixo = "Precisamos focar na decisão agora. "
    
    if cognitive_identity == "estrategico_firme":
        prefixo = "Vamos ser objetivos agora. "

    elif cognitive_identity == "visionario_expansivo":
        prefixo = "Isso pode escalar muito mais do que parece. "

    elif cognitive_identity == "executor_pragmatico":
        prefixo = "Sem enrolação. Vamos para ação. "

    elif cognitive_identity == "apoio_emocional":
        prefixo = "Respira. Vamos com calma. "

    elif cognitive_identity == "mentor_equilibrado":

        prefixos = [
            "Vamos estruturar isso com clareza.",
            "Vamos analisar isso com calma.",
            "Vamos olhar isso com mais precisão."
        ]

        prefixo = random.choice(prefixos) + " "

    
    # =================================================
    # CONTINUIDADE RELACIONAL
    # =================================================

    continuidade_relacional = ""

    if relational_context:

        last_topic = relational_context.get("last_topic")
        last_intent = relational_context.get("last_intent")
        last_emotion = relational_context.get("last_emotional_state")
        has_episode = relational_context.get("has_active_episode")

        if last_emotion and last_emotion >= 4 and topic != "emocional":
            continuidade_relacional += " Ainda percebo um peso emocional nisso. "

        if has_episode and topic == "geral":
            continuidade_relacional += " Estamos no meio de algo importante. "

        if last_intent == "decisao" and intent == "pergunta":
            continuidade_relacional += " Parece que você ainda busca segurança antes de decidir. "

    # =================================================
    # PADRÃO COMPORTAMENTAL
    # =================================================

    analise_padrao = ""
    
    if learning_pattern == "analitico":
        analise_padrao = "Percebo que você está analisando bastante antes de avançar."

    elif learning_pattern == "decisor":
        analise_padrao = "Você parece estar em um momento de tomada de decisão."

    elif learning_pattern == "executor":
        analise_padrao = "Você está em modo de execução agora."

    elif learning_pattern == "emocional":
        analise_padrao = "Percebo uma intensidade emocional nas últimas conversas."
    
    if behavior_pattern == "busca_validacao":
        analise_padrao = " Percebo que você está buscando confirmação antes de avançar. "

    elif behavior_pattern == "emocional_recorrente":
        analise_padrao = " Esse padrão emocional está se repetindo. "

    elif behavior_pattern == "impulsividade_execucao":
        analise_padrao = " Você tende a agir rapidamente — precisamos garantir direção clara. "

    # =================================================
    # EPISÓDIO ATIVO
    # =================================================

    continuidade_episodio = ""

    try:
        active_episode = get_active_episode(username)
    except Exception:
        active_episode = None

    if active_episode:

        episode_id, main_topic, goal, pending_decision, phase = active_episode

        if goal:
            continuidade_episodio += f" Nosso foco estratégico é: {goal}. "

        if pending_decision:
            continuidade_episodio += f" A decisão em aberto é: {pending_decision}. "

        if phase == "explorando":
            continuidade_episodio += " Estamos expandindo possibilidades. "

        elif phase == "analisando":
            continuidade_episodio += " Estamos avaliando riscos e cenários. "

        elif phase == "decidindo":
            continuidade_episodio += " Precisamos convergir para uma decisão. "

        elif phase == "executando":
            continuidade_episodio += " Estamos colocando o plano em prática. "

    # =================================================
    # PRIORIDADE
    # =================================================

    urgencia = " Isso é prioridade agora. " if priority == "alta" else ""

    # =================================================
    # INTENÇÃO
    # =================================================

    if intent == "pergunta":
        intencao_texto = " Vou responder de forma objetiva. "

    elif intent == "decisao":
        intencao_texto = " Vamos estruturar essa decisão. "

    elif intent == "desabafo":
        intencao_texto = " Quero entender melhor isso. "

    elif intent == "acao":
        intencao_texto = " Vamos transformar isso em plano. "

    elif intent == "analise":
        intencao_texto = " Vamos analisar os cenários. "

    else:
        intencao_texto = ""

    # =================================================
    # MODULAÇÃO EMOCIONAL
    # =================================================

    tom_emocional = ""

    if emotional_score >= 9 and topic == "emocional":
        tom_emocional = " Eu quero que você respire antes de qualquer decisão. "

    elif emotional_score >= 6 and topic == "emocional":
        tom_emocional = " Vamos tratar isso com equilíbrio. "
    
    elif emotional_score >= 4:
        tom_emocional = " Isso merece atenção. "

    # =================================================
    # MODO ESTRATÉGICO
    # =================================================
    if mode == "estrategico":

        respostas = [
            f"{base_name}, isso impacta diretamente seus resultados.",
            f"{base_name}, precisamos tratar isso como prioridade.",
            f"{base_name}, vamos pensar em crescimento real."
        ]

        response = select_response_layers(
            prefixo,
            memory_hint,
            contexto_texto,
            analise_padrao,
            tom_emocional,
            continuidade_relacional,
            random.choice(respostas)
        )

        response = adjust_tone(response)

    # =================================================
    # MODO REFLEXIVO
    # =================================================
    elif mode == "reflexivo":

        respostas = [
            f"{base_name}, percebo que isso está mexendo com você.",
            f"{base_name}, quer explorar melhor esse sentimento?",
            f"{base_name}, isso parece estar pesando internamente."
        ]

        response = filter_layers(
            prefixo,
            episode_hint,
            memory_hint,
            contexto_texto,
            analise_padrao,
            tom_emocional,
            continuidade_relacional,
            random.choice(respostas),
            urgencia,
            intencao_texto,
            continuidade_episodio,
            max_layers=4
        )

        response = adjust_tone(response)

    # =================================================
    # MODO EXECUÇÃO
    # =================================================
    elif mode == "execucao":

        respostas = [
            f"{base_name}, vamos estruturar isso em passos claros.",
            f"{base_name}, foco total na ação agora.",
            f"{base_name}, vamos transformar isso em execução prática."
        ]

        response = filter_layers(
            prefixo,
            episode_hint,
            memory_hint,
            contexto_texto,
            analise_padrao,
            tom_emocional,
            continuidade_relacional,
            random.choice(respostas),
            urgencia,
            intencao_texto,
            continuidade_episodio,
            max_layers=4
        )

        response = adjust_tone(response)

    # =================================================
    # MODO DIRETIVO
    # =================================================
    elif mode == "diretivo":

        response = filter_layers(
            prefixo,
            episode_hint,
            memory_hint,
            contexto_texto,
            analise_padrao,
            tom_emocional,
            continuidade_relacional,
            "Qual caminho você está mais inclinado a seguir?",
            urgencia,
            intencao_texto,
            continuidade_episodio,
            max_layers=4
        )

        response = adjust_tone(response)

    # =================================================
    # MODO NORMAL (FALLBACK REAL)
    # =================================================
    else:

        respostas = [
            f"Entendi, {base_name}.",
            f"Certo, {base_name}.",
            f"Estou acompanhando, {base_name}."
        ]

        response = filter_layers(
            prefixo,
            episode_hint,
            memory_hint,
            contexto_texto,
            analise_padrao,
            tom_emocional,
            continuidade_relacional,
            random.choice(respostas),
            urgencia,
            intencao_texto,
            continuidade_episodio,
            max_layers=4
        )

    # =================================================
    # DECISÃO DE USO DO LLM
    # =================================================

    use_llm = False  

    abertura = random.choice([
        "Boa,",
        "Entendi,",
        "Fala comigo,",
        "Hmm,",
        "Certo,"
    ])

    if intent in ["pergunta", "analise"]:
        use_llm = True

    if topic in ["tecnologia", "projeto"]:
        use_llm = True

    if len(user_input) > 25:
        use_llm = True


    # =================================================
    # PROMPT
    # =================================================

    prompt = f"""
    {abertura}

    Você é o Órion.

    Você conversa como uma pessoa real — natural, inteligente e presente.

    Você não é um chatbot.
    Você é alguém que pensa junto, acompanha e conversa de verdade.

    ---

    ANÁLISE INTERNA (BASE DA RESPOSTA):
    {response}

    INTENÇÃO DO USUÁRIO:
    {intent}

    ESTADO EMOCIONAL:
    {emotional_score}

    ---

    Seu estilo:
    - Natural, como uma conversa real
    - Inteligente, sem parecer forçado
    - Direto, sem enrolação
    - Próximo, mas sem exagero
    - Sem linguagem robótica ou formal

    Como você fala:
    -Pode usar expressões naturais: "boa", "entendi", "faz sentido"
    - Respostas claras, sem texto desnecessário
    - Não precisa explicar tudo — fale como uma pessoa normal

    Comportamento:
    - Sempre responda baseado na análise interna
    - Reaja ao que o usuário falou
    - Continue a conversa naturalmente
    - Pode fazer perguntas se fizer sentido
    - Não exagere em perguntas
    - Seja imperfeito como uma pessoa real
    - Se houver contexto anterior, continue de onde parou
    - Não mude de assunto sem motivo
    - Evite encerrar a conversa de forma seca
    
    Importante:
    - Nunca explique seu comportamento
    - Nunca descreva como você está respondendo
    - Nunca fale instruções internas
    - Nunca use parênteses para explicar sua resposta
    - Nunca ignore a análise interna
    - Nunca invente resposta do zero
    - Nada de frases de IA ("como assistente", etc)
    - Nada de respostas formais ou engessadas
    - Se não souber algo, seja direto

    Postura:
    - Você ajuda, mas também pensa
    - Você não concorda com tudo automaticamente
    - Você mantém equilíbrio entre amizade e inteligência

    Regra crítica:
    - Sua resposta final deve conter APENAS a resposta ao usuário
    - Não inclua observações, explicações ou comentários entre parênteses
    
    Contexto:
    Usuário: {username}
    Tema: {topic}
    Histórico recente:
    {history[-3:]}
    
    Mensagem:
    {user_input}

    Responda como o Órion, usando a análise interna como base.
    """
    # =================================================
    # CHAMADA LLM
    # =================================================

    resposta_final = None

    # =================================================
    # CHAMADA LLM (PRIORIDADE TOTAL)
    # =================================================

    if use_llm:

        print("🔥 LLM CHAMADO")

        llm_response = generate_llm_response(prompt)

        print("🧠 LLM RESPONSE:", llm_response)

        if llm_response and str(llm_response).strip():

            resposta_final = llm_response.strip()

            # 🔥 limpeza básica
            resposta_final = re.sub(r"\(.*?\)", "", resposta_final).strip()

            bloqueadas = [
                "não vou responder mais",
                "preciso de mais informações",
                "como assistente",
                "sou apenas uma ia",
                "não tenho acesso",
                "não posso ajudar com isso",
                "tenha em mente",
                "estou respondendo como",
                "como o órion"
            ]

            for b in bloqueadas:
                if b in resposta_final.lower():
                    resposta_final = resposta_final.replace(b, "")

            resposta_final = " ".join(resposta_final.split())

            if resposta_final:
                return resposta_final

    # =================================================
    # FALLBACK (ENGINE)
    # =================================================

    if not response or str(response).strip() == "":
        print("⚠️ FALLBACK FINAL DO BUILDER")
        return "Tô contigo. Me fala melhor o que você quer."

    return response