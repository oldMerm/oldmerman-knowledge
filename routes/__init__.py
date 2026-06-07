from .auth import router as login_router
from .user import router as user_router
from .model import router as model_router
from .model_group import router as model_group_router
from .model_type import router as model_type_router
from .vector_manage import router as vector_manage_router
from .api_simple_agent import router as api_simple_agent_router

__all__ = ["login_router",
           "user_router",
           "model_router", "model_group_router", "model_type_router",
           "vector_manage_router",
           "api_simple_agent_router"]
