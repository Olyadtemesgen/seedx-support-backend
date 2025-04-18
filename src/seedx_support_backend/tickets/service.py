from fastapi import HTTPException, status
import uuid
from .repository import TicketRepository
from .core import TicketCreate, TicketRead

class TicketService:
    def __init__(self, repo: TicketRepository):
        self.repo = repo

    def list_tickets(self, user_id: uuid.UUID) -> list[TicketRead]:
        tickets = self.repo.list_by_user(user_id)
        return [TicketRead(
            id=t.id,
            title=t.title,
            description=t.description,
            status=t.status,
            created_at=t.created_at,
            updated_at=t.updated_at,
            user_id=t.user_id,
        ) for t in tickets]

    def create_ticket(self, user_id: uuid.UUID, ticket_in: TicketCreate) -> TicketRead:
        t = self.repo.create({
            "title": ticket_in.title,
            "description": ticket_in.description,
            "status": "open",
            "user_id": user_id,
        })
        return TicketRead(
            id=t.id,
            title=t.title,
            description=t.description,
            status=t.status,
            created_at=t.created_at,
            updated_at=t.updated_at,
            user_id=t.user_id,
        )

    def get_ticket(self, ticket_id: uuid.UUID) -> TicketRead:
        t = self.repo.get(ticket_id)
        if not t:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        return TicketRead(
            id=t.id,
            title=t.title,
            description=t.description,
            status=t.status,
            created_at=t.created_at,
            updated_at=t.updated_at,
            user_id=t.user_id,
        )
