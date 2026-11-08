from sqlalchemy import Column, String, Float, Integer, DateTime
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    credits = Column(Float, default=20.0)
    subscription = Column(String, default="free")
    streak_days = Column(Integer, default=0)
    last_activity = Column(DateTime, nullable=True)
    phone_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
