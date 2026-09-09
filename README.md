# HintAI

**HintAI** est une application web éducative basée sur l'intelligence artificielle qui aide les élèves à comprendre et résoudre leurs exercices progressivement.

## 🚀 Fonctionnalités

### Help Me
- Analyse d'exercices via texte, image ou PDF
- Indices progressifs (3 niveaux)
- Solution complète
- Analyse locale avec OpenCV.js pour la qualité d'image
- Streaming des réponses IA

### Learn a Concept
- Apprentissage de concepts avec parcours pédagogique
- Explications adaptées
- Exercices d'évaluation
- Questions/réponses interactives

### Système de crédits
- 20 crédits gratuits pour le plan Free
- Plans d'abonnement (Basic, Pro, Pro Plus, Super, Heavy)
- Packs de crédits supplémentaires
- Bonus de série (3 jours = +6 crédits, 6 jours = +12 crédits)
- Publicités récompensées (+1 crédit)

### Paiements
- Intégration TMoney (Togo)
- Intégration Mobile Money (MTN/Airtel)
- Système de paiement sécurisé

## 📁 Structure du projet

```
HintAI/
├── backend/                  # Backend FastAPI
│   ├── app/
│   │   ├── main.py           # Routes API
│   │   ├── ai/
│   │   │   ├── client.py     # Client Mistral/Pixtral
│   │   │   └── vision.py     # Traitement images (OpenCV)
│   │   ├── core/
│   │   │   ├── config.py     # Configuration
│   │   │   └── security.py   # Authentification JWT
│   │   ├── models/
│   │   │   ├── user.py       # Modèle utilisateur
│   │   │   ├── exercise.py   # Modèle exercice
│   │   │   └── payment.py    # Modèle paiement
│   │   ├── services/
│   │   │   ├── user_service.py   # Gestion utilisateurs
│   │   │   ├── credit_service.py # Gestion crédits
│   │   │   ├── payment_service.py # Gestion paiements
│   │   │   └── storage.py    # Base de données
│   │   └── utils/
│   │       └── helpers.py    # Fonctions utilitaires
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                 # Frontend
│   ├── src/
│   │   ├── index.html        # Page principale
│   │   ├── style.css         # Styles
│   │   ├── analyser.js       # OpenCV.js
│   │   └── main.js           # Logique principale
│   └── assets/
│       ├── icons/
│       └── uploads/
│
├── db/                      # Base de données SQLite
│   └── hints.db
│
└── README.md
```

## 🛠️ Configuration

### Backend

1. **Installer les dépendances**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos clés API
```

3. **Démarrer le serveur**
```bash
uvicorn app.main:app --reload
```

### Frontend

Ouvrir `frontend/src/index.html` dans un navigateur ou servir avec un serveur web local:
```bash
cd frontend
python -m http.server 8000
```

### Base de données

Par défaut, SQLite est utilisé. Pour PostgreSQL (Neon):
```
DATABASE_URL=postgres://user:password@ep-xxx.neon.tech/dbname
```

## 🔧 Déploiement

### Backend (Render)
1. Créer un compte sur [Render](https://render.com)
2. Connecter votre dépôt GitHub
3. Sélectionner le dossier `backend/`
4. Configurer les variables d'environnement
5. Déployer

### Frontend (GitHub Pages)
1. Activer GitHub Pages dans les paramètres du dépôt
2. Sélectionner la branche `main` et le dossier `/frontend`
3. Le site sera accessible à `https://username.github.io/HintAI/`

## 🎯 API Endpoints

### Authentification
- `POST /auth/register` - Inscription
- `POST /auth/login` - Connexion
- `GET /auth/me` - Informations utilisateur

### Help Me
- `POST /help-me/text` - Analyser un exercice (texte)
- `POST /help-me/image` - Analyser un exercice (image)
- `POST /help-me/pdf` - Analyser un exercice (PDF)
- `POST /help-me/hint` - Obtenir un indice
- `POST /help-me/full-solution` - Solution complète
- `POST /stream/help-me` - Streaming de la réponse

### Learn a Concept
- `POST /learn-concept` - Commencer l'apprentissage
- `POST /learn-concept/continue` - Continuer la session

### Crédits
- `GET /credits` - Solde de crédits
- `POST /rewarded-ads/watch` - Regarder une pub (+1 crédit)

### Abonnements
- `GET /subscriptions/plans` - Liste des plans
- `GET /subscriptions/packs` - Liste des packs de crédits
- `GET /subscriptions/me` - Mon abonnement

### Paiements
- `POST /payments/subscribe` - Souscrire à un plan
- `POST /payments/buy-credits` - Acheter des crédits
- `POST /payments/verify` - Vérifier un paiement
- `GET /payments/history` - Historique des paiements

### Historique
- `GET /history` - Historique des sessions

## 💰 Système de crédits

| Action | Coût |
|--------|------|
| Ouvrir Help Me | Gratuit |
| Saisie texte | Gratuit |
| Caméra | Gratuit |
| Upload image | 0.5 crédit |
| Upload PDF | 0.5 crédit |
| Analyse IA initiale | 2 crédits |
| Indice 1/2/3 | 1 crédit chacun |
| Solution complète | 2 crédits |
| Learn a Concept (initial) | 2 crédits |
| Question/Indice (Learn) | 1 crédit |

### Plans d'abonnement

| Plan | Prix/mois | Crédits/mois |
|------|-----------|--------------|
| Free | $0 | 20 |
| Basic | $5 | 40 |
| Pro | $10 | 80 |
| Pro Plus | $15 | 150 |
| Super | $20 | 200 |
| Heavy | $30 | 300 |

### Packs de crédits

| Pack | Prix | Crédits |
|------|------|---------|
| 10 crédits | $1 | 10 |
| 20 crédits | $2 | 20 |
| 50 crédits | $5 | 50 |
| 100 crédits | $8 | 100 |

## 🤖 Intelligence Artificielle

HintAI utilise **Pixtral** (Mistral AI) pour:
- L'analyse de texte
- La vision (analyse d'images)
- La génération de réponses pédagogiques

### Configuration

1. Créer un compte sur [Mistral Studio](https://console.mistral.ai/)
2. Obtenir une clé API
3. Configurer dans `.env`:
```
MISTRAL_API_KEY=your_api_key
MISTRAL_MODEL=pixtral-12b
```

## 💳 Paiements Mobile Money

### TMoney (Togo)
- Configurer `TMONEY_API_KEY` dans `.env`
- Intégration avec l'API TMoney

### Mobile Money (MTN/Airtel)
- Configurer `MOMO_API_KEY` dans `.env`
- Intégration avec les APIs Mobile Money

## 📱 Frontend

### Fonctionnalités
- Interface responsive (mobile + desktop)
- Caméra intégrée
- Upload d'images/PDF
- Analyse locale avec OpenCV.js
- Streaming des réponses IA
- Gestion des crédits
- Paiements Mobile Money
- Historique des sessions

### Dépendances
- [OpenCV.js](https://docs.opencv.org/4.7.0/opencv.js) - Traitement d'images

## 🔒 Sécurité

- Authentification JWT
- Protection des routes API
- Validation des entrées
- Système anti-abus (crédits, paiements)

## 📝 Licence

MIT

## 🙏 Contribuer

Les contributions sont les bienvenues ! Ouvrez une Pull Request ou un Issue pour discuter des améliorations.

---

**Développé avec ❤️ pour les élèves du Togo**
