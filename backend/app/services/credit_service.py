from sqlalchemy.orm import Session
from app.services.user_service import check_credits, deduct_credits, update_credits


ACTION_COSTS = {
    "open_help_me": 0, "text_input": 0, "camera": 0, "opencv_check": 0,
    "local_crop": 0, "open_learn": 0, "local_history": 0, "auth": 0,
    "view_history": 0, "replay": 0,
    "upload_image": 0.5, "upload_pdf": 0.5,
    "hint_1": 1, "hint_2": 1, "hint_3": 1, "ai_question": 1,
    "generate_exercise": 1, "correct_work": 1, "exercise_question": 1,
    "exercise_hint": 1, "learn_question": 1, "learn_hint": 1,
    "simple_exercise": 1, "correct_exercise": 1, "new_explanation": 1,
    "ai_analysis": 1,
    "ai_analysis_help_me": 2, "full_solution": 2, "learn_explanation": 2,
    "hard_exercise": 2,
}


SUBSCRIPTION_PLANS = {
    "free": {"price": 0, "credits": 20, "name": "Free"},
    # SUSPENDU: Aucun abonnement payant ne fonctionne sans méthode de paiement
    # "basic": {"price": 5, "credits": 40, "name": "Basic"},
    # "pro": {"price": 10, "credits": 80, "name": "Pro"},
    # "pro_plus": {"price": 15, "credits": 150, "name": "Pro Plus"},
    # "super": {"price": 20, "credits": 200, "name": "Super"},
    # "heavy": {"price": 30, "credits": 300, "name": "Heavy"},
}


CREDIT_PACKS = {
    # SUSPENDU: Aucun pack de crédits n'est disponible sans système de paiement
    # "pack_10": {"credits": 10, "price": 1, "name": "10 crédits"},
    # "pack_20": {"credits": 20, "price": 2, "name": "20 crédits"},
    # "pack_50": {"credits": 50, "price": 5, "name": "50 crédits"},
    # "pack_100": {"credits": 100, "price": 8, "name": "100 crédits"},
}


def can_perform(db: Session, user_id: str, action: str) -> bool:
    cost = ACTION_COSTS.get(action, 0)
    return cost == 0 or check_credits(db, user_id, cost)


def perform(db: Session, user_id: str, action: str) -> bool:
    cost = ACTION_COSTS.get(action, 0)
    if cost == 0:
        return True
    return deduct_credits(db, user_id, cost)


def get_credits(db: Session, user_id: str) -> float:
    from app.services.user_service import get_user_by_id
    user = get_user_by_id(db, user_id)
    return user.credits if user else 0


def add_credits(db: Session, user_id: str, amount: float) -> bool:
    return update_credits(db, user_id, amount)


def get_plans() -> dict:
    return SUBSCRIPTION_PLANS


def get_packs() -> dict:
    return CREDIT_PACKS
