from dependency_injector import containers, providers

from app.dependencies.db.db_container import DbContainer
from app.repositories.user.user_repository import UserRepository


class UserRepositoryContainer(containers.DeclarativeContainer):
    db_container = providers.Container(DbContainer)
    
    user_repository = providers.Factory(
        UserRepository,
        db=db_container.db
    )
