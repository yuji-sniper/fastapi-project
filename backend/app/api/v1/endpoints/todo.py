import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth.auth_dependencies import get_auth_user
from app.repositories.todo.todo_repository import TodoRepository
from app.schemas.todo import TodoInput, TodoOutput, TodoCreate, TodoUpdate


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", response_model=List[TodoOutput])
def get(auth_user = Depends(get_auth_user),
        db: Session = Depends(get_db)):
    '''
    Get all todos.
    '''
    todo_repository = TodoRepository(db)
    todos = todo_repository.get_by_user_id(auth_user.id)
    
    return todos


@router.post("/", response_model=TodoOutput)
def create(todo_input: TodoInput,
           auth_user = Depends(get_auth_user),
           db: Session = Depends(get_db)):
    '''
    Create a todo.
    '''
    todo_repository = TodoRepository(db)
    
    todo_create = TodoCreate(
        user_id=auth_user.id,
        title=todo_input.title,
        description=todo_input.description
    )
    
    try:
        return todo_repository.create(todo_create)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error")


@router.put("/{id}", response_model=TodoOutput)
def update(id: int,
           todo_input: TodoInput,
           auth_user = Depends(get_auth_user),
           db: Session = Depends(get_db)):
    '''
    Update a todo by id.
    '''
    todo_repository = TodoRepository(db)
    
    todo_update = TodoUpdate(
        id=id,
        user_id=auth_user.id,
        title=todo_input.title,
        description=todo_input.description
    )
    
    try:
        return todo_repository.update(todo_update)
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error")


@router.delete("/{id}")
def delete(id: int,
           auth_user = Depends(get_auth_user),
           db: Session = Depends(get_db)):
    '''
    Delete a todo by id.
    '''
    todo_repository = TodoRepository(db)
    
    try:
        todo_repository.delete(id, auth_user.id)
        return {"message": "Todo deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error")
