import uuid
from sqlalchemy.orm import Session
from src.seedx_support_backend.infrastructure.repository import RepositoryInterface
from .models import Ticket

class TicketRepository(RepositoryInterface[Ticket]):
    def __init__(self, db: Session):
        super().__init__(Ticket, db)

    def list_by_user(self, user_id: uuid.UUID) -> list[Ticket]:
        return self.db.query(self.model).filter(Ticket.user_id == user_id).all()
