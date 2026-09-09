from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.models.user import User
from app.core.security import get_password_hash
import uuid


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_phone(db: Session, phone: str) -> Optional[User]:
    return db.query(User).filter(User.phone_number == phone).first()


def create_user(db: Session, username: str, email: Optional[str] = None, password: Optional[str] = None, phone: Optional[str] = None) -> User:
    hashed_password = get_password_hash(password) if password else None
    user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        hashed_password=hashed_password,
        phone_number=phone,
        credits=20.0,
        subscription="free",
        streak_days=0,
        last_activity=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_credits(db: Session, user_id: str, amount: float) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    user.credits += amount
    db.commit()
    return True


def deduct_credits(db: Session, user_id: str, amount: float) -> bool:
    user = get_user_by_id(db, user_id)
    if not user or user.credits < amount:
        return False
    user.credits -= amount
    db.commit()
    return True


def check_credits(db: Session, user_id: str, amount: float) -> bool:
    user = get_user_by_id(db, user_id)
    return user is not None and user.credits >= amount


def update_streak(db: Session, user_id: str) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    today = datetime.utcnow().date()
    last_date = user.last_activity.date() if user.last_activity else None
    
    if last_date and (today - last_date).days == 1:
        user.streak_days += 1
        if user.streak_days == 3:
            user.credits += 6
        elif user.streak_days == 6:
            user.credits += 12
    elif last_date and (today - last_date).days > 1:
        user.streak_days = 1
    else:
        user.streak_days += 1
    
    user.last_activity = datetime.utcnow()
    db.commit()
    return True


def update_subscription(db: Session, user_id: str, plan: str) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    user.subscription = plan
    db.commit()
    return True
