from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

    
    profile = relationship("Profile", back_populates="owner", uselist=False)


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

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    content = Column(String)

    media_url = Column(String)     # 🔥 NOVO
    media_type = Column(String)    # 🔥 NOVO

    created_at = Column(String, default=str(datetime.utcnow()))

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True)

    requester_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String, default="pending")  # pending, accepted