import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.token import TokenOutput
from app.schemas.user import UserInput, UserOutput
from app.services.auth.auth_service import AuthService


router = APIRouter()

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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


@router.post("/login", response_model=TokenOutput)
def login(user_input: UserInput, db: Session = Depends(get_db)):
    '''
    Login a user.
    '''
    auth_service = AuthService()
    
    user = auth_service.authenticate_user(db, user_input)
    
    token = auth_service.create_access_token(user)
    
    return TokenOutput(token_type="access_token", token=token)


@router.get("/me", response_model=UserOutput)
def me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    '''
    Get the current user.
    '''
    auth_service = AuthService()

    try:
        user = auth_service.get_current_user(db, token)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting current user: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error")
