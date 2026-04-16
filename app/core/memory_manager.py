print("MEMORY_MANAGER CARREGADO CORRETAMENTE")
import sqlite3
import os

# =================================================
# 🔹 CAMINHO ABSOLUTO DO BANCO
# =================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../"))


DB_PATH = os.path.join(PROJECT_ROOT, "orion.db")

print("📂 Banco em uso:", DB_PATH)


# =================================================
# 🔹 INICIALIZAÇÃO DO BANCO
# =================================================

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # =========================
    # 🧠 MEMÓRIA DO ÓRION
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        response TEXT,
        topic TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # 🧠 ESTADO DO USUÁRIO
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_state (
        username TEXT PRIMARY KEY,
        dominant_topic TEXT,
        mode TEXT,
        emotional_score INTEGER DEFAULT 0,
        dominant_intent TEXT,
        last_update DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_state_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        dominant_topic TEXT,
        mode TEXT,
        emotional_score INTEGER,
        dominant_intent TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # 🧠 EPISÓDIOS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_episode (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        main_topic TEXT,
        goal TEXT,
        pending_decision TEXT,
        phase TEXT DEFAULT 'explorando',
        status TEXT DEFAULT 'ativo',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # 🧠 PERFIL DO USUÁRIO (APRENDIZADO)
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        username TEXT,
        key TEXT,
        value TEXT,
        PRIMARY KEY (username, key)
    )
    """)

    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect(DB_PATH)


# =================================================
# 🔹 MEMÓRIA DE CURTO PRAZO
# =================================================

def save_memory(username: str, message: str, response: str, topic: str = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memory (username, message, response, topic)
        VALUES (?, ?, ?, ?)
    """, (username, message, response, topic))

    conn.commit()
    conn.close()


def get_last_messages(username: str, limit: int = 5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, response
        FROM memory
        WHERE username = ?
        ORDER BY id DESC
        LIMIT ?
    """, (username, limit))

    rows = cursor.fetchall()
    conn.close()

    return rows[::-1] if rows else []


def get_topics_summary(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic, COUNT(*) as total
        FROM memory
        WHERE username = ?
        GROUP BY topic
        ORDER BY total DESC
    """, (username,))

    rows = cursor.fetchall()
    conn.close()

    return rows if rows else []


# =================================================
# 🔹 MEMÓRIA DE LONGO PRAZO
# =================================================

def save_profile(username: str, key: str, value: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_profile (username, key, value)
        VALUES (?, ?, ?)
        ON CONFLICT(username, key)
        DO UPDATE SET value=excluded.value
    """, (username, key, value))

    conn.commit()
    conn.close()


def get_profile(username: str, key: str):
    return None
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT value
        FROM user_profile
        WHERE username = ? AND key = ?
    """, (username, key))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


def get_full_profile(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT key, value
        FROM user_profile
        WHERE username = ?
    """, (username,))

    rows = cursor.fetchall()
    conn.close()

    return rows if rows else []


# =================================================
# 🔹 ESTADO COGNITIVO
# =================================================

def update_user_state(username: str,
                      dominant_topic: str,
                      mode: str,
                      emotional_score: int,
                      dominant_intent: str):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_state (username, dominant_topic, mode, emotional_score, dominant_intent)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(username)
        DO UPDATE SET
            dominant_topic=excluded.dominant_topic,
            mode=excluded.mode,
            emotional_score=excluded.emotional_score,
            dominant_intent=excluded.dominant_intent,
            last_update=CURRENT_TIMESTAMP
    """, (username, dominant_topic, mode, emotional_score, dominant_intent))

    conn.commit()
    conn.close()


def get_user_state(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT dominant_topic, mode, emotional_score, dominant_intent
        FROM user_state
        WHERE username = ?
    """, (username,))

    row = cursor.fetchone()
    conn.close()

    return row

# =================================================
# 🔥 HISTÓRICO REAL DE ESTADOS — ORION v1.5
# =================================================

def get_user_state_history(username: str, limit: int = 7):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT dominant_topic, mode, emotional_score, dominant_intent
        FROM user_state_history
        WHERE username = ?
        ORDER BY id DESC
        LIMIT ?
    """, (username, limit))

    rows = cursor.fetchall()
    conn.close()

    return rows[::-1] if rows else []
# =================================================
# 🔥 MEMÓRIA EPISÓDICA EVOLUÍDA
# =================================================

def get_active_episode(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, main_topic, goal, pending_decision, phase
        FROM conversation_episode
        WHERE username = ? AND status = 'ativo'
        ORDER BY id DESC
        LIMIT 1
    """, (username,))

    row = cursor.fetchone()
    conn.close()

    return row


def create_episode(username: str, topic: str, goal: str = None, decision: str = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversation_episode (username, main_topic, goal, pending_decision)
        VALUES (?, ?, ?, ?)
    """, (username, topic, goal, decision))

    conn.commit()
    conn.close()


def update_episode_phase(username: str, phase: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE conversation_episode
        SET phase = ?
        WHERE username = ? AND status = 'ativo'
    """, (phase, username))

    conn.commit()
    conn.close()


def close_active_episode(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE conversation_episode
        SET status = 'encerrado'
        WHERE username = ? AND status = 'ativo'
    """, (username,))

    conn.commit()
    conn.close()


# =================================================
# 🔥 RESUMO DO EPISÓDIO (MEMÓRIA NARRATIVA)
# =================================================

def update_episode_summary(username: str, summary: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE conversation_episode
        SET goal = ?
        WHERE username = ? AND status = 'ativo'
    """, (summary, username))

    conn.commit()
    conn.close()


# =================================================
# 🔥 PERSONALIDADE ADAPTATIVA
# =================================================

def get_or_create_personality(username: str):
    personality = get_profile(username, "personality")

    if not personality:
        personality = "estrategico_visionario"
        save_profile(username, "personality", personality)

    return personality


def detect_user_style(username: str):

    topics = get_topics_summary(username) or []

    if not topics:
        return "neutro"

    dominant_topic = topics[0][0]

    if dominant_topic == "projeto":
        return "visionario"

    if dominant_topic == "financeiro":
        return "estrategico"

    if dominant_topic == "emocional":
        return "reflexivo"

    return "equilibrado"


# =================================================
# 🔥 IDENTIDADE COGNITIVA ADAPTATIVA (VERSÃO BASE)
# =================================================

def detect_cognitive_identity(username: str, current_intent: str, topic: str):

    style = detect_user_style(username)

    if current_intent == "decisao":
        return "estrategico_firme"

    if current_intent == "analise":
        return "mentor_equilibrado"

    if current_intent == "acao":
        return "executor_pragmatico"

    if topic == "emocional":
        return "apoio_emocional"

    if style == "visionario":
        return "visionario_expansivo"

    if style == "estrategico":
        return "estrategico_firme"

    return "mentor_equilibrado"

    def save_user_state(username: str, state: dict):

        # obter estado atual
        current_state = get_user_state(username)

        if isinstance(current_state, tuple):
            current_state = current_state[-1]

        if not isinstance(current_state, dict):
            current_state = {}

        # atualizar estado
        current_state.update(state)

        # aqui você salva no mesmo local onde o sistema guarda os estados
        user_states[username] = current_state