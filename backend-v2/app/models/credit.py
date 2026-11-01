"""
Credit and payment models for HintAI V2.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend_v2.app.core.database import Base
from enum import Enum


class TransactionType(str, Enum):
    PURCHASE = "purchase"
    REWARD = "reward"
    SUBSCRIPTION = "subscription"
    USAGE = "usage"
    REFUND = "refund"
    BONUS = "bonus"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    TMONEY = "tmoney"
    MOMO_MTN = "momo_mtn"
    MOMO_AIRTEL = "momo_airtel"
    CARD = "card"
    REWARDED_ADS = "rewarded_ads"


class SubscriptionPlan(Base):
    """
    Subscription plan (Free, Basic, Pro, etc.).
    """
    __tablename__ = "subscription_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # Pricing
    monthly_price = Column(Integer, nullable=False)  # Price in FCFA or cents
    yearly_price = Column(Integer)  # Optional yearly price
    currency = Column(String(3), default="XOF")  # FCFA = XOF
    
    # Credits
    credit_bonus = Column(Integer, default=0)  # Monthly credit bonus
    initial_credits = Column(Integer, default=0)  # Credits given on first subscription
    
    # Features
    features = Column(JSON, default=[])  # List of features included
    max_exam_attempts = Column(Integer)  # Max exam attempts per month
    max_annales_access = Column(String(20), default="full")  # none, limited, full
    max_study_groups = Column(Integer, default=5)  # Max study groups
    max_flashcards = Column(Integer)  # Max flashcards
    
    # Limits
    max_ai_requests = Column(Integer)  # Max AI requests per day
    max_file_uploads = Column(Integer)  # Max file uploads per day
    
    # Status
    is_active = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)
    
    # Order
    order = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="subscription_plan")
    subscriptions = relationship("UserSubscription", back_populates="subscription_plan", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<SubscriptionPlan(id={self.id}, name={self.name})>"


class CreditTransaction(Base):
    """
    Track credit transactions (purchases, usage, rewards, etc.).
    """
    __tablename__ = "credit_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Transaction details
    amount = Column(Integer, nullable=False)  # Positive for credits added, negative for credits used
    type = Column(String(20), nullable=False)  # TransactionType enum
    description = Column(Text)
    
    # Metadata
    metadata = Column(JSON, default={})  # Additional details (e.g., {"plan": "pro", "duration": "1 month"})
    reference_id = Column(String(100))  # Reference to related entity (e.g., payment_id, exam_id)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="credit_transactions")
    
    def __repr__(self):
        return f"<CreditTransaction(id={self.id}, user_id={self.user_id}, amount={self.amount})>"


class Payment(Base):
    """
    Track payments (TMoney, Mobile Money, etc.).
    """
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Payment details
    amount = Column(Integer, nullable=False)  # Amount in smallest currency unit (e.g., FCFA)
    currency = Column(String(3), default="XOF")
    method = Column(String(20), nullable=False)  # PaymentMethod enum
    
    # Transaction IDs
    transaction_id = Column(String(100), unique=True)  # External transaction ID (e.g., from TMoney)
    reference_id = Column(String(100))  # Internal reference
    
    # Status
    status = Column(String(20), default=PaymentStatus.PENDING)
    failure_reason = Column(Text)
    
    # Metadata
    metadata = Column(JSON, default={})  # Additional details from payment provider
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="payments")
    subscription = relationship("UserSubscription", back_populates="payment", uselist=False)
    
    def __repr__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount}, status={self.status})>"
