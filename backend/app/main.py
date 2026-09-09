from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional, List
from sqlalchemy.orm import Session
import uuid

from app.core.config import settings
from app.core.security import create_token, verify_password as verify_pwd
from app.ai.client import get_ai_response, get_ai_stream
from app.ai.vision import analyze_image, extract_text, enhance_image
from app.utils.helpers import process_image, resize_image, convert_pdf_to_images
from app.services.storage import get_db, init_db
from app.services.user_service import (
    get_user_by_id, get_user_by_username, get_user_by_email, get_user_by_phone, create_user,
    update_credits, deduct_credits, check_credits, update_streak, update_subscription
)
from app.services.credit_service import can_perform, perform, get_credits, add_credits, get_plans, get_packs, ACTION_COSTS
from app.services.payment_service import process_payment, verify_payment, get_user_payments, create_payment
from app.models.user import User
from app.models.exercise import Exercise
from app.models.payment import Payment, PaymentStatus


app = FastAPI(
    title="HintAI API",
    description="Backend éducatif avec IA, paiements Mobile Money et système de crédits",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Helper Functions ---

def save_history(db: Session, user_id: str, action: str, prompt: str, response: str, credits: float):
    history = Exercise(user_id=user_id, action=action, prompt=prompt, response=response, credits_used=credits)
    db.add(history)
    db.commit()


# --- Routes ---

@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "HintAI API - Backend éducatif avec Pixtral"}


# ============ AUTHENTIFICATION ============

