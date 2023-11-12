from dependency_injector import containers, providers

from app.dependencies.repositories.user_repository_container import UserRepositoryContainer
from app.dependencies.session.redis_container import RedisContainer
from app.services.auth.auth_service import AuthService


class AuthServiceContainer(containers.DeclarativeContainer):
    redis_container = providers.Container(RedisContainer)
    user_repository_container = providers.Container(UserRepositoryContainer)
    
    auth_service = providers.Factory(
        AuthService,
        redis=redis_container.redis_pool,
        user_repository=user_repository_container.user_repository
    )
