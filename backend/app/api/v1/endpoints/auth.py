import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi_csrf_protect import CsrfProtect
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth.auth_dependencies import get_auth_user
from app.models.user import User
from app.schemas.common import Ok
from app.schemas.csrf import Csrf
from app.schemas.user import UserInput, UserOutput
from app.services.auth.auth_service import AuthService


router = APIRouter()

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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


@router.post("/login", response_model=Ok)
def login(response: Response, user_input: UserInput, db: Session = Depends(get_db)):
    '''
    Login a user.
    '''
    auth_service = AuthService()
    
    user = auth_service.authenticate_user(db, user_input)
    
    token = auth_service.create_access_token(user)
    
    response.set_cookie(
        key="access_token", value=f'Bearer {token}', httponly=True, samesite="lax", secure=False)
    
    return Ok(message="Successfully logged in")


@router.post("/logout", response_model=Ok)
def logout(response: Response):
    '''
    Logout a user.
    '''
    response.delete_cookie(key="access_token")
    
    return Ok(message="Successfully logged out")


@router.get("/me", response_model=UserOutput)
def me(auth_user: User = Depends(get_auth_user)):
    '''
    Get the current user.
    '''
    return auth_user
