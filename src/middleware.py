# src/middleware.py

from typing import Callable

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings
from seedx_support_backend.infrastructure.database import get_db
from seedx_support_backend.users.repository import UserRepository
from seedx_support_backend.users.service import UserService
from seedx_support_backend.users.models import User


# --- CORS setup -------------------------------------------------------------

def setup_cors(app: FastAPI):
    """
    Apply CORS middleware to the FastAPI app.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# --- Authentication middleware ---------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts a Bearer token, validates it, and attaches the User
    object to request.state.user.  Skips auth for login/signup/docs paths.
    """
    def __init__(self, app: FastAPI, user_svc: UserService):
        super().__init__(app)
        self.user_svc = user_svc

    async def dispatch(self, request: Request, call_next: Callable):
        # Skip authentication for open endpoints
        open_paths = ["/auth/signup", "/auth/login", "/openapi.json", "/docs", "/docs/oauth2-redirect"]
        if any(request.url.path.startswith(p) for p in open_paths):
            return await call_next(request)

        # Extract and validate Bearer token
        auth: str | None = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
        token = auth.split(" ", 1)[1]

        try:
            user = self.user_svc.validate_token(token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Attach user to request state
        request.state.user = user
        return await call_next(request)


# --- Combined middleware setup ---------------------------------------------

def setup_middlewares(app: FastAPI):
    """
    Call this in your main.py after creating FastAPI() to wire up CORS and Auth.
    Usage:
      from seedx_support_backend.middleware import setup_middlewares
      setup_middlewares(app)
    You must also have created a UserService instance and stored it on app.state.user_service.
    """
    # 1) Apply CORS
    setup_cors(app)

    # 2) Ensure UserService is available
    if not hasattr(app.state, "user_service"):
        # Construct a UserService from a fresh DB session
        db = next(get_db())
        repo = UserRepository(db)
        svc = UserService(
            repo=repo,
            jwt_secret=settings.JWT_SECRET,
            expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        app.state.user_service = svc

    # 3) Add AuthMiddleware
    app.add_middleware(AuthMiddleware, user_svc=app.state.user_service)


# --- Dependencies ----------------------------------------------------------

def get_current_user(request: Request) -> User:
    """
    Dependency to retrieve the current authenticated user (from middleware).
    """
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


def require_role(required_role: str):
    """
    Dependency factory to enforce that the current user has a specific role.

    Usage:
      @router.get("/admin-only")
      def admin_endpoint(current: User = Depends(require_role("admin"))):
          ...
    """
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.value != required_role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user

    return Depends(checker)
