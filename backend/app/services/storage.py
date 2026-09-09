from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models import UserBase, ExerciseBase, PaymentBase

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    UserBase.metadata.create_all(bind=engine)
    ExerciseBase.metadata.create_all(bind=engine)
    PaymentBase.metadata.create_all(bind=engine)
