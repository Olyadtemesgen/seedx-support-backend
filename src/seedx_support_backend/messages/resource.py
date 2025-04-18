from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from typing import List
from ..infrastructure.database import get_db
from src.middleware import get_current_user
from .core import MessageCreate, MessageRead
from .repository import MessageRepository
from .service import MessageService

router = APIRouter(prefix="/tickets/{ticket_id}/messages", tags=["messages"])

@router.post("", response_model=MessageRead)
def create_message(
    ticket_id: uuid.UUID,
    msg_in: MessageCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # optionally, check ticket exists and belongs to user; omitted for brevity
    repo = MessageRepository(db)
    svc = MessageService(repo)
    return svc.add_message(ticket_id, current_user.id, msg_in)

@router.get("", response_model=List[MessageRead])
def list_messages(
    ticket_id: uuid.UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # optionally, check user has access
    repo = MessageRepository(db)
    svc = MessageService(repo)
    return svc.list_messages(ticket_id)
