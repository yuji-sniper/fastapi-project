from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from redis import Redis

from app.config.redis_config import get_redis
from app.db.session import get_db
from app.models.user import User
from app.repositories.user.user_repository import UserRepository
from app.services.auth.auth_service import AuthService
from app.utils.auth_util import get_request_token


def get_auth_user(
    request: Request,
    db: Session = Depends(get_db),
    session: Redis = Depends(get_redis)) -> User:
    '''
    Get the current user.
    '''
    token = get_request_token(request)
    
    auth_service = AuthService()
    
    auth_username = auth_service.get_auth_username_from_session(token, session)
    
    if not auth_username:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    
    user_repository = UserRepository(db)
    
    auth_user = user_repository.find_by_username(auth_username)
    
    if not auth_user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    
    return auth_user
