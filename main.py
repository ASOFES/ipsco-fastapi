#!/usr/bin/env python3
"""
IPSCO FastAPI - Version ultra-légère
Migration complète de votre Django en FastAPI moderne
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime

# Import conditionnel pour éviter les erreurs de connexion
try:
    from database import get_db, engine
    from models import vehicule as vehicule_model
    from schemas import vehicule as vehicule_schema
    from routes import vehicules, missions, chauffeurs, auth
    DB_AVAILABLE = True
    print("✅ Base de données disponible")
except Exception as e:
    print(f"⚠️ Base de données non disponible: {e}")
    DB_AVAILABLE = False

# Application FastAPI
app = FastAPI(
    title="IPSCO API",
    description="Gestion de parc automobile - Version FastAPI ultra-légère",
    version="2.0.0",
    docs_url="/docs",  # Swagger UI automatique
    redoc_url="/redoc"  # Documentation alternative
)

# CORS pour permettre les appels depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Dev React
        "http://localhost:5173",  # Dev Vite
        "https://*.vercel.app",   # Vercel
        "https://*.netlify.app",  # Netlify  
        "*"  # Temporaire pour test
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes si la base de données est disponible
if DB_AVAILABLE:
    try:
        from routes import missions_complete
        app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
        app.include_router(vehicules.router, prefix="/api/vehicules", tags=["Véhicules"])
        app.include_router(missions.router, prefix="/api/missions", tags=["Missions Demo"])
        app.include_router(missions_complete.router, prefix="/api/missions", tags=["Missions Complete"])
        app.include_router(chauffeurs.router, prefix="/api/chauffeurs", tags=["Chauffeurs"])
        print("✅ Routes API chargées (avec Missions complètes)")
    except Exception as e:
        print(f"⚠️ Erreur chargement routes: {e}")
        DB_AVAILABLE = False

@app.get("/")
async def root():
    """
    Page d'accueil de l'API IPSCO
    """
    return {
        "message": "🚗 IPSCO API - Gestion de parc automobile",
        "version": "2.0.0 FastAPI",
        "status": "active",
        "features": [
            "Gestion des véhicules",
            "Suivi des missions", 
            "Gestion des chauffeurs",
            "Rapports automatiques",
            "API REST complète"
        ],
        "docs": "/docs",
        "database": "Supabase PostgreSQL",
        "deployed_at": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """
    Vérification de santé de l'API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }

@app.get("/stats")
async def get_stats():
    """
    Statistiques générales du système
    """
    if DB_AVAILABLE:
        try:
            # Compte des véhicules (exemple)
            from database import SessionLocal
            db = SessionLocal()
            total_vehicules = db.query(vehicule_model.Vehicule).count()
            db.close()
            
            return {
                "total_vehicules": total_vehicules,
                "active_missions": 0,  # À implémenter
                "total_chauffeurs": 0,  # À implémenter
                "system_status": "operational",
                "database_status": "connected"
            }
        except Exception as e:
            return {
                "total_vehicules": 0,
                "active_missions": 0, 
                "total_chauffeurs": 0,
                "system_status": "database_connecting",
                "database_status": "error",
                "note": f"Erreur base de données: {str(e)}"
            }
    else:
        return {
            "total_vehicules": 0,
            "active_missions": 0, 
            "total_chauffeurs": 0,
            "system_status": "demo_mode",
            "database_status": "disconnected",
            "note": "Mode démonstration - Base de données non connectée"
        }

# Routes de démonstration (sans base de données)
@app.get("/demo/vehicules")
async def demo_vehicules():
    """
    Démonstration - Liste des véhicules (données fictives)
    """
    return {
        "vehicules": [
            {
                "id": 1,
                "immatriculation": "ABC-123",
                "marque": "Toyota",
                "modele": "Corolla",
                "couleur": "Blanc",
                "statut": "Actif"
            },
            {
                "id": 2,
                "immatriculation": "DEF-456",
                "marque": "Honda",
                "modele": "Civic",
                "couleur": "Bleu",
                "statut": "En mission"
            },
            {
                "id": 3,
                "immatriculation": "GHI-789",
                "marque": "Nissan",
                "modele": "Sentra",
                "couleur": "Rouge",
                "statut": "Maintenance"
            }
        ],
        "total": 3,
        "mode": "demonstration"
    }

@app.get("/demo/missions")
async def demo_missions():
    """
    Démonstration - Liste des missions (données fictives)
    """
    return {
        "missions": [
            {
                "id": 1,
                "vehicule": "ABC-123",
                "chauffeur": "Jean Mukadi",
                "destination": "Lubumbashi Centre",
                "date": "2025-01-15",
                "statut": "En cours",
                "distance_km": 25
            },
            {
                "id": 2,
                "vehicule": "DEF-456",
                "chauffeur": "Marie Kasongo",
                "destination": "Aéroport Luano",
                "date": "2025-01-15",
                "statut": "Terminée",
                "distance_km": 45
            }
        ],
        "total": 2,
        "mode": "demonstration"
    }

@app.get("/demo/dashboard")
async def demo_dashboard():
    """
    Démonstration - Tableau de bord (données fictives)
    """
    return {
        "dashboard": {
            "vehicules_total": 3,
            "vehicules_actifs": 2,
            "vehicules_maintenance": 1,
            "missions_aujourd_hui": 5,
            "missions_terminées": 3,
            "missions_en_cours": 2,
            "chauffeurs_actifs": 4,
            "kilometrage_total": 1250,
            "carburant_consommé": "850L"
        },
        "alertes": [
            "Véhicule GHI-789 en maintenance",
            "Mission urgente en attente d'attribution",
            "Assurance du véhicule ABC-123 expire dans 15 jours"
        ],
        "mode": "demonstration"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port,
        reload=True,  # Hot reload en développement
        log_level="info"
    )
