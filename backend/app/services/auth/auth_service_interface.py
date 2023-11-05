from abc import ABC, abstractmethod

from fastapi import Request

from app.models.user import User


class AuthServiceInterface(ABC):
    
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str):
        '''
        Verify a password.
        '''
        pass
    
    @abstractmethod
    def get_password_hash(self, password):
        '''
        Get a password hash.
        '''
        pass
    
    @abstractmethod
    def register_user(self, user_input, db) -> User:
        '''
        Register a user.
        '''
        pass
    
    @abstractmethod
    def authenticate_user(self, user_input, db) -> User:
        '''
        Authenticate a user.
        '''
        pass
    
    
    @abstractmethod
    def create_access_token(self, user: User) -> str:
        '''
        Create an access token.
        '''
        pass
    
    
    @abstractmethod
    def decode_access_token(self, request: Request) -> str:
        '''
        Get an access token.
        '''
        pass
    
    
    @abstractmethod
    def get_auth_user(self, db, request: Request) -> User:
        '''
        Verify an access token.
        '''
        pass
