from .user import user_router
from .mail import mail_router
from .auth import auth_router
from .work_type import work_type_router
from .service import service_router
from .category import category_router
from .appointment import appointment_router
from .statistic import statistic_router

__all__ = ["user_router", "mail_router", "auth_router", "work_type_router", "service_router", "category_router", "appointment_router", "statistic_router"]
