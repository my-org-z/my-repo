from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, Dict
from app.models.payment import Payment, PaymentStatus
from app.services.user_service import get_user_by_id, update_credits, update_subscription
from app.services.credit_service import get_plans, get_packs
import uuid


class MobileMoneyAPI:
    @staticmethod
    def initiate(operator: str, phone: str, amount: float, reference: str) -> Dict:
        return {
            "success": True,
            "message": f"Paiement {operator} initialisé",
            "reference": reference,
            "payment_url": f"https://{operator}.tg/pay?ref={reference}",
        }

    @staticmethod
    def verify(operator: str, reference: str) -> Dict:
        return {"success": True, "status": "completed", "transaction_id": reference}


def create_payment(db: Session, user_id: str, amount: float, method: str, plan: Optional[str] = None, pack: Optional[str] = None) -> Payment:
    payment = Payment(
        id=str(uuid.uuid4()),
        user_id=user_id,
        amount=amount,
        method=method,
        plan=plan,
        credit_pack=pack,
        status=PaymentStatus.pending,
        reference=f"HINTAI-{uuid.uuid4().hex[:8].upper()}",
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def complete_payment(db: Session, payment_id: str, user_id: str, plan: Optional[str] = None, pack: Optional[str] = None) -> bool:
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        return False
    
    payment.status = PaymentStatus.completed
    payment.updated_at = datetime.utcnow()
    db.commit()
    
    if plan:
        plans = get_plans()
        if plan in plans:
            update_subscription(db, user_id, plan)
            update_credits(db, user_id, plans[plan]["credits"])
    elif pack:
        packs = get_packs()
        if pack in packs:
            update_credits(db, user_id, packs[pack]["credits"])
    
    return True


def process_payment(db: Session, user_id: str, plan: Optional[str] = None, pack: Optional[str] = None, method: str = "tmoney", phone: Optional[str] = None) -> Dict:
    if plan:
        plans = get_plans()
        if plan not in plans:
            return {"success": False, "message": "Plan invalide"}
        amount = plans[plan]["price"]
    elif pack:
        packs = get_packs()
        if pack not in packs:
            return {"success": False, "message": "Pack invalide"}
        amount = packs[pack]["price"]
    else:
        return {"success": False, "message": "Plan ou pack requis"}
    
    if method == "tmoney" and not phone:
        return {"success": False, "message": "Numéro de téléphone requis"}
    
    payment = create_payment(db, user_id, amount, method, plan, pack)
    
    if method == "tmoney":
        result = MobileMoneyAPI.initiate("tmoney", phone, amount, payment.reference)
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "payment_id": payment.id,
                "reference": payment.reference,
                "payment_url": result["payment_url"],
            }
    
    return {"success": False, "message": "Méthode non supportée"}


def verify_payment(db: Session, reference: str, method: str = "tmoney") -> Dict:
    result = MobileMoneyAPI.verify(method, reference)
    if result["success"] and result["status"] == "completed":
        payment = db.query(Payment).filter(Payment.reference == reference).first()
        if payment:
            complete_payment(db, payment.id, payment.user_id, payment.plan, payment.credit_pack)
            return {"success": True, "message": "Paiement validé"}
    return {"success": False, "message": "Paiement non trouvé ou échoué"}


def get_user_payments(db: Session, user_id: str, limit: int = 50) -> list:
    return db.query(Payment).filter(Payment.user_id == user_id).order_by(Payment.created_at.desc()).limit(limit).all()
