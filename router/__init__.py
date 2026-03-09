from .user import user_router
from .mail import mail_router
from .auth import auth_router


__all__ = [user_router, mail_router, auth_router]