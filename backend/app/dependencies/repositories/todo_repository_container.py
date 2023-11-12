from dependency_injector import containers, providers

from app.dependencies.db.db_container import DbContainer
from app.repositories.todo.todo_repository import TodoRepository


class TodoRepositoryContainer(containers.DeclarativeContainer):
    db_container = providers.Container(DbContainer)
    
    todo_repository = providers.Factory(
        TodoRepository,
        db=db_container.db
    )
