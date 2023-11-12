from decouple import config
from dependency_injector import containers, providers

from app.session.redis import init_redis_pool


class RedisContainer(containers.DeclarativeContainer):
    
    redis_pool = providers.Resource(
        init_redis_pool,
        host=config('REDIS_HOST'),
        port=config('REDIS_PORT', cast=int)
    )
