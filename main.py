from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.memory_manager import init_db
from database.database import Base, engine
from database.models import User, Profile
from database import models

import os

app = FastAPI(
    title="Orion Cloud",
    version="1.0"
)

# =========================
# 🔥 BASE DIR (ABSOLUTO SEGURO)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# =========================
# 🔥 GARANTE PASTAS
# =========================
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# 🔥 BANCO DE DADOS
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# 🔥 CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🔥 STATIC FILES
# =========================

# HTML do painel
app.mount("/painel", StaticFiles(directory=STATIC_DIR, html=True), name="painel")

# Arquivos estáticos (css/js/img)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Uploads (imagens do usuário)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# =========================
# 🚀 STARTUP
# =========================
@app.on_event("startup")
def startup():
    init_db()

# =========================
# 🔗 ROTAS API
# =========================
app.include_router(router)

# =========================
# 🔥 ROOT
# =========================
@app.get("/")
def root():
    return {
        "system": "Orion Cloud",
        "status": "online"
    }

# =========================
# 🔧 TESTE
# =========================
@app.get("/teste2")
def teste2():
    return {"ok": "main funcionando"}