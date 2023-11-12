from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect

from app.api.v1.router import api_router as v1_router
from app.api.v2.router import api_router as v2_router
from app.dependencies.db.db_container import DbContainer
from app.dependencies.repositories.todo_repository_container import TodoRepositoryContainer
from app.dependencies.repositories.user_repository_container import UserRepositoryContainer
from app.dependencies.services.auth_service_container import AuthServiceContainer
from app.dependencies.redis.redis_container import RedisContainer
from app.exceptions.handler import setup_exception_handlers
from app.middleware.auth.verify_csrf_middleware import VerifyCsrfMiddleware
from app.schemas.csrf import CsrfSettings


app = FastAPI()


db_container = DbContainer()
redis_container = RedisContainer()
auth_service_container = AuthServiceContainer()
todo_repository_container = TodoRepositoryContainer()
user_repository_container = UserRepositoryContainer()

wire_modules = [
    "app.api.v1.endpoints.auth",
    "app.api.v1.endpoints.todo",
]
db_container.wire(modules=wire_modules)
redis_container.wire(modules=wire_modules)
auth_service_container.wire(modules=wire_modules)
todo_repository_container.wire(modules=wire_modules)
user_repository_container.wire(modules=wire_modules)


app.include_router(v1_router, prefix="/v1")
app.include_router(v2_router, prefix="/v2")


setup_exception_handlers(app)


app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000'],
                   allow_credentials=True,
                   allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE"],
                   allow_headers=["*"])
app.add_middleware(VerifyCsrfMiddleware)


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()
