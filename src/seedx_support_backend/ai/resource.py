from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
import json
from uuid import UUID
from typing import AsyncIterator

from ..infrastructure.database import get_db
from src.middleware import get_current_user
from ..tickets.repository import TicketRepository
from ..tickets.service import TicketService
from ..messages.repository import MessageRepository
from ..messages.service import MessageService
from .dependencies import get_ai_service
from .service import AIService

router = APIRouter(prefix="/tickets/{ticket_id}/ai-response", tags=["ai"])

async def ai_event_generator(
    ticket_id: UUID,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    ai_svc: AIService = Depends(get_ai_service),
) -> AsyncIterator[str]:
    # Verify ticket ownership
    ticket_repo = TicketRepository(db)
    ticket_svc = TicketService(ticket_repo)
    ticket = ticket_svc.get_ticket(ticket_id)
    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Fetch message history
    msg_repo = MessageRepository(db)
    msg_svc = MessageService(msg_repo)
    history = msg_svc.list_messages(ticket_id)

    # Stream AI chunks as SSE
    async for chunk in ai_svc.stream_chat_response(ticket, history):
        payload = {"content": chunk}
        yield f"data: {json.dumps(payload)}\n\n"

@router.get("", response_model=None)
async def stream_ai(
    ticket_id: UUID,
    event_stream: AsyncIterator[str] = Depends(ai_event_generator),
):
    """
    SSE endpoint that streams AI-generated responses for a given ticket.
    """
    return StreamingResponse(event_stream, media_type="text/event-stream")
