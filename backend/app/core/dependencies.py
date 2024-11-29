from .settings import REDIS_URL
import redis

def get_redis_client():
    return redis.StrictRedis.from_url(REDIS_URL)
