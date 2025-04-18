from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from typing import List
from ..infrastructure.database import get_db
from src.middleware import get_current_user
from .core import TicketCreate, TicketRead
from .repository import TicketRepository
from .service import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("", response_model=List[TicketRead])
def list_tickets(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = TicketRepository(db)
    svc = TicketService(repo)
    return svc.list_tickets(current_user.id)

@router.post("", response_model=TicketRead)
def create_ticket(ticket_in: TicketCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = TicketRepository(db)
    svc = TicketService(repo)
    return svc.create_ticket(current_user.id, ticket_in)

@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: uuid.UUID, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    repo = TicketRepository(db)
    svc = TicketService(repo)
    ticket = svc.get_ticket(ticket_id)
    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return ticket
