from sqlalchemy import Column, String, Text, Float, Integer, DateTime, ForeignKey
from datetime import datetime
from .base import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    action = Column(String)
    prompt = Column(Text)
    response = Column(Text)
    credits_used = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
