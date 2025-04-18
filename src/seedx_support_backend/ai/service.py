import httpx
from typing import AsyncIterator, List
from datetime import datetime
from uuid import UUID

from src.config import settings
from ..tickets.core import TicketRead
from ..messages.core import MessageRead

class AIService:
    """
    Handles streaming AI responses via Groq API.
    """
    def __init__(self, api_key: str = settings.GROK_API_KEY, base_url: str = settings.GROK_API_URL):
        self.api_key = api_key
        self.base_url = base_url

    async def stream_chat_response(
        self,
        ticket: TicketRead,
        message_history: List[MessageRead],
    ) -> AsyncIterator[str]:
        # Build the prompt
        prompt_lines = [
            "You are a helpful customer support assistant.",
            f"Ticket Title: {ticket.title}",
            f"Description: {ticket.description}",
            "Conversation so far:"
        ]
        for msg in message_history:
            role = "AI" if msg.is_ai else "User"
            prompt_lines.append(f"{role}: {msg.content}")
        prompt_lines.append("AI:")
        prompt = "\n".join(prompt_lines)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {"prompt": prompt, "stream": True}

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", self.base_url, headers=headers, json=body) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    if line.startswith("data:"):
                        data = line.removeprefix("data:").strip()
                        if data == "[DONE]":
                            break
                        yield data
                    else:
                        yield line
