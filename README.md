# IPSCO FastAPI Backend

Backend moderne et léger pour la gestion de parc automobile IPSCO, développé avec FastAPI.

## 🚀 Technologies

- **FastAPI** - Framework web Python moderne et rapide
- **SQLAlchemy** - ORM pour la base de données
- **PostgreSQL** - Base de données (Supabase)
- **Pydantic** - Validation des données
- **Uvicorn** - Serveur ASGI

## 📦 Installation

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## 🔧 Configuration

1. Copier `.env.example` vers `.env`
2. Configurer les variables d'environnement :
   - `DATABASE_URL` : URL de connexion Supabase
   - `SECRET_KEY` : Clé secrète pour JWT

## 🏃‍♂️ Démarrage

```bash
# Mode développement
uvicorn main:app --reload

# Mode production
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🗄️ Base de données

Compatible avec votre base Django existante sur Supabase :
- Tables : `core_vehicule`, `core_course`, `core_utilisateur`
- Modèles SQLAlchemy compatibles
- Migration automatique des données existantes

## 🚀 Déploiement

### Render
1. Connecter le repository Git
2. Configurer les variables d'environnement
3. Déploiement automatique activé

### Variables d'environnement Render
- `DATABASE_URL` : URL Supabase
- `SECRET_KEY` : Généré automatiquement
- `DEBUG` : False en production
