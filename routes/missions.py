"""
Routes API pour les missions
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime
from database import get_db

router = APIRouter()

class MissionBase(BaseModel):
    destination: str
    date_mission: date
    vehicule_id: int
    chauffeur_id: Optional[int] = None
    distance_km: Optional[int] = None
    statut: str = "planifiee"

class MissionCreate(MissionBase):
    pass

class MissionResponse(MissionBase):
    id: int
    date_creation: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[dict])
async def get_missions():
    """
    Récupérer toutes les missions
    """
    # Données d'exemple (à remplacer par la vraie base)
    missions = [
        {
            "id": 1,
            "destination": "Lubumbashi Centre",
            "date_mission": "2025-01-15",
            "vehicule": "ABC-123",
            "chauffeur": "Jean Mukadi",
            "statut": "en_cours",
            "distance_km": 25
        },
        {
            "id": 2,
            "destination": "Aéroport Luano",
            "date_mission": "2025-01-15",
            "vehicule": "DEF-456",
            "chauffeur": "Marie Kasongo",
            "statut": "terminee",
            "distance_km": 45
        }
    ]
    return missions

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_mission(mission_data: MissionCreate):
    """
    Créer une nouvelle mission
    """
    # Logique de création (à implémenter avec la vraie base)
    return {
        "id": 3,
        **mission_data.dict(),
        "date_creation": datetime.now().isoformat(),
        "statut": "planifiee"
    }

@router.get("/{mission_id}")
async def get_mission(mission_id: int):
    """
    Détail d'une mission
    """
    if mission_id == 1:
        return {
            "id": 1,
            "destination": "Lubumbashi Centre",
            "date_mission": "2025-01-15",
            "vehicule": {
                "id": 1,
                "immatriculation": "ABC-123",
                "marque": "Toyota",
                "modele": "Corolla"
            },
            "chauffeur": {
                "id": 1,
                "nom": "Jean Mukadi",
                "telephone": "+243990123456"
            },
            "statut": "en_cours",
            "distance_km": 25,
            "heure_depart": "08:30",
            "heure_arrivee": None
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Mission non trouvée"
    )

@router.put("/{mission_id}/status")
async def update_mission_status(mission_id: int, nouveau_statut: str):
    """
    Mettre à jour le statut d'une mission
    """
    statuts_valides = ["planifiee", "en_cours", "terminee", "annulee"]
    
    if nouveau_statut not in statuts_valides:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statut invalide. Statuts valides: {statuts_valides}"
        )
    
    return {
        "mission_id": mission_id,
        "ancien_statut": "en_cours",
        "nouveau_statut": nouveau_statut,
        "mise_a_jour": datetime.now().isoformat()
    }
