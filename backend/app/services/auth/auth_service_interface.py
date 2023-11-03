from abc import ABC, abstractmethod

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
    def create_access_token(self, user: User):
        '''
        Create an access token.
        '''
        pass
    
    
    @abstractmethod
    def decode_access_token(self, token: str):
        '''
        Decode an access token.
        '''
        pass
    
    
    @abstractmethod
    def get_current_user(self, token: str, db) -> User:
        '''
        Get the current user.
        '''
        pass
