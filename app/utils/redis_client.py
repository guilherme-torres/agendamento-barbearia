import redis
from app.config import get_settings


redis_client = redis.Redis(
    host=get_settings().REDIS_HOST,
    port=get_settings().REDIS_PORT,
    db=get_settings().REDIS_DB
)