from fastapi import Request, Response, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.services.auth.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

auth_service = AuthService()


def get_auth_user(
    request: Request, response: Response, db: Session = Depends(get_db)) -> User:
    '''
    Get the current user.
    '''
    try:
        user = auth_service.verify_access_token(db, request)
        
        new_access_token = auth_service.create_access_token(user)
        
        response.set_cookie(
            key="access_token", value=f'Bearer {new_access_token}', httponly=True, samesite="lax", secure=False)
        
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
