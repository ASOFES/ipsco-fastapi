"""
Routes véhicules avec vraies données Supabase
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.django_models import CoreVehicule
from schemas.vehicule import VehiculeResponse, VehiculeSummary
from datetime import date

router = APIRouter()

@router.get("/real", response_model=List[dict])
async def get_real_vehicules(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Récupérer les vrais véhicules depuis Supabase
    """
    try:
        query = db.query(CoreVehicule)
        
        # Recherche
        if search:
            query = query.filter(
                (CoreVehicule.immatriculation.ilike(f"%{search}%")) |
                (CoreVehicule.marque.ilike(f"%{search}%")) |
                (CoreVehicule.modele.ilike(f"%{search}%"))
            )
        
        vehicules = query.offset(skip).limit(limit).all()
        total = query.count()
        
        # Convertir en format JSON avec statut calculé
        vehicules_data = []
        today = date.today()
        
        for v in vehicules:
            # Calculer le statut basé sur les dates d'expiration
            statut = "actif"
            alerts = []
            
            # Vérifier les expirations
            if v.date_expiration_assurance <= today:
                statut = "alerte"
                alerts.append("Assurance expirée")
            elif v.date_expiration_controle_technique <= today:
                statut = "alerte" 
                alerts.append("Contrôle technique expiré")
            elif (v.date_expiration_assurance - today).days <= 30:
                statut = "attention"
                alerts.append(f"Assurance expire dans {(v.date_expiration_assurance - today).days} jours")
            
            vehicules_data.append({
                "id": v.id,
                "immatriculation": v.immatriculation,
                "marque": v.marque,
                "modele": v.modele,
                "couleur": v.couleur,
                "numero_chassis": v.numero_chassis,
                "statut": statut,
                "alerts": alerts,
                "kilometrage_actuel": v.kilometrage_actuel or 0,
                "date_creation": v.date_creation.isoformat() if v.date_creation else None,
                "dates_expiration": {
                    "assurance": v.date_expiration_assurance.isoformat(),
                    "controle_technique": v.date_expiration_controle_technique.isoformat(),
                    "vignette": v.date_expiration_vignette.isoformat(),
                    "stationnement": v.date_expiration_stationnement.isoformat()
                }
            })
        
        return {
            "vehicules": vehicules_data,
            "total": total,
            "source": "supabase_real_data",
            "count": len(vehicules_data)
        }
        
    except Exception as e:
        # Si erreur base de données, retourner données de démo
        print(f"Erreur Supabase: {e}")
        return {
            "vehicules": [
                {
                    "id": 1,
                    "immatriculation": "ABC-123",
                    "marque": "Toyota",
                    "modele": "Corolla",
                    "couleur": "Blanc",
                    "statut": "actif",
                    "alerts": [],
                    "kilometrage_actuel": 45000
                }
            ],
            "total": 1,
            "source": "demo_data_fallback",
            "error": str(e)
        }

@router.get("/stats")
async def get_vehicules_stats(db: Session = Depends(get_db)):
    """
    Statistiques des véhicules depuis Supabase
    """
    try:
        total = db.query(CoreVehicule).count()
        
        # Compter par statut calculé
        vehicules = db.query(CoreVehicule).all()
        today = date.today()
        
        actifs = 0
        alertes = 0
        attention = 0
        
        for v in vehicules:
            if v.date_expiration_assurance <= today or v.date_expiration_controle_technique <= today:
                alertes += 1
            elif (v.date_expiration_assurance - today).days <= 30:
                attention += 1
            else:
                actifs += 1
        
        return {
            "total_vehicules": total,
            "vehicules_actifs": actifs,
            "vehicules_attention": attention,
            "vehicules_alerte": alertes,
            "source": "supabase",
            "last_updated": date.today().isoformat()
        }
        
    except Exception as e:
        return {
            "total_vehicules": 0,
            "vehicules_actifs": 0,
            "vehicules_attention": 0,
            "vehicules_alerte": 0,
            "source": "error",
            "error": str(e)
        }

@router.get("/tables")
async def check_tables(db: Session = Depends(get_db)):
    """
    Vérifier les tables disponibles dans Supabase
    """
    try:
        result = db.execute("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'core_%'
            ORDER BY table_name, ordinal_position;
        """)
        
        tables = {}
        for row in result.fetchall():
            table_name = row[0]
            if table_name not in tables:
                tables[table_name] = []
            tables[table_name].append({
                "column": row[1],
                "type": row[2]
            })
        
        return {
            "available_tables": list(tables.keys()),
            "table_details": tables,
            "total_tables": len(tables)
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "message": "Impossible de vérifier les tables Supabase"
        }
