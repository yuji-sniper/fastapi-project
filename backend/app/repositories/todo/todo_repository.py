from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.repositories.todo.todo_repository_interface import TodoRepositoryInterface
from app.schemas.todo import TodoInput


class TodoRepository(TodoRepositoryInterface):
    
    db: Session
    
    
    def __init__(self, db: Session):
        self.db = db
    
    
    def get_all(self) -> List[Todo]:
        return self.db.query(Todo).all()


    def create(self, todo_input: TodoInput) -> Todo:
        todo = Todo(
            title=todo_input.title,
            description=todo_input.description
        )
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    
    def update(self, id: int, todo_input: TodoInput) -> Todo:
        todo = self.db.query(Todo).get(id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo.title = todo_input.title
        todo.description = todo_input.description
        self.db.commit()
        self.db.refresh(todo)
        return todo
    

    def delete(self, id: int) -> None:
        todo = self.db.query(Todo).get(id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        self.db.delete(todo)
        self.db.commit()
