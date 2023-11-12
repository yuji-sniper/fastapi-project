from dependency_injector import containers, providers

from app.db.session import get_db


class DbContainer(containers.DeclarativeContainer):
    
    db = providers.Resource(get_db)
