from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.repositories.todo.todo_repository_interface import TodoRepositoryInterface
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoRepository(TodoRepositoryInterface):
    
    def __init__(self, db: Session):
        self.db = db
    
    
    def get_all(self) -> List[Todo]:
        return self.db.query(Todo).all()
    
    
    def get_by_user_id(self, user_id: int) -> List[Todo]:
        return self.db.query(Todo).filter(Todo.user_id == user_id).all()


    def create(self, todo_create: TodoCreate) -> Todo:
        todo = Todo(
            user_id=todo_create.user_id,
            title=todo_create.title,
            description=todo_create.description
        )
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    
    def update(self, todo_update: TodoUpdate) -> Todo:
        todo = self.db.query(Todo).filter(Todo.id == todo_update.id, Todo.user_id == todo_update.user_id).first()
        
        if not todo:
            raise HTTPException(
                status_code=404,
                detail="Todo not found"
            )
        
        todo.title = todo_update.title
        todo.description = todo_update.description
        self.db.commit()
        self.db.refresh(todo)
        return todo
    

    def delete(self, id: int, user_id: int) -> None:
        todo = self.db.query(Todo).filter(Todo.id == id, Todo.user_id == user_id).first()
        
        if not todo:
            raise HTTPException(
                status_code=404,
                detail="Todo not found"
            )
        
        self.db.delete(todo)
        self.db.commit()
