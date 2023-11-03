from abc import ABC, abstractmethod
from typing import List

from app.models.todo import Todo


class TodoRepositoryInterface(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Todo]:
        '''
        Get all todos.
        '''
        pass

    @abstractmethod
    def create(self, todo) -> Todo:
        '''
        Create a todo.
        '''
        pass

    @abstractmethod
    def update(self, id, todo) -> Todo:
        '''
        Update a todo by id.
        '''
        pass

    @abstractmethod
    def delete(self, id) -> None:
        '''
        Delete a todo by id.
        '''
        pass
