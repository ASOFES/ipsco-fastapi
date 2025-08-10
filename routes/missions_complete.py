"""
Module Missions complet avec CRUD
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime
from database import get_db

router = APIRouter()

# Modèles Pydantic
class MissionBase(BaseModel):
    destination: str
    lieu_depart: Optional[str] = None
    date_souhaitee: date
    heure_depart: Optional[str] = None
    heure_retour: Optional[str] = None
    vehicule_id: Optional[int] = None
    chauffeur_id: Optional[int] = None
    demandeur_id: Optional[int] = None
    observations: Optional[str] = None

class MissionCreate(MissionBase):
    pass

class MissionUpdate(BaseModel):
    destination: Optional[str] = None
    statut: Optional[str] = None
    vehicule_id: Optional[int] = None
    chauffeur_id: Optional[int] = None
    heure_depart: Optional[str] = None
    heure_retour: Optional[str] = None
    distance_parcourue: Optional[int] = None

class MissionResponse(MissionBase):
    id: int
    statut: str
    distance_parcourue: Optional[int] = None
    date_creation: datetime
    date_modification: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Données de démonstration enrichies
MISSIONS_DEMO = [
    {
        "id": 1,
        "destination": "Lubumbashi Centre-Ville",
        "lieu_depart": "Bureau IPSCO",
        "date_souhaitee": "2025-01-15",
        "heure_depart": "08:30",
        "heure_retour": "17:00",
        "vehicule": {"id": 1, "immatriculation": "ABC-123", "marque": "Toyota", "modele": "Corolla"},
        "chauffeur": {"id": 1, "nom": "Jean Mukadi", "telephone": "+243990123456"},
        "demandeur": {"id": 2, "nom": "Marie Tshimanga", "departement": "Administration"},
        "statut": "en_cours",
        "distance_parcourue": 25,
        "date_creation": "2025-01-15T08:00:00",
        "observations": "Mission urgente - Transport documents importants"
    },
    {
        "id": 2,
        "destination": "Aéroport International Luano",
        "lieu_depart": "Hôtel Lubumbashi",
        "date_souhaitee": "2025-01-15",
        "heure_depart": "14:00",
        "heure_retour": "16:30",
        "vehicule": {"id": 2, "immatriculation": "DEF-456", "marque": "Honda", "modele": "Civic"},
        "chauffeur": {"id": 2, "nom": "Paul Kasongo", "telephone": "+243991234567"},
        "demandeur": {"id": 3, "nom": "David Mbuyi", "departement": "Direction"},
        "statut": "terminee",
        "distance_parcourue": 45,
        "date_creation": "2025-01-15T13:30:00",
        "observations": "Transport VIP - Ponctualité requise"
    },
    {
        "id": 3,
        "destination": "Université de Lubumbashi",
        "lieu_depart": "Bureau IPSCO",
        "date_souhaitee": "2025-01-16",
        "heure_depart": "09:00",
        "heure_retour": "12:00",
        "vehicule": {"id": 3, "immatriculation": "GHI-789", "marque": "Nissan", "modele": "Sentra"},
        "chauffeur": {"id": 3, "nom": "Alice Mwamba", "telephone": "+243992345678"},
        "demandeur": {"id": 4, "nom": "Prof. Kabamba", "departement": "Formation"},
        "statut": "planifiee",
        "distance_parcourue": 0,
        "date_creation": "2025-01-14T16:00:00",
        "observations": "Mission formation - Matériel pédagogique à transporter"
    },
    {
        "id": 4,
        "destination": "Clinique Bondeko",
        "lieu_depart": "Résidence Personnel",
        "date_souhaitee": "2025-01-16",
        "heure_depart": "07:00",
        "heure_retour": "08:00",
        "vehicule": None,
        "chauffeur": None,
        "demandeur": {"id": 5, "nom": "Infirmier Chef", "departement": "Santé"},
        "statut": "en_attente",
        "distance_parcourue": 0,
        "date_creation": "2025-01-15T20:00:00",
        "observations": "Urgence médicale - Priorité absolue"
    }
]

@router.get("/", response_model=List[dict])
async def get_missions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    statut: Optional[str] = Query(None, description="Filtrer par statut"),
    date_debut: Optional[date] = Query(None),
    date_fin: Optional[date] = Query(None),
    chauffeur_id: Optional[int] = Query(None),
    vehicule_id: Optional[int] = Query(None)
):
    """
    Récupérer toutes les missions avec filtres avancés
    """
    missions = MISSIONS_DEMO.copy()
    
    # Filtres
    if statut:
        missions = [m for m in missions if m["statut"].lower() == statut.lower()]
    
    if date_debut:
        missions = [m for m in missions if m["date_souhaitee"] >= str(date_debut)]
    
    if date_fin:
        missions = [m for m in missions if m["date_souhaitee"] <= str(date_fin)]
    
    if chauffeur_id:
        missions = [m for m in missions if m["chauffeur"] and m["chauffeur"]["id"] == chauffeur_id]
    
    if vehicule_id:
        missions = [m for m in missions if m["vehicule"] and m["vehicule"]["id"] == vehicule_id]
    
    # Pagination
    total = len(missions)
    missions = missions[skip:skip + limit]
    
    return {
        "missions": missions,
        "total": total,
        "page": skip // limit + 1,
        "per_page": limit,
        "filters_applied": {
            "statut": statut,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "chauffeur_id": chauffeur_id,
            "vehicule_id": vehicule_id
        }
    }

@router.get("/{mission_id}")
async def get_mission(mission_id: int):
    """
    Détail complet d'une mission
    """
    mission = next((m for m in MISSIONS_DEMO if m["id"] == mission_id), None)
    
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission {mission_id} non trouvée"
        )
    
    # Ajouter des détails supplémentaires
    mission_detail = mission.copy()
    mission_detail["timeline"] = [
        {"time": "08:00", "event": "Mission créée", "status": "completed"},
        {"time": "08:30", "event": "Départ confirmé", "status": "completed" if mission["statut"] != "planifiee" else "pending"},
        {"time": "12:00", "event": "Arrivée destination", "status": "completed" if mission["statut"] == "terminee" else "pending"},
        {"time": "17:00", "event": "Retour bureau", "status": "completed" if mission["statut"] == "terminee" else "pending"}
    ]
    
    return mission_detail

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_mission(mission_data: MissionCreate):
    """
    Créer une nouvelle mission
    """
    new_id = max([m["id"] for m in MISSIONS_DEMO]) + 1
    
    new_mission = {
        "id": new_id,
        **mission_data.dict(),
        "statut": "en_attente",
        "distance_parcourue": 0,
        "date_creation": datetime.now().isoformat(),
        "vehicule": None,
        "chauffeur": None,
        "demandeur": {"id": 1, "nom": "Utilisateur", "departement": "Général"}
    }
    
    MISSIONS_DEMO.append(new_mission)
    
    return {
        "mission": new_mission,
        "message": "Mission créée avec succès",
        "next_steps": [
            "Attribution d'un véhicule",
            "Assignment d'un chauffeur",
            "Validation par le dispatcher"
        ]
    }

@router.put("/{mission_id}")
async def update_mission(mission_id: int, mission_data: MissionUpdate):
    """
    Modifier une mission
    """
    mission_index = next((i for i, m in enumerate(MISSIONS_DEMO) if m["id"] == mission_id), None)
    
    if mission_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission {mission_id} non trouvée"
        )
    
    # Mettre à jour les champs modifiés
    update_data = mission_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field in MISSIONS_DEMO[mission_index]:
            MISSIONS_DEMO[mission_index][field] = value
    
    MISSIONS_DEMO[mission_index]["date_modification"] = datetime.now().isoformat()
    
    return {
        "mission": MISSIONS_DEMO[mission_index],
        "message": "Mission mise à jour avec succès"
    }

@router.put("/{mission_id}/statut")
async def update_mission_statut(mission_id: int, nouveau_statut: str):
    """
    Changer le statut d'une mission
    """
    statuts_valides = ["en_attente", "planifiee", "en_cours", "terminee", "annulee"]
    
    if nouveau_statut not in statuts_valides:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statut invalide. Statuts valides: {statuts_valides}"
        )
    
    mission_index = next((i for i, m in enumerate(MISSIONS_DEMO) if m["id"] == mission_id), None)
    
    if mission_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission {mission_id} non trouvée"
        )
    
    ancien_statut = MISSIONS_DEMO[mission_index]["statut"]
    MISSIONS_DEMO[mission_index]["statut"] = nouveau_statut
    MISSIONS_DEMO[mission_index]["date_modification"] = datetime.now().isoformat()
    
    return {
        "mission_id": mission_id,
        "ancien_statut": ancien_statut,
        "nouveau_statut": nouveau_statut,
        "timestamp": datetime.now().isoformat(),
        "message": f"Statut changé de '{ancien_statut}' vers '{nouveau_statut}'"
    }

@router.get("/stats/dashboard")
async def get_missions_stats():
    """
    Statistiques des missions pour le dashboard
    """
    total = len(MISSIONS_DEMO)
    
    stats_by_status = {}
    for mission in MISSIONS_DEMO:
        statut = mission["statut"]
        stats_by_status[statut] = stats_by_status.get(statut, 0) + 1
    
    # Missions d'aujourd'hui
    today = date.today().isoformat()
    missions_today = [m for m in MISSIONS_DEMO if m["date_souhaitee"] == today]
    
    # Distance totale
    distance_totale = sum([m["distance_parcourue"] for m in MISSIONS_DEMO])
    
    return {
        "total_missions": total,
        "missions_aujourd_hui": len(missions_today),
        "stats_by_status": stats_by_status,
        "distance_totale_km": distance_totale,
        "missions_actives": stats_by_status.get("en_cours", 0),
        "missions_en_attente": stats_by_status.get("en_attente", 0),
        "taux_completion": round((stats_by_status.get("terminee", 0) / total * 100), 1) if total > 0 else 0
    }

@router.delete("/{mission_id}")
async def delete_mission(mission_id: int):
    """
    Supprimer une mission
    """
    mission_index = next((i for i, m in enumerate(MISSIONS_DEMO) if m["id"] == mission_id), None)
    
    if mission_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission {mission_id} non trouvée"
        )
    
    deleted_mission = MISSIONS_DEMO.pop(mission_index)
    
    return {
        "message": f"Mission {mission_id} supprimée avec succès",
        "mission_supprimee": {
            "id": deleted_mission["id"],
            "destination": deleted_mission["destination"],
            "statut": deleted_mission["statut"]
        }
    }
