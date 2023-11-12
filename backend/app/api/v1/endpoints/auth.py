import logging
import sys

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_csrf_protect import CsrfProtect
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth.auth_dependencies import get_auth_user
from app.dependencies.services.auth_service_container import AuthServiceContainer
from app.models.user import User
from app.schemas.common import Ok
from app.schemas.csrf import Csrf
from app.schemas.token import TokenOutput
from app.schemas.user import UserInput, UserOutput
from app.services.auth.auth_service import AuthService
from app.services.auth.auth_service_interface import AuthServiceInterface
from app.utils.auth_util import get_request_token


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/csrf", response_model=Csrf)
def get_csrf_token(response: Response, csrf_protect: CsrfProtect = Depends()):
    '''
    Get a CSRF token.
    '''
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    
    csrf_protect.set_csrf_cookie(signed_token, response)
    
    return Csrf(csrf_token=csrf_token)


@router.post("/register")
@inject
def register(user_input: UserInput,
             db: Session = Depends(get_db),
             auth_service: AuthServiceInterface = Depends(Provide[AuthServiceContainer.auth_service])):
    '''
    Register a user.
    '''
    try:
        user = auth_service.register_user(user_input)
        
        return UserOutput(id=user.id, username=user.username)
    except Exception as e:
        db.rollback()
        
        logger.error(f"Error registering user: {e}", exc_info=True)
        
        raise HTTPException(status_code=500, detail=f"Internal Server Error")


@router.post("/login", response_model=TokenOutput)
@inject
async def login(request: Request,
          user_input: UserInput,
          auth_service: AuthServiceInterface = Depends(Provide[AuthServiceContainer.auth_service])):
    '''
    Login a user.
    '''    
    user = auth_service.authenticate_user(user_input)
    
    old_api_token = get_request_token(request)
    
    if old_api_token:
        await auth_service.delete_auth_username_from_redis(old_api_token)
    
    new_api_token = await auth_service.generate_api_token()
    
    await auth_service.store_auth_username_in_redis(user.username, new_api_token)
    
    return TokenOutput(token=new_api_token)


@router.post("/logout", response_model=Ok)
@inject
async def logout(request: Request,
           auth_user: User = Depends(get_auth_user),
           auth_service: AuthServiceInterface = Depends(Provide[AuthServiceContainer.auth_service])):
    '''
    Logout a user.
    '''
    token = get_request_token(request)
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    await auth_service.delete_auth_username_from_redis(token)
    
    return Ok(message="Successfully logged out")


@router.get("/me", response_model=UserOutput)
@inject
async def me(
    request: Request,
    auth_user: User = Depends(get_auth_user),
    auth_service: AuthServiceInterface = Depends(Provide[AuthServiceContainer.auth_service])):
    '''
    Get the current user.
    '''
    return auth_user
