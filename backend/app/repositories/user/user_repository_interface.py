from abc import ABC, abstractmethod

from app.models.user import User
from app.schemas.user import UserInput


class UserRepositoryInterface(ABC):
    
    @abstractmethod
    def find_by_username(self, username: str) -> User:
        '''
        Find a user by username.
        '''
        pass
    
    @abstractmethod
    def create(self, user_input: UserInput) -> User:
        '''
        Create a user.
        '''
        pass
