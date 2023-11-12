from dependency_injector.wiring import inject, Provide
from fastapi import Request, Depends

from app.dependencies.services.auth_service_container import AuthServiceContainer
from app.models.user import User
from app.services.auth.auth_service_interface import AuthServiceInterface


@inject
async def get_auth_user(
    request: Request,
    auth_service: AuthServiceInterface = Depends(Provide[AuthServiceContainer.auth_service])
) -> User:
    '''
    Get an auth user.
    '''
    return await auth_service.get_auth_user(request)
