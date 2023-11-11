from redis import Redis


def get_redis() -> Redis:
    '''
    Get a Redis instance.
    '''
    return Redis(host="redis", port=6379, db=0)
