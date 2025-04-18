from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from .core import UserCreate, UserLogin, AuthResponse, UserPublic
from .repository import UserRepository
from .service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserPublic)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    svc = UserService(repo)
    return svc.register_user(user_in)

@router.post("/login", response_model=AuthResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    svc = UserService(repo)
    token = svc.authenticate_user(credentials.email, credentials.password)
    user = svc.validate_token(token)
    return AuthResponse(access_token=token, user=user)
