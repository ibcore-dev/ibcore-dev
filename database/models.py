from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime


# =========================
# USUÁRIO
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    profile = relationship("Profile", back_populates="owner", uselist=False)


# =========================
# PERFIL
# =========================
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    bio = Column(String)
    cover_image_url = Column(String)
    foto = Column(String)
    nome = Column(String)
    relacionamento = Column(String)
    nascimento = Column(String)
    profissao = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="profile")


# =========================
# POSTS
# =========================
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    content = Column(String)

    media_url = Column(String)
    media_type = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")


# =========================
# LIKES
# =========================
class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))


# =========================
# COMENTÁRIOS
# =========================
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))


# =========================
# AMIGOS
# =========================
class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True)

    requester_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String, default="pending")  # pending, accepted


# =================================================
# 🧠 MEMÓRIA DO ÓRION (CURTO PRAZO)
# =================================================
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    username = Column(String, index=True)
    role = Column(String)  # "user" ou "assistant"
    content = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)


# =================================================
# 🧠 MEMÓRIA DE LONGO PRAZO (APRENDIZADO)
# =================================================
class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True)

    username = Column(String, index=True)
    key = Column(String)   # ex: "objetivo", "profissao"
    value = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)