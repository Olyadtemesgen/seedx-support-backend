from .service import AIService


def get_ai_service() -> AIService:
    """
    Dependency to provide a singleton AIService instance.
    """
    return AIService()