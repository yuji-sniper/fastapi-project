from abc import ABC, abstractmethod
from fastapi import Request

from app.models.user import User
from app.schemas.user import UserInput


class AuthServiceInterface(ABC):
    
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        '''
        Verify a password.
        '''
        pass
    
    
    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        '''
        Get a password hash.
        '''
        pass
    
    
    @abstractmethod
    def register_user(self, user_input: UserInput) -> User:
        '''
        Register a user.
        '''
        pass
    
    
    @abstractmethod
    def authenticate_user(self, user_input: UserInput) -> User:
        '''
        Authenticate a user.
        '''
        pass
    
    
    @abstractmethod
    def get_auth_username_from_redis(
        self,
        api_token: str) -> str:
        '''
        Get an auth user id.
        '''
        pass
    
    
    @abstractmethod
    def generate_api_token(self) -> str:
        '''
        Generate an API token.
        '''
        pass
    
    
    @abstractmethod
    def store_auth_username_in_redis(
        self,
        username: str,
        api_token: str):
        '''
        Store an auth user id in the redis.
        '''
        pass
    
    
    @abstractmethod
    def delete_auth_username_from_redis(
        self,
        api_token: str):
        '''
        Delete an auth user id from the redis.
        '''
        pass
    
    
    @abstractmethod
    def get_key_for_auth_username(self, api_token: str) -> str:
        '''
        Get a key for an auth user id.
        '''
        pass
    
    
    @abstractmethod
    def get_auth_user(self, request: Request) -> User:
        '''
        Get an auth user.
        '''
        pass
