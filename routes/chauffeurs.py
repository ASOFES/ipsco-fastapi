"""
Routes API pour les chauffeurs
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel

router = APIRouter()

class ChauffeurResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    telephone: str
    numero_permis: str
    statut: str

@router.get("/", response_model=List[ChauffeurResponse])
async def get_chauffeurs():
    """
    Récupérer tous les chauffeurs
    """
    # Données d'exemple
    chauffeurs = [
        {
            "id": 1,
            "nom": "Mukadi",
            "prenom": "Jean",
            "telephone": "+243990123456",
            "numero_permis": "LBB123456",
            "statut": "actif"
        },
        {
            "id": 2,
            "nom": "Kasongo",
            "prenom": "Marie",
            "telephone": "+243991234567",
            "numero_permis": "LBB789012",
            "statut": "actif"
        },
        {
            "id": 3,
            "nom": "Tshimanga",
            "prenom": "Paul",
            "telephone": "+243992345678",
            "numero_permis": "LBB345678",
            "statut": "repos"
        }
    ]
    return chauffeurs

@router.get("/{chauffeur_id}")
async def get_chauffeur(chauffeur_id: int):
    """
    Détail d'un chauffeur
    """
    if chauffeur_id == 1:
        return {
            "id": 1,
            "nom": "Mukadi",
            "prenom": "Jean",
            "nom_complet": "Jean Mukadi",
            "telephone": "+243990123456",
            "numero_permis": "LBB123456",
            "date_obtention_permis": "2018-03-15",
            "statut": "actif",
            "missions_total": 45,
            "missions_ce_mois": 8,
            "note_moyenne": 4.6,
            "vehicule_attribue": {
                "id": 1,
                "immatriculation": "ABC-123",
                "marque": "Toyota",
                "modele": "Corolla"
            }
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Chauffeur non trouvé"
    )

@router.get("/{chauffeur_id}/missions")
async def get_chauffeur_missions(chauffeur_id: int):
    """
    Missions d'un chauffeur
    """
    return {
        "chauffeur_id": chauffeur_id,
        "missions": [
            {
                "id": 1,
                "destination": "Lubumbashi Centre",
                "date": "2025-01-15",
                "statut": "terminee",
                "distance_km": 25
            },
            {
                "id": 2,
                "destination": "Aéroport Luano",
                "date": "2025-01-14",
                "statut": "terminee",
                "distance_km": 45
            }
        ],
        "total_missions": 2,
        "total_km": 70
    }
