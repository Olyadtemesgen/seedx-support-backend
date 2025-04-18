from sqlalchemy.orm import Session
from src.seedx_support_backend.infrastructure.repository import RepositoryInterface
from .models import Message
import uuid

class MessageRepository(RepositoryInterface[Message]):
    def __init__(self, db: Session):
        super().__init__(Message, db)

    def list_by_ticket(self, ticket_id: uuid.UUID):
        return self.db.query(self.model).filter(Message.ticket_id == ticket_id).order_by(Message.created_at).all()
