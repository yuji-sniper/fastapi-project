from typing import AsyncIterable

from redis.asyncio import Redis, from_url


async def init_redis_pool(host: str, port: int) -> AsyncIterable[Redis]:
    redis = await from_url(
        f'redis://{host}:{port}',
        encoding='utf-8',
        decode_responses=True
    )
    yield redis
    redis.close()
    await redis.wait_closed()
