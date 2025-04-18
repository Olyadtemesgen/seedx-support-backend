# src/app.py
from fastapi import FastAPI

# point at your package’s middleware
from middleware import setup_middlewares

# import the routers (they’re all defined as `router = APIRouter(prefix=...)` in their modules)
from seedx_support_backend.users.resource    import router as auth_router
from seedx_support_backend.tickets.resource  import router as tickets_router
from seedx_support_backend.messages.resource import router as messages_router
from seedx_support_backend.ai.resource       import router as ai_response_router


def create_app() -> FastAPI:
    app = FastAPI(title="Support Assistant API")

    # CORS + auth
    setup_middlewares(app)

    # each router already has its own prefix:
    #   auth_router    → /auth
    #   tickets_router → /tickets
    #   messages_router→ /tickets/{ticket_id}/messages
    #   ai_response_router → /tickets/{ticket_id}/ai-response
    app.include_router(auth_router)
    app.include_router(tickets_router)
    app.include_router(messages_router)
    app.include_router(ai_response_router)

    return app
app = create_app()
