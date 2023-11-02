import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoOut



router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", response_model=List[TodoOut])
def get(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos


@router.post("/", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create(todo_create: TodoCreate, db: Session = Depends(get_db)):
    todo = Todo(
        title=todo_create.title,
        description=todo_create.description
    )
    db.add(todo)
    
    try:
        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
