from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
import uuid

class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

@dataclass
class UserBase:
    name: str
    email: EmailStr

class UserCreate(UserBase, BaseModel):
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

@dataclass
class UserPublic(UserBase):
    id: uuid.UUID
    role: Role
    created_at: datetime
    updated_at: datetime

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
