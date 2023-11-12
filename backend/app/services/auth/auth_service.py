from redis.asyncio import Redis
from fastapi import HTTPException, Request
import hashlib
from passlib.context import CryptContext

from app.models.user import User
from app.repositories.user.user_repository import UserRepository
from app.schemas.user import UserInput
from app.services.auth.auth_service_interface import AuthServiceInterface
from app.utils.auth_util import get_request_token
from app.utils.crypt_util import encrypt, decrypt
from app.utils.string_util import random_string


class AuthService(AuthServiceInterface):
    
    AUTH_USERNAME_REDIS_KEY_PREFIX = "auth_user_name:"
    TOKEN_EXPIRE_MINUTES = 5
    
    
    pwd_context: CryptContext
    
    
    def __init__(self,
                 redis: Redis,
                 user_repository: UserRepository):
        self.redis = redis
        self.user_repository = user_repository
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
    
    
    def register_user(self, user_input: UserInput) -> User:
        '''
        Register a user.
        '''        
        overlap_user = self.user_repository.find_by_username(user_input.username)
        
        if overlap_user:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )
        
        hashed_password = self.get_password_hash(user_input.password)
        
        user_input.password = hashed_password
        
        return self.user_repository.create(user_input)
    
    
    def authenticate_user(self, user_input: UserInput) -> User:
        '''
        Authenticate a user.
        '''        
        user = self.user_repository.find_by_username(user_input.username)
        
        if not user:
            return False
        
        if not self.verify_password(user_input.password, user.password):
            return False
        
        return user
    
    
    async def get_auth_username_from_redis(
        self,
        api_token: str) -> str:
        '''
        Get an auth user id.
        '''
        key = self.get_key_for_auth_username(api_token)
        
        encrypt_auth_username = await self.redis.get(key)
        
        if not encrypt_auth_username:
            return None
        
        auth_username = decrypt(encrypt_auth_username)
        
        return auth_username
    
    
    async def generate_api_token(self) -> str:
        '''
        Create an api token.
        '''        
        while True:
            api_token = random_string(40)
            
            key = self.get_key_for_auth_username(api_token)
            
            is_exists =  await self.redis.exists(key)
            
            if not is_exists:
                break
        
        return api_token
    
    
    async def store_auth_username_in_redis(
        self,
        auth_username: int,
        api_token: str):
        '''
        Store an auth user id.
        '''
        key = self.get_key_for_auth_username(api_token)
        
        value = encrypt(str(auth_username))
        
        await self.redis.set(name=key, value=value, ex=self.TOKEN_EXPIRE_MINUTES * 60)
    
    
    async def delete_auth_username_from_redis(
        self,
        api_token: str):
        '''
        Delete an auth user id.
        '''
        api_token_hash = api_token
        
        key = self.get_key_for_auth_username(api_token_hash)
        
        await self.redis.delete(key)
    
    
    def get_key_for_auth_username(self, api_token: str) -> str:
        '''
        Get a key for an auth user id.
        '''
        api_token_hash = hashlib.sha256(api_token.encode()).hexdigest()
        
        return f"{self.AUTH_USERNAME_REDIS_KEY_PREFIX}{api_token_hash}"
    
    
    async def get_auth_user(self, request: Request) -> User:
        '''
        Get an auth user.
        '''
        unauthorized_exception = HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
        
        api_token = get_request_token(request)

        if not api_token:
            raise unauthorized_exception
        
        auth_username = await self.get_auth_username_from_redis(api_token)
        
        if not auth_username:
            raise unauthorized_exception
        
        auth_user = self.user_repository.find_by_username(auth_username)
        
        if not auth_user:
            raise unauthorized_exception
        
        return auth_user
