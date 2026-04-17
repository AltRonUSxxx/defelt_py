from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey, DateTime, String
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

engine = create_engine(
    "sqlite:///chat.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)

    messages = relationship("Message", back_populates="user")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_text = Column(Text)
    ai_text = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="messages")

Base.metadata.create_all(bind=engine)