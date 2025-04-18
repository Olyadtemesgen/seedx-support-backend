from fastapi import HTTPException, status
import uuid
from .repository import MessageRepository
from .core import MessageCreate, MessageRead

class MessageService:
    def __init__(self, repo: MessageRepository):
        self.repo = repo

    def add_message(self, ticket_id: uuid.UUID, author_id: uuid.UUID, msg_in: MessageCreate) -> MessageRead:
        # create record
        db_obj = self.repo.create({
            "content": msg_in.content,
            "is_ai": msg_in.is_ai,
            "ticket_id": ticket_id,
            "author_id": author_id,
        })
        return MessageRead(
            id=db_obj.id,
            content=db_obj.content,
            is_ai=db_obj.is_ai,
            created_at=db_obj.created_at,
            ticket_id=db_obj.ticket_id,
            author_id=db_obj.author_id,
        )

    def list_messages(self, ticket_id: uuid.UUID) -> list[MessageRead]:
        objs = self.repo.list_by_ticket(ticket_id)
        return [MessageRead(
            id=o.id,
            content=o.content,
            is_ai=o.is_ai,
            created_at=o.created_at,
            ticket_id=o.ticket_id,
            author_id=o.author_id,
        ) for o in objs]
