"""
Schémas Pydantic pour les véhicules
Remplace Django Forms et Serializers
"""

from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime

class VehiculeBase(BaseModel):
    """Schéma de base pour les véhicules"""
    immatriculation: str
    marque: str
    modele: str
    couleur: str
    numero_chassis: str
    date_immatriculation: Optional[date] = None
    date_expiration_assurance: date
    date_expiration_controle_technique: date
    date_expiration_vignette: date
    date_expiration_stationnement: date
    kilometrage_actuel: Optional[int] = None

    @validator('immatriculation')
    def validate_immatriculation(cls, v):
        """Valider le format d'immatriculation"""
        if not v or len(v.strip()) < 3:
            raise ValueError('Immatriculation doit avoir au moins 3 caractères')
        return v.strip().upper()
    
    @validator('numero_chassis')
    def validate_chassis(cls, v):
        """Valider le numéro de châssis"""
        if not v or len(v.strip()) < 5:
            raise ValueError('Numéro de châssis doit avoir au moins 5 caractères')
        return v.strip().upper()

class VehiculeCreate(VehiculeBase):
    """Schéma pour créer un véhicule"""
    pass

class VehiculeUpdate(BaseModel):
    """Schéma pour modifier un véhicule"""
    immatriculation: Optional[str] = None
    marque: Optional[str] = None
    modele: Optional[str] = None
    couleur: Optional[str] = None
    numero_chassis: Optional[str] = None
    date_expiration_assurance: Optional[date] = None
    date_expiration_controle_technique: Optional[date] = None
    date_expiration_vignette: Optional[date] = None
    date_expiration_stationnement: Optional[date] = None
    kilometrage_actuel: Optional[int] = None

class VehiculeResponse(VehiculeBase):
    """Schéma de réponse pour les véhicules"""
    id: int
    date_creation: datetime
    date_modification: Optional[datetime] = None
    kilometrage_dernier_entretien: int = 0
    image_path: Optional[str] = None
    
    class Config:
        from_attributes = True  # Pour SQLAlchemy

class VehiculeList(BaseModel):
    """Schéma pour la liste des véhicules"""
    vehicules: list[VehiculeResponse]
    total: int
    page: int = 1
    per_page: int = 10

class VehiculeSummary(BaseModel):
    """Résumé d'un véhicule pour les listes"""
    id: int
    immatriculation: str
    marque: str
    modele: str
    couleur: str
    nom_complet: str
    
    class Config:
        from_attributes = True
