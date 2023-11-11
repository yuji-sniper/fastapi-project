import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_csrf_protect import CsrfProtect
from sqlalchemy.orm import Session
from redis import Redis

from app.config.redis_config import get_redis
from app.db.session import get_db
from app.dependencies.auth.auth_dependencies import get_auth_user
from app.models.user import User
from app.schemas.common import Ok
from app.schemas.csrf import Csrf
from app.schemas.user import UserInput, UserOutput
from app.services.auth.auth_service import AuthService
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
def register(user_input: UserInput, db: Session = Depends(get_db)):
    '''
    Register a user.
    '''
    auth_service = AuthService()
    
    try:
        return auth_service.register_user(user_input, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        logger.error(f"Error registering user: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error")


@router.post("/login")
def login(request: Request,
          user_input: UserInput,
          db: Session = Depends(get_db),
          session: Redis = Depends(get_redis)):
    '''
    Login a user.
    '''
    auth_service = AuthService()
    
    user = auth_service.authenticate_user(db, user_input)
    
    old_api_token = get_request_token(request)
    
    if old_api_token:
        auth_service.delete_auth_username_from_session(old_api_token, session)
    
    new_api_token = auth_service.generate_api_token(session)
    
    auth_service.store_auth_username_in_session(user.username, new_api_token, session)
    
    return {"token": new_api_token}


@router.post("/logout", response_model=Ok)
def logout(request: Request,
           session: Redis = Depends(get_redis)):
    '''
    Logout a user.
    '''
    token = get_request_token(request)
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    auth_service = AuthService()
    
    auth_service.delete_auth_username_from_session(token, session)
    
    return Ok(message="Successfully logged out")


@router.get("/me", response_model=UserOutput)
def me(auth_user: User = Depends(get_auth_user)):
    '''
    Get the current user.
    '''
    return auth_user
