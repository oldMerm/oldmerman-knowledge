from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import routes
from config import Settings, get_settings
from utils.logger import get_logger
from middleware import AuthMiddleware
from middleware.response_handler import ResponseWrapperMiddleware
from middleware.exception_handler import register_exception_handlers
from common.Result import Result
import uvicorn

logger = get_logger("main")

settings = get_settings()
app = FastAPI()

# register routers
app.include_router(routes.login_router)
app.include_router(routes.user_router)
app.include_router(routes.model_group_router)
app.include_router(routes.model_router)
app.include_router(routes.model_type_router)
app.include_router(routes.vector_manage_router)

# register middleware
app.add_middleware(ResponseWrapperMiddleware)
app.add_middleware(AuthMiddleware)
register_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


logger.info("Application started")


@app.get("/")
async def root():
    return Result.success(data={"message": "Hello World"})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_config=None
    )