@app.post("/auth/register")
def register(
    username: str = Form(...),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    if get_user_by_username(db, username):
        raise HTTPException(400, "Nom d'utilisateur déjà pris")
    if email and get_user_by_email(db, email):
        raise HTTPException(400, "Email déjà utilisé")
    if phone and get_user_by_phone(db, phone):
        raise HTTPException(400, "Numéro déjà utilisé")

    user = create_user(db, username, email, password, phone)
    token = create_token({"sub": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone_number,
            "credits": user.credits,
            "subscription": user.subscription,
        }
    }


@app.post("/auth/login")
def login(
    identifier: str = Form(...),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    user = get_user_by_username(db, identifier) or get_user_by_email(db, identifier) or get_user_by_phone(db, identifier)
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")

    if password and user.hashed_password and not verify_pwd(password, user.hashed_password):
        raise HTTPException(401, "Mot de passe incorrect")

    token = create_token({"sub": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone_number,
            "credits": user.credits,
            "subscription": user.subscription,
        }
    }


@app.get("/auth/me")
def me(user_id: str = Query(...), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone_number,
        "credits": user.credits,
        "subscription": user.subscription,
        "streak_days": user.streak_days,
        "last_activity": user.last_activity,
    }


# ============ CRÉDITS ============

@app.get("/credits")
def get_user_credits(user_id: str = Query(...), db: Session = Depends(get_db)):
    return {"credits": get_credits(db, user_id)}


@app.post("/rewarded-ads/watch")
def watch_ad(user_id: str = Form(...), db: Session = Depends(get_db)):
    add_credits(db, user_id, 1)
    update_streak(db, user_id)
    return {"message": "+1 crédit ajouté !", "credits": get_credits(db, user_id)}


# ============ ABONNEMENTS ============

@app.get("/subscriptions/plans")
def plans():
    return get_plans()


@app.get("/subscriptions/packs")
def packs():
    return get_packs()


@app.get("/subscriptions/me")
def my_subscription(user_id: str = Query(...), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")
    plan = get_plans().get(user.subscription, get_plans()["free"])
    return {"plan": user.subscription, "name": plan["name"], "credits": plan["credits"], "price": plan["price"]}


# ============ PAIEMENTS ============

@app.post("/payments/subscribe")
def subscribe(
    user_id: str = Form(...),
    plan: str = Form(...),
    method: str = Form("tmoney"),
    phone: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    if method == "tmoney" and not phone:
        raise HTTPException(400, "Numéro de téléphone requis pour TMoney")
    return process_payment(db, user_id, plan=plan, method=method, phone=phone)


@app.post("/payments/buy-credits")
def buy_credits(
    user_id: str = Form(...),
    pack: str = Form(...),
    method: str = Form("tmoney"),
    phone: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    if method == "tmoney" and not phone:
        raise HTTPException(400, "Numéro de téléphone requis pour TMoney")
    return process_payment(db, user_id, pack=pack, method=method, phone=phone)


@app.post("/payments/verify")
def verify(
    reference: str = Form(...),
    method: str = Form("tmoney"),
    db: Session = Depends(get_db),
):
    return verify_payment(db, reference, method)


@app.get("/payments/history")
def payment_history(user_id: str = Query(...), limit: int = 50, db: Session = Depends(get_db)):
    payments = get_user_payments(db, user_id, limit)
    return [
        {
            "id": p.id,
            "amount": p.amount,
            "currency": p.currency,
            "method": p.method,
            "plan": p.plan,
            "credit_pack": p.credit_pack,
            "status": p.status,
            "reference": p.reference,
            "created_at": p.created_at,
        }
        for p in payments
    ]


# ============ HELP ME ============

@app.post("/help-me/text")
def help_me_text(
    user_id: str = Form(...),
    exercise: str = Form(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)
    if not user:
        user = create_user(db, f"guest_{user_id}")
        user_id = user.id

    if not can_perform(db, user_id, "ai_analysis_help_me"):
        raise HTTPException(400, f"Il faut {ACTION_COSTS['ai_analysis_help_me']} crédits")

    prompt = f"""Tu es un professeur d'aide aux devoirs. Analyse cet exercice et fournis une réponse progressive:
Exercice: {exercise}

Réponds en suivant ces étapes:
1. Compréhension de l'exercice (1 phrase)
2. Indice 1 (pour commencer)
3. Indice 2 (si l'élève bloque)
4. Indice 3 (si l'élève bloque toujours)
5. Solution complète (si demandé)

Commence par l'étape 1."""

    response = get_ai_response(prompt)
    perform(db, user_id, "ai_analysis_help_me")
    update_streak(db, user_id)
    save_history(db, user_id, "help_me_text", exercise, response, ACTION_COSTS["ai_analysis_help_me"])

    return {"response": response, "credits": get_credits(db, user_id)}


@app.post("/help-me/image")
async def help_me_image(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)
    if not user:
        user = create_user(db, f"guest_{user_id}")
        user_id = user.id

    image_data = await file.read()
    analysis = analyze_image(image_data)
    if not analysis["valid"]:
        raise HTTPException(400, f"Image invalide: {analysis['reason']}")

    extracted_text = extract_text(image_data)
    if not extracted_text:
        raise HTTPException(400, "Aucun texte détecté")

    total_cost = ACTION_COSTS["upload_image"] + ACTION_COSTS["ai_analysis_help_me"]
    if not can_perform(db, user_id, "upload_image") or not can_perform(db, user_id, "ai_analysis_help_me"):
        raise HTTPException(400, f"Il faut {total_cost} crédits")

    prompt = """Tu es un professeur. Analyse cette image d'exercice et fournis une réponse progressive:
1. Compréhension
2. Indice 1
3. Indice 2
4. Indice 3
5. Solution
Commence par l'étape 1."""

    response = get_ai_response(prompt, image_data=image_data)
    perform(db, user_id, "upload_image")
    perform(db, user_id, "ai_analysis_help_me")
    update_streak(db, user_id)
    save_history(db, user_id, "help_me_image", extracted_text, response, total_cost)

    return {"response": response, "text": extracted_text, "credits": get_credits(db, user_id)}


@app.post("/help-me/pdf")
async def help_me_pdf(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)
    if not user:
        user = create_user(db, f"guest_{user_id}")
        user_id = user.id

    pdf_data = await file.read()
    images = convert_pdf_to_images(pdf_data)
    if not images:
        raise HTTPException(400, "Aucune image extraite du PDF")

    image_data = images[0]
    analysis = analyze_image(image_data)
    if not analysis["valid"]:
        raise HTTPException(400, f"Image invalide: {analysis['reason']}")

    extracted_text = extract_text(image_data)
    if not extracted_text:
        raise HTTPException(400, "Aucun texte détecté")

    total_cost = ACTION_COSTS["upload_pdf"] + ACTION_COSTS["ai_analysis_help_me"]
    if not can_perform(db, user_id, "upload_pdf") or not can_perform(db, user_id, "ai_analysis_help_me"):
        raise HTTPException(400, f"Il faut {total_cost} crédits")

    prompt = f"""Analyse cet exercice du PDF et fournis une réponse progressive:
Exercice: {extracted_text}
1. Compréhension
2. Indice 1
3. Indice 2
4. Indice 3
5. Solution"""

    response = get_ai_response(prompt)
    perform(db, user_id, "upload_pdf")
    perform(db, user_id, "ai_analysis_help_me")
    update_streak(db, user_id)
    save_history(db, user_id, "help_me_pdf", extracted_text, response, total_cost)

    return {"response": response, "text": extracted_text, "credits": get_credits(db, user_id)}


# ============ INDICES ============

@app.post("/help-me/hint")
def get_hint(
    user_id: str = Form(...),
    exercise: str = Form(...),
    hint_number: int = Query(1, ge=1, le=3),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)
    if not user:
        user = create_user(db, f"guest_{user_id}")
        user_id = user.id

    action = f"hint_{hint_number}"
    if not can_perform(db, user_id, action):
        raise HTTPException(400, f"Il faut {ACTION_COSTS[action]} crédit")

    prompt = f"Fournis l'indice {hint_number} pour cet exercice: {exercise}"
    response = get_ai_response(prompt)
    perform(db, user_id, action)
    update_streak(db, user_id)
    save_history(db, user_id, action, exercise, response, ACTION_COSTS[action])

    return {"response": response, "credits": get_credits(db, user_id)}


# ============ SOLUTION COMPLÈTE ============

@app.post("/help-me/full-solution")
def full_solution(
    user_id: str = Form(...),
    exercise: str = Form(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)
    if not user:
        user = create_user(db, f"guest_{user_id}")
        user_id = user.id

    if not can_perform(db, user_id, "full_solution"):
        raise HTTPException(400, f"Il faut {ACTION_COSTS['full_solution']} crédits")

    prompt = f"""Fournis la solution complète et détaillée pour cet exercice: {exercise}
Structure:
1. Étapes de résolution
2. Calculs intermédiaires
3. Réponse finale"""

    response = get_ai_response(prompt)
    perform(db, user_id, "full_solution")
    update_streak(db, user_id)
    save_history(db, user_id, "full_solution", exercise, response, ACTION_COSTS["full_solution"])

    return {"response": response, "credits": get_credits(db, user_id)}


# ============ LEARN A CONCEPT ============

@app.post("/learn-concept")
def learn_concept(
    user_id: str = Form(...),
    concept: str = Form(...),
    user_explanation: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)
    if not user:
        user = create_user(db, f"guest_{user_id}")
        user_id = user.id

    if not can_perform(db, user_id, "learn_explanation"):
        raise HTTPException(400, f"Il faut {ACTION_COSTS['learn_explanation']} crédits")

    prompt = f"""Tu es un professeur patient. Explique ce concept à un élève de 14 ans: {concept}
Structure:
1. Définition simple
2. Exemple concret
3. Question pour vérifier la compréhension"""

    if user_explanation:
        prompt += f"\nL'élève pense comprendre: {user_explanation}. Corrigé si nécessaire."

    response = get_ai_response(prompt)
    perform(db, user_id, "learn_explanation")
    update_streak(db, user_id)
    save_history(db, user_id, "learn_concept", concept, response, ACTION_COSTS["learn_explanation"])

    return {"response": response, "credits": get_credits(db, user_id)}


@app.post("/learn-concept/continue")
def learn_continue(
    user_id: str = Form(...),
    concept: str = Form(...),
    previous_response: str = Form(...),
    user_input: str = Form(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)
    if not user:
        user = create_user(db, f"guest_{user_id}")
        user_id = user.id

    if not can_perform(db, user_id, "learn_question"):
        raise HTTPException(400, f"Il faut {ACTION_COSTS['learn_question']} crédit")

    prompt = f"""Suite de l'apprentissage sur: {concept}
Précédente réponse: {previous_response}
Réponse élève: {user_input}
Réponds de manière adaptée:
- Si compris: propose un exercice simple
- Si difficultés: donne un indice ou explication
- Si question: réponds clairement"""

    response = get_ai_response(prompt)
    perform(db, user_id, "learn_question")
    update_streak(db, user_id)
    save_history(db, user_id, "learn_continue", user_input, response, ACTION_COSTS["learn_question"])

    return {"response": response, "credits": get_credits(db, user_id)}


# ============ STREAMING ============

@app.post("/stream/help-me")
def stream_help_me(
    user_id: str = Form(...),
    exercise: str = Form(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)
    if not user:
        user = create_user(db, f"guest_{user_id}")
        user_id = user.id

    if not check_credits(db, user_id, ACTION_COSTS["ai_analysis_help_me"]):
        raise HTTPException(400, "Pas assez de crédits")

    deduct_credits(db, user_id, ACTION_COSTS["ai_analysis_help_me"])
    update_streak(db, user_id)

    prompt = f"""Analyse cet exercice: {exercise}
Réponds progressivement:
1. Compréhension
2. Indice 1
3. Indice 2
4. Solution"""

    return StreamingResponse(get_ai_stream(prompt), media_type="text/plain")


# ============ HISTORIQUE ============

@app.get("/history")
def history(user_id: str = Query(...), limit: int = 50, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")

    items = db.query(Exercise).filter(Exercise.user_id == user_id).order_by(Exercise.timestamp.desc()).limit(limit).all()
    return [
        {"id": i.id, "action": i.action, "prompt": i.prompt, "response": i.response, "credits": i.credits_used, "timestamp": i.timestamp}
        for i in items
    ]
