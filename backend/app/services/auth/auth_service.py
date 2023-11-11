from decouple import config
import hashlib
from passlib.context import CryptContext
from redis import Redis
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user.user_repository import UserRepository
from app.schemas.user import UserInput
from app.services.auth.auth_service_interface import AuthServiceInterface
from app.utils.string_util import random_string
from app.utils.crypt_util import encrypt, decrypt


class AuthService(AuthServiceInterface):
    
    SECRET_KEY = config("SECRET_KEY")
    AUTH_USERNAME_SESSION_KEY_PREFIX = "auth_user_name:"
    ALGORITHM = "HS256"
    TOKEN_EXPIRE_MINUTES = 5
    
    
    pwd_context: CryptContext
    
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        '''
        Verify a password.
        '''
        return self.pwd_context.verify(plain_password, hashed_password)
    
    
    def get_password_hash(self, password: str) -> str:
        '''
        Get a password hash.
        '''
        return self.pwd_context.hash(password)
    
    
    def register_user(self, user_input: UserInput, db: Session) -> User:
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
    
    
    def authenticate_user(
        self,
        db: Session,
        user_input: UserInput) -> User:
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
    
    
    def get_auth_username_from_session(
        self,
        api_token: str,
        session: Redis) -> str:
        '''
        Get an auth user id.
        '''
        key = self.get_key_for_auth_username(api_token)
        
        encrypt_auth_username = session.get(key)
        
        if not encrypt_auth_username:
            return None
        
        auth_username = decrypt(encrypt_auth_username)
        
        return auth_username
    
    
    def generate_api_token(self, session: Redis) -> str:
        '''
        Create an api token.
        '''        
        while True:
            api_token = random_string(40)
            
            key = self.get_key_for_auth_username(api_token)
            
            if not session.exists(key):
                break
        
        return api_token
    
    
    def store_auth_username_in_session(
        self,
        auth_username: int,
        api_token: str,
        session: Redis):
        '''
        Store an auth user id.
        '''
        key = self.get_key_for_auth_username(api_token)
        
        value = encrypt(str(auth_username))
                
        session.set(name=key, value=value, ex=self.TOKEN_EXPIRE_MINUTES * 60)
    
    
    def delete_auth_username_from_session(
        self,
        api_token: str,
        session: Redis):
        '''
        Delete an auth user id.
        '''
        api_token_hash = api_token
        
        key = self.get_key_for_auth_username(api_token_hash)
        
        session.delete(key)
    
    
    def get_key_for_auth_username(self, api_token: str) -> str:
        '''
        Get a key for an auth user id.
        '''
        api_token_hash = hashlib.sha256(api_token.encode()).hexdigest()
        
        return f"{self.AUTH_USERNAME_SESSION_KEY_PREFIX}{api_token_hash}"
