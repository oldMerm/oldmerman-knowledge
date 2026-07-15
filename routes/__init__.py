from .auth import router as login_router
from .user import router as user_router
from .model import router as model_router
from .log import router as log_router
from .model_group import router as model_group_router
from .model_type import router as model_type_router
from .vector_manage import router as vector_manage_router
from .api import router as api_simple_agent_router
from .document_manage import router as document_router
from .chat import router as chat_router
from .system_config import router as system_config_router

__all__ = ["login_router",
           "user_router",
           "model_router", "model_group_router", "model_type_router",
           "log_router",
           "vector_manage_router",
           "api_simple_agent_router",
           "document_router",
           "chat_router",
           "system_config_router"]
