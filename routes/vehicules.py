"""
Routes API pour les véhicules
Remplace les vues Django
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.vehicule import Vehicule
from schemas.vehicule import (
    VehiculeCreate, 
    VehiculeUpdate, 
    VehiculeResponse, 
    VehiculeSummary,
    VehiculeList
)

router = APIRouter()

@router.get("/", response_model=List[VehiculeSummary])
async def get_vehicules(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(10, ge=1, le=100, description="Nombre d'éléments à retourner"),
    search: Optional[str] = Query(None, description="Recherche par immatriculation ou marque"),
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des véhicules
    Remplace la vue Django ListView
    """
    query = db.query(Vehicule)
    
    # Recherche
    if search:
        query = query.filter(
            (Vehicule.immatriculation.ilike(f"%{search}%")) |
            (Vehicule.marque.ilike(f"%{search}%")) |
            (Vehicule.modele.ilike(f"%{search}%"))
        )
    
    vehicules = query.offset(skip).limit(limit).all()
    
    # Ajouter nom_complet pour chaque véhicule
    for vehicule in vehicules:
        vehicule.nom_complet = vehicule.nom_complet
    
    return vehicules

@router.get("/{vehicule_id}", response_model=VehiculeResponse)
async def get_vehicule(vehicule_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un véhicule par ID
    Remplace la vue Django DetailView
    """
    vehicule = db.query(Vehicule).filter(Vehicule.id == vehicule_id).first()
    
    if not vehicule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Véhicule avec l'ID {vehicule_id} non trouvé"
        )
    
    return vehicule

@router.post("/", response_model=VehiculeResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicule(vehicule_data: VehiculeCreate, db: Session = Depends(get_db)):
    """
    Créer un nouveau véhicule
    Remplace la vue Django CreateView
    """
    # Vérifier l'unicité de l'immatriculation
    existing = db.query(Vehicule).filter(
        Vehicule.immatriculation == vehicule_data.immatriculation
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un véhicule avec cette immatriculation existe déjà"
        )
    
    # Vérifier l'unicité du châssis
    existing_chassis = db.query(Vehicule).filter(
        Vehicule.numero_chassis == vehicule_data.numero_chassis
    ).first()
    
    if existing_chassis:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un véhicule avec ce numéro de châssis existe déjà"
        )
    
    # Créer le véhicule
    vehicule = Vehicule(**vehicule_data.dict())
    db.add(vehicule)
    db.commit()
    db.refresh(vehicule)
    
    return vehicule

@router.put("/{vehicule_id}", response_model=VehiculeResponse)
async def update_vehicule(
    vehicule_id: int, 
    vehicule_data: VehiculeUpdate, 
    db: Session = Depends(get_db)
):
    """
    Modifier un véhicule
    Remplace la vue Django UpdateView
    """
    vehicule = db.query(Vehicule).filter(Vehicule.id == vehicule_id).first()
    
    if not vehicule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Véhicule avec l'ID {vehicule_id} non trouvé"
        )
    
    # Mettre à jour les champs modifiés
    update_data = vehicule_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(vehicule, field, value)
    
    db.commit()
    db.refresh(vehicule)
    
    return vehicule

@router.delete("/{vehicule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicule(vehicule_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un véhicule
    Remplace la vue Django DeleteView
    """
    vehicule = db.query(Vehicule).filter(Vehicule.id == vehicule_id).first()
    
    if not vehicule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Véhicule avec l'ID {vehicule_id} non trouvé"
        )
    
    db.delete(vehicule)
    db.commit()
    
    return None

@router.get("/{vehicule_id}/stats")
async def get_vehicule_stats(vehicule_id: int, db: Session = Depends(get_db)):
    """
    Statistiques d'un véhicule
    Nouvelle fonctionnalité FastAPI
    """
    vehicule = db.query(Vehicule).filter(Vehicule.id == vehicule_id).first()
    
    if not vehicule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Véhicule avec l'ID {vehicule_id} non trouvé"
        )
    
    # Calculer les jours avant expiration
    from datetime import date
    today = date.today()
    
    stats = {
        "vehicule_id": vehicule_id,
        "immatriculation": vehicule.immatriculation,
        "kilometrage_actuel": vehicule.kilometrage_actuel or 0,
        "kilometrage_depuis_entretien": (vehicule.kilometrage_actuel or 0) - vehicule.kilometrage_dernier_entretien,
        "jours_avant_expiration": {
            "assurance": (vehicule.date_expiration_assurance - today).days,
            "controle_technique": (vehicule.date_expiration_controle_technique - today).days,
            "vignette": (vehicule.date_expiration_vignette - today).days,
            "stationnement": (vehicule.date_expiration_stationnement - today).days
        },
        "alertes": []
    }
    
    # Générer les alertes
    for doc, jours in stats["jours_avant_expiration"].items():
        if jours < 0:
            stats["alertes"].append(f"{doc.title()} EXPIRÉ depuis {abs(jours)} jours")
        elif jours <= 30:
            stats["alertes"].append(f"{doc.title()} expire dans {jours} jours")
    
    return stats
