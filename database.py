"""
Configuration de la base de données
Connexion à votre Supabase existante
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Utilisation de votre Supabase existante
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:ALcX66APUxYltilK@db.ruejckvikpewirrfzfhy.supabase.co:5432/postgres?sslmode=require"
)

# Configuration SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Vérifier la connexion
    pool_recycle=300,    # Recycler les connexions
    echo=False           # True pour voir les requêtes SQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency pour obtenir une session de base de données
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """
    Tester la connexion à Supabase
    """
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("✅ Connexion Supabase réussie!")
            return True
    except Exception as e:
        print(f"❌ Erreur connexion Supabase: {e}")
        return False

if __name__ == "__main__":
    test_connection()
