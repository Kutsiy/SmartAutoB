from .user import user_router
from .mail import mail_router
from .auth import auth_router
from .catalog import catalog_router
from .service import service_router

__all__ = [user_router, mail_router, auth_router, catalog_router, service_router]