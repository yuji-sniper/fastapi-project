from fastapi import APIRouter
from .endpoints import auth
# from .endpoints import auth, todo


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["v1: auth"])
# api_router.include_router(todo.router, prefix="/todo", tags=["v1: todo"])
