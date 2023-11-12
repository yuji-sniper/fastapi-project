import logging
from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth.auth_dependencies import get_auth_user
from app.dependencies.repositories.todo_repository_container import TodoRepositoryContainer
from app.repositories.todo.todo_repository_interface import TodoRepositoryInterface
from app.schemas.todo import TodoInput, TodoOutput, TodoCreate, TodoUpdate


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("", response_model=List[TodoOutput])
@inject
def get(auth_user = Depends(get_auth_user),
        todo_repository: TodoRepositoryInterface = Depends(Provide[TodoRepositoryContainer.todo_repository])):
    '''
    Get all todos.
    '''
    todos = todo_repository.get_by_user_id(auth_user.id)
    
    return todos


@router.post("", response_model=TodoOutput)
@inject
def create(todo_input: TodoInput,
           auth_user = Depends(get_auth_user),
           todo_repository: TodoRepositoryInterface = Depends(Provide[TodoRepositoryContainer.todo_repository])):
    '''
    Create a todo.
    '''
    todo_create = TodoCreate(
        user_id=auth_user.id,
        title=todo_input.title,
        description=todo_input.description
    )
    
    try:
        return todo_repository.create(todo_create)
    except Exception as e:
        logger.error(f"Error creating todo: {e}", exc_info=True)
        
        raise HTTPException(status_code=500, detail=f"Internal Server Error")


@router.put("/{id}", response_model=TodoOutput)
@inject
def update(id: int,
           todo_input: TodoInput,
           auth_user = Depends(get_auth_user),
           todo_repository: TodoRepositoryInterface = Depends(Provide[TodoRepositoryContainer.todo_repository])):
    '''
    Update a todo by id.
    '''
    todo_update = TodoUpdate(
        id=id,
        user_id=auth_user.id,
        title=todo_input.title,
        description=todo_input.description
    )
    
    try:
        return todo_repository.update(todo_update)
    except Exception as e:
        logger.error(f"Error updating todo: {e}", exc_info=True)
        
        raise HTTPException(status_code=500, detail=f"Internal Server Error")


@router.delete("/{id}")
@inject
def delete(id: int,
           auth_user = Depends(get_auth_user),
           todo_repository: TodoRepositoryInterface = Depends(Provide[TodoRepositoryContainer.todo_repository])):
    '''
    Delete a todo by id.
    '''
    try:
        todo_repository.delete(id, auth_user.id)
        
        return {"message": "Todo deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting todo: {e}", exc_info=True)
        
        raise HTTPException(status_code=500, detail=f"Internal Server Error")
