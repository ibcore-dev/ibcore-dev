from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Body
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import sqlite3

from app.security.hashing import hash_password, verify_password
from app.security.auth import create_token, decode_token, get_current_user
from app.core.decision_engine import DecisionEngine

from datetime import datetime
from database.database import get_db
from database.models import User as DBUser, Profile as DBProfile
from database.models import Post, Like, Comment, Friend
from pydantic import BaseModel

import os
import shutil
from uuid import uuid4


def log_error(message, route):
    conn = sqlite3.connect("orion.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS error_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        route TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    INSERT INTO error_logs (message, route)
    VALUES (?, ?)
    """, (message, route))

    conn.commit()
    conn.close()

router = APIRouter()
engine = DecisionEngine()

UPLOAD_DIR = "uploads"

# =========================
# MODELS
# =========================
class User(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class CommandInput(BaseModel):
    input: str


class ProfileUpdate(BaseModel):
    nome: Optional[str] = None
    bio: Optional[str] = None
    profissao: Optional[str] = None
    nascimento: Optional[str] = None
    relacionamento: Optional[str] = None
    foto: Optional[str] = None
    capa: Optional[str] = None

class PostCreate(BaseModel):
    content: Optional[str] = None
    media: Optional[str] = None
    mediaType: Optional[str] = None
    
# =========================
# REGISTER
# =========================

@router.post("/register")
def register(user: User, db: Session = Depends(get_db)):

    existing = db.query(DBUser).filter(DBUser.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    new_user = DBUser(
        username=user.username,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário criado com sucesso"}

# =========================
# LOGIN
# =========================
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(DBUser).filter(DBUser.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_token({"sub": str(db_user.id)})

    return {"access_token": token}
# =========================
# COMMAND
# =========================

@router.post("/command")
def command(data: CommandInput, current_user: DBUser = Depends(get_current_user)):

    try:
        username = current_user.username

        response = engine.process(username, data.input)

        return {"response": response}

    except Exception as e:
        print("🔥 ERRO COMMAND:", e)
        log_error(str(e), "/command")
        raise HTTPException(status_code=500, detail="Erro interno no Órion")
# =========================
# 🖼️ UPLOAD IMAGEM
# =========================

@router.post("/upload-profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: DBUser = Depends(get_current_user)
):

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    ext = file.filename.split(".")[-1].lower()

    if ext not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Formato inválido")

    filename = f"{uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "image_url": f"uploads/{filename}"
    }

# =========================
# 👤 SALVAR PERFIL (FIX TOTAL)
# =========================

@router.post("/profile/save")
def save_profile(
    data: ProfileUpdate,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:
        profile = db.query(DBProfile).filter(DBProfile.user_id == current_user.id).first()

        # cria se não existir
        if not profile:
            profile = DBProfile(user_id=current_user.id)
            db.add(profile)
            db.commit()
            db.refresh(profile)

        # atualiza campos
        if data.nome is not None:
            profile.nome = data.nome

        if data.bio is not None:
            profile.bio = data.bio

        if data.profissao is not None:
            profile.profissao = data.profissao

        if data.nascimento is not None:
            profile.nascimento = data.nascimento

        if data.relacionamento is not None:
            profile.relacionamento = data.relacionamento

        if data.foto is not None:
            profile.foto = data.foto

        if data.capa is not None:
            profile.cover_image_url = data.capa

        db.commit()
        db.refresh(profile)

        return {"msg": "Perfil salvo com sucesso"}

    except Exception as e:
        print("🔥 ERRO SAVE:", e)
        log_error(str(e), "/profile/save")
        raise HTTPException(status_code=500, detail=str(e))
        

# =========================
# 📥 CARREGAR PERFIL
# =========================

@router.get("/profile/me")
def get_my_profile(
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        profile = db.query(DBProfile).filter(DBProfile.user_id == current_user.id).first()

        if not profile:
            return {
                "nome": current_user.username,
                "bio": "",
                "profissao": "",
                "nascimento": "",
                "relacionamento": "",
                "foto": "",
                "capa": ""
            }

        return {
            "nome": profile.nome or current_user.username,
            "bio": profile.bio or "",
            "profissao": profile.profissao or "",
            "nascimento": profile.nascimento or "",
            "relacionamento": profile.relacionamento or "",
            "foto": profile.foto or "",
            "capa": profile.cover_image_url or ""
        }

    except Exception as e:
        print("🔥 ERRO REAL:", e)
        log_error(str(e), "/profile/me")
        raise HTTPException(status_code=500, detail=str(e))
# =========================
# TESTE
# =========================

@router.get("/teste")
def teste():
    return {"ok": True}

# =========================
# ADMIN
# =========================

@router.get("/admin/dashboard")
def admin_dashboard(
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    usuarios = db.query(DBUser).count()

    import sqlite3
    conn = sqlite3.connect("orion.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM memory")
    mensagens = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM error_logs")
    erros = cursor.fetchone()[0]

    conn.close()

    return {
        "usuarios": usuarios,
        "mensagens": mensagens,
        "ia": mensagens,
        "erros": erros,
        "historico": [5, 10, 8, 12, 15]
    }

@router.get("/admin/usuarios")
def listar_usuarios(
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    users = db.query(DBUser).all()
    lista = [user.username for user in users]

    return {
        "usuarios": lista
    }
    

@router.post("/posts/create")
def create_post(
    data: PostCreate,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        post = Post(
            content=data.content or "",
            media_url=data.media,
            media_type=data.mediaType,
            user_id=current_user.id,
            created_at=str(datetime.utcnow())
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        return {"msg": "Post criado"}

    except Exception as e:
        print("🔥 ERRO REAL:", e)
        log_error(str(e), "/posts/create")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/posts/feed")
def get_feed(db: Session = Depends(get_db)):

    posts = db.query(Post).order_by(Post.id.desc()).all()

    result = []

    for p in posts:

        user = db.query(DBUser).filter(DBUser.id == p.user_id).first()

        likes = db.query(Like).filter(Like.post_id == p.id).count()

        comments = db.query(Comment).filter(Comment.post_id == p.id).all()

        comentarios_formatados = []

        for c in comments:
            user_c = db.query(DBUser).filter(DBUser.id == c.user_id).first()

            comentarios_formatados.append({
                "user": user_c.username if user_c else "Usuário",
                "content": c.content
            })

        result.append({
            "id": p.id,
            "user": user.username if user else "Usuário",
            "content": p.content,
            "time": p.created_at,
            "likes": likes,
            "comments": comentarios_formatados,
            "media": p.media_url,
            "mediaType": p.media_type,
        })

    return result

@router.post("/posts/like/{post_id}")
def like_post(
    post_id: int,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.post_id == post_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"msg": "Descurtido"}

    like = Like(user_id=current_user.id, post_id=post_id)
    db.add(like)
    db.commit()

    return {"msg": "Curtido"}

@router.post("/posts/comment/{post_id}")
def comment_post(
    post_id: int,
    data: dict,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    comment = Comment(
        content=data.get("content"),
        user_id=current_user.id,
        post_id=post_id
    )

    db.add(comment)
    db.commit()

    return {"msg": "Comentado"}

@router.get("/posts/me")
def get_my_posts(
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    posts = db.query(Post)\
        .filter(Post.user_id == current_user.id)\
        .order_by(Post.id.desc())\
        .all()

    result = []

    for p in posts:

        likes = db.query(Like).filter(Like.post_id == p.id).count()

        comments = db.query(Comment).filter(Comment.post_id == p.id).all()

        comentarios_formatados = []

        for c in comments:
            user_c = db.query(DBUser).filter(DBUser.id == c.user_id).first()

            comentarios_formatados.append({
                "user": user_c.username if user_c else "Usuário",
                "content": c.content
            })

        result.append({
            "id": p.id,
            "user": current_user.username,
            "content": p.content,
            "time": p.created_at,
            "likes": likes,
            "comments": comentarios_formatados,
            "media": p.media_url,
            "mediaType": p.media_type,
        })

    return result

@router.delete("/posts/delete/{post_id}")
def delete_post(
    post_id: int,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado")

    db.delete(post)
    db.commit()

    return {"msg": "Post deletado"}

@router.put("/posts/edit/{post_id}")
def edit_post(
    post_id: int,
    data: dict,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado")

    post.content = data.get("content", post.content)

    db.commit()

    return {"msg": "Post atualizado"}

@router.post("/friends/add/{user_id}")
def add_friend(user_id: int, current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):

    existing = db.query(Friend).filter(
        Friend.requester_id == current_user.id,
        Friend.receiver_id == user_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Já enviado")

    friend = Friend(
        requester_id=current_user.id,
        receiver_id=user_id,
        status="pending"  # 🔥 ESSENCIAL
    )

    db.add(friend)
    db.commit()

    return {"msg": "Solicitação enviada"}

@router.post("/friends/accept/{friend_id}")
def accept_friend(friend_id: int, current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):

    f = db.query(Friend).filter(Friend.id == friend_id).first()

    if not f:
        raise HTTPException(status_code=404)

    if f.receiver_id != current_user.id:
        raise HTTPException(status_code=403)

    f.status = "accepted"
    db.commit()

    return {"msg": "Amigo adicionado"}

@router.get("/friends/requests")
def get_requests(current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):

    requests = db.query(Friend).filter(
        Friend.receiver_id == current_user.id
    ).all()

    result = []

    for r in requests:
        user = db.query(DBUser).filter(DBUser.id == r.requester_id).first()

        if not user:
            continue

        result.append({
            "id": r.id,
            "user": user.username,
            "foto": user.profile.foto if user.profile and user.profile.foto else ""
        })

    return result

@router.get("/friends/list")
def get_friends(current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):

    friends = db.query(Friend).filter(
        ((Friend.requester_id == current_user.id) | (Friend.receiver_id == current_user.id)),
        Friend.status == "accepted"
    ).all()

    result = []

    for f in friends:
        other_id = f.receiver_id if f.requester_id == current_user.id else f.requester_id

        user = db.query(DBUser).filter(DBUser.id == other_id).first()

        result.append({
            "id": user.id,
            "username": user.username,
            "foto": user.profile.foto if user.profile and user.profile.foto else ""
        })

    return result

@router.get("/users/search")
def search_users(q: str = "", current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):

    users = db.query(DBUser).filter(
        DBUser.username.contains(q),
        DBUser.id != current_user.id
    ).all()

    result = []

    for u in users:
        result.append({
            "id": u.id,
            "username": u.username
        })

    return result

@router.get("/users/suggestions")
def suggestions(current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):

    # pega todas amizades do usuário
    relations = db.query(Friend).filter(
        (Friend.requester_id == current_user.id) |
        (Friend.receiver_id == current_user.id)
    ).all()

    ids_relacionados = set()

    for r in relations:
        ids_relacionados.add(r.requester_id)
        ids_relacionados.add(r.receiver_id)

    users = db.query(DBUser).filter(
        DBUser.id != current_user.id,
        ~DBUser.id.in_(ids_relacionados)
    ).limit(10).all()

    return [
        {
            "id": u.id,
            "username": u.username,
            "foto": u.profile.foto if u.profile and u.profile.foto else ""
        }
        for u in users
    ]

@router.get("/admin/errors")
def listar_erros(current_user: DBUser = Depends(get_current_user)):

    conn = sqlite3.connect("orion.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT message, route, timestamp
    FROM error_logs
    ORDER BY id DESC
    LIMIT 10
    """)

    erros = cursor.fetchall()

    conn.close()

    return {"erros": erros}