from datetime import datetime, timedelta

from decouple import config
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_csrf_protect import CsrfProtect
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user.user_repository import UserRepository
from app.schemas.token import AccessTokenData
from app.schemas.user import UserInput
from app.services.auth.auth_service_interface import AuthServiceInterface


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AuthService(AuthServiceInterface):
    
    SECRET_KEY = config("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    
    
    pwd_context: CryptContext
    
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    
    def verify_password(self, plain_password: str, hashed_password: str):
        '''
        Verify a password.
        '''
        return self.pwd_context.verify(plain_password, hashed_password)
    
    
    def get_password_hash(self, password):
        '''
        Get a password hash.
        '''
        return self.pwd_context.hash(password)
    
    
    def register_user(self, user_input: UserInput, db: Session):
        '''
        Register a user.
        '''
        user_repository = UserRepository(db)
        
        overlap_user = user_repository.find_by_username(user_input.username)
        
        if overlap_user:
            return False
        
        hashed_password = self.get_password_hash(user_input.password)
        
        user_input.password = hashed_password
        
        return user_repository.create(user_input)
    
    
    def authenticate_user(self, db: Session, user_input: UserInput):
        '''
        Authenticate a user.
        '''
        user_repository = UserRepository(db)
        
        user = user_repository.find_by_username(user_input.username)
        
        if not user:
            return False
        
        if not self.verify_password(user_input.password, user.password):
            return False
        
        return user
    
    
    def create_access_token(self, user: User) -> str:
        '''
        Create an access token.
        '''
        claims = {"sub": user.username}
        
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        claims.update({"exp": expire})
        
        return jwt.encode(claims, self.SECRET_KEY, algorithm=self.ALGORITHM)
    
    
    def decode_access_token(self, request: Request):
        '''
        Decode an access token.
        '''
        value = request.cookies.get("access_token")
        
        if not value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token is missing",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        _, _, token = value.partition(" ")
        
        try:
            return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    
    def verify_access_token(self, db: Session, request: Request) -> User:
        '''
        Verify an access token.
        '''
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

        payload = self.decode_access_token(request)
        
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = AccessTokenData(username=username)
         
        user_repository = UserRepository(db)
        
        user = user_repository.find_by_username(token_data.username)
        
        if user is None:
            raise credentials_exception
        
        return user
    
    
    def verify_and_update_access_token(self, db: Session, request: Request):
        '''
        Verify and update an access token.
        '''
        user = self.verify_access_token(db, request)
        
        return self.create_access_token(user)
    
    
    def create_csrf_token(self, response: Response, csrf_protect: CsrfProtect):
        '''
        Create a CSRF token.
        '''
        csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
        
        csrf_protect.set_csrf_cookie(response, signed_token)
        
        return csrf_token
