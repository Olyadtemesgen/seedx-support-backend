from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel, Field
import uuid

@dataclass
class TicketBase:
    title: str
    description: str

class TicketCreate(TicketBase, BaseModel):
    pass

@dataclass
class TicketRead(TicketBase):
    id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID
