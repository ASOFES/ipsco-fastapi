"""
Modèle Véhicule FastAPI
Remplace le modèle Django par SQLAlchemy
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Boolean
from sqlalchemy.sql import func
from database import Base

class Vehicule(Base):
    """
    Modèle Véhicule - Version FastAPI
    Compatible avec votre structure Django existante
    """
    __tablename__ = "core_vehicule"  # Même nom que Django
    __table_args__ = {'extend_existing': True}  # Éviter le conflit de table

    id = Column(Integer, primary_key=True, index=True)
    immatriculation = Column(String(20), unique=True, index=True, nullable=False)
    marque = Column(String(50), nullable=False)
    modele = Column(String(50), nullable=False)
    couleur = Column(String(30), nullable=False)
    numero_chassis = Column(String(50), unique=True, nullable=False)
    
    # Dates importantes
    date_immatriculation = Column(Date, nullable=True)
    date_expiration_assurance = Column(Date, nullable=False)
    date_expiration_controle_technique = Column(Date, nullable=False)
    date_expiration_vignette = Column(Date, nullable=False)
    date_expiration_stationnement = Column(Date, nullable=False)
    
    # Métadonnées
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Kilométrage
    kilometrage_dernier_entretien = Column(Integer, default=0)
    kilometrage_actuel = Column(Integer, nullable=True)
    
    # Image (path vers le fichier)
    image_path = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Vehicule {self.immatriculation} - {self.marque} {self.modele}>"
    
    @property
    def nom_complet(self):
        """Nom complet du véhicule"""
        return f"{self.immatriculation} - {self.marque} {self.modele}"
