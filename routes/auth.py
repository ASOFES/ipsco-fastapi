"""
Routes d'authentification
Remplace Django Auth par JWT moderne
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """
    Connexion utilisateur
    Remplace Django login
    """
    # Pour le moment, authentification simple
    # À remplacer par votre logique d'auth
    if credentials.username == "admin" and credentials.password == "admin123":
        return LoginResponse(
            access_token="fake-jwt-token-for-testing",
            user_id=1,
            username=credentials.username
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nom d'utilisateur ou mot de passe incorrect"
    )

@router.post("/logout")
async def logout():
    """
    Déconnexion utilisateur
    """
    return {"message": "Déconnexion réussie"}

@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Informations utilisateur connecté
    """
    # Vérification simple du token
    if credentials.credentials == "fake-jwt-token-for-testing":
        return {
            "user_id": 1,
            "username": "admin",
            "role": "admin",
            "permissions": ["read", "write", "delete"]
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide"
    )
