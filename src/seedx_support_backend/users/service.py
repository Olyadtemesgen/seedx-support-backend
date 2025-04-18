from datetime import datetime
from fastapi import HTTPException, status
from .repository import UserRepository
from .auth import hash_password, verify_password, create_access_token, decode_token
from .core import UserCreate, Role, UserPublic
from typing import Optional

class UserService:
    def __init__(
        self,
        repo: Optional[UserRepository] = None,
        jwt_key: Optional[str] = None,
        jwt_secret: Optional[str] = None,
        expire_minutes: Optional[str] = None,
    ):
        self.repo = repo
        self.jwt_key = jwt_key
        self.jwt_secret = jwt_secret
        self.expire_minutes = expire_minutes

    def register_user(self, user_in: UserCreate) -> UserPublic:
        if self.repo.get_by_email(user_in.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        hashed = hash_password(user_in.password)
        user = self.repo.create({
            "name": user_in.name,
            "email": user_in.email,
            "hashed_password": hashed,
            "role": Role.USER.value,
        })
        return UserPublic(
            id=user.id,
            name=user.name,
            email=user.email,
            role=Role(user.role),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def authenticate_user(self, email: str, password: str) -> str:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credentials")
        return create_access_token({"sub": str(user.id)})

    def validate_token(self, token: str) -> UserPublic:
        payload = decode_token(token)
        user_id = payload.get("sub")
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return UserPublic(
            id=user.id,
            name=user.name,
            email=user.email,
            role=Role(user.role),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
