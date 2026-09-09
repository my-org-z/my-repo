from sqlalchemy import Column, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum

Base = declarative_base()


class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String)
    amount = Column(Float)
    currency = Column(String, default="XOF")
    method = Column(String)  # tmoney, momo, etc.
    plan = Column(String, nullable=True)  # subscription plan
    credit_pack = Column(String, nullable=True)  # credit pack
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    reference = Column(String, unique=True)
    phone_number = Column(String, nullable=True)
    operator = Column(String, nullable=True)
    metadata = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
