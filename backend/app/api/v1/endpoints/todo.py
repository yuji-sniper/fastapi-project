import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.todo.todo_repository import TodoRepository
from app.schemas.todo import TodoInput, TodoOut


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", response_model=List[TodoOut])
def get(db: Session = Depends(get_db)):
    '''
    Get all todos.
    '''
    todo_repository = TodoRepository(db)
    todos = todo_repository.get_all()
    
    return todos


@router.post("/", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create(todo_input: TodoInput, db: Session = Depends(get_db)):
    '''
    Create a todo.
    '''
    todo_repository = TodoRepository(db)
    
    try:
        return todo_repository.create(todo_input)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error")


@router.put("/{id}", response_model=TodoOut)
def update(id: int, todo_input: TodoInput, db: Session = Depends(get_db)):
    '''
    Update a todo by id.
    '''
    todo_repository = TodoRepository(db)
    
    try:
        return todo_repository.update(id, todo_input)
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error")


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    '''
    Delete a todo by id.
    '''
    todo_repository = TodoRepository(db)
    
    try:
        todo_repository.delete(id)
        return {"message": "Todo deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error")
