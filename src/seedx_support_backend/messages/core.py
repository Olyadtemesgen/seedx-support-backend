from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel, Field
import uuid

@dataclass
class MessageBase:
    content: str = ""
    is_ai: bool = False

class MessageCreate(MessageBase, BaseModel):
    pass

@dataclass
class MessageRead:
    id: uuid.UUID
    created_at: datetime
    ticket_id: uuid.UUID
    author_id: uuid.UUID
    content: str = ""
    is_ai: bool = False

