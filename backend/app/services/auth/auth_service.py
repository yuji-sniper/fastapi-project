from datetime import datetime, timedelta

from decouple import config
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user.user_repository import UserRepository
from app.schemas.user import UserInput
from app.services.auth.auth_service_interface import AuthServiceInterface


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AuthService(AuthServiceInterface):
    
    SECRET_KEY = config("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 5
    
    
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
    
    
    def create_access_token(self, user: User):
        '''
        Create an access token.
        '''
        claims = {"sub": user.username}
        
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        claims.update({"exp": expire})
        
        token = jwt.encode(claims, self.SECRET_KEY, algorithm=self.ALGORITHM)
        
        return token
    
    
    def decode_access_token(self, token: str = Depends(oauth2_scheme)):
        '''
        Decode an access token.
        '''
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
    
    
    def get_current_user(self, db: Session, token: str = Depends(oauth2_scheme)):
        '''
        Get the current user.
        '''
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
        user_repository = UserRepository(db)
        
        try:
            payload = self.decode_access_token(token)
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except  JWTError:
            raise credentials_exception
        
        user = user_repository.find_by_username(username)
        
        if user is None:
            raise credentials_exception
        
        return user
