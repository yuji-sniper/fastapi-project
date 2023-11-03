from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.schemas.todo import TodoInput


class TodoRepository:
    
    db: Session
    
    
    def __init__(self, db: Session):
        self.db = db
    
    
    def get_all(self) -> List[Todo]:
        '''
        Get all todos.
        '''
        return self.db.query(Todo).all()


    def create(self, todo_input: TodoInput) -> Todo:
        '''
        Create a todo.
        '''
        todo = Todo(
            title=todo_input.title,
            description=todo_input.description
        )
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    
    def update(self, id: int, todo_input: TodoInput) -> Todo:
        '''
        Update a todo by id.
        '''
        todo = self.db.query(Todo).get(id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo.title = todo_input.title
        todo.description = todo_input.description
        self.db.commit()
        self.db.refresh(todo)
        return todo
    

    def delete(self, id: int) -> None:
        '''
        Delete a todo by id.
        '''
        todo = self.db.query(Todo).get(id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        self.db.delete(todo)
        self.db.commit()
