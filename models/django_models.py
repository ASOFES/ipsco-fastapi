"""
Modèles compatibles avec votre base Django existante
Tables existantes dans Supabase
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class CoreVehicule(Base):
    """
    Table core_vehicule de votre Django existant
    """
    __tablename__ = "core_vehicule"

    id = Column(Integer, primary_key=True, index=True)
    immatriculation = Column(String(20), unique=True, nullable=False)
    marque = Column(String(50), nullable=False)
    modele = Column(String(50), nullable=False)
    couleur = Column(String(30), nullable=False)
    numero_chassis = Column(String(50), unique=True, nullable=False)
    
    # Dates
    date_immatriculation = Column(Date, nullable=True)
    date_expiration_assurance = Column(Date, nullable=False)
    date_expiration_controle_technique = Column(Date, nullable=False)
    date_expiration_vignette = Column(Date, nullable=False)
    date_expiration_stationnement = Column(Date, nullable=False)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Kilométrage
    kilometrage_dernier_entretien = Column(Integer, default=0)
    kilometrage_actuel = Column(Integer, nullable=True)
    
    # Relations (si les tables existent)
    etablissement_id = Column(Integer, nullable=True)
    createur_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Vehicule {self.immatriculation} - {self.marque} {self.modele}>"

class CoreUtilisateur(Base):
    """
    Table core_utilisateur (AbstractUser Django)
    """
    __tablename__ = "core_utilisateur"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    first_name = Column(String(150))
    last_name = Column(String(150))
    email = Column(String(254))
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())
    
    # Champs personnalisés IPSCO
    telephone = Column(String(15))
    role = Column(String(20))
    departement_id = Column(Integer, nullable=True)

class CoreEtablissement(Base):
    """
    Table core_etablissement
    """
    __tablename__ = "core_etablissement"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    adresse = Column(Text)
    telephone = Column(String(15))
    email = Column(String(254))
    
class CoreCourse(Base):
    """
    Table core_course (Missions)
    """
    __tablename__ = "core_course"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicule_id = Column(Integer, ForeignKey('core_vehicule.id'))
    chauffeur_id = Column(Integer, ForeignKey('core_utilisateur.id'))
    demandeur_id = Column(Integer, ForeignKey('core_utilisateur.id'))
    
    destination = Column(String(200), nullable=False)
    lieu_depart = Column(String(200))
    date_souhaitee = Column(Date)
    heure_depart = Column(String(10))
    heure_retour = Column(String(10))
    
    distance_parcourue = Column(Integer, default=0)
    statut = Column(String(20), default='en_attente')
    
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())

# Fonctions utilitaires pour récupérer les données existantes
async def get_existing_tables(db):
    """
    Vérifier quelles tables existent déjà dans Supabase
    """
    try:
        result = db.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        return [row[0] for row in result.fetchall()]
    except Exception as e:
        print(f"Erreur vérification tables: {e}")
        return []
