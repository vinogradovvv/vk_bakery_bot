# redis_repository.py
import redis.asyncio as aioredis
import json
import os


class RedisRepository:
    def __init__(self):
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = os.getenv('REDIS_PORT', 6379)
        self.redis_db = os.getenv('REDIS_DB', 0)
        self.redis_client = None

    async def get_redis_client(self):
        if not self.redis_client:
            self.redis_client = await aioredis.from_url(
                f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}",
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client

    async def save(self, key, value):
        redis = await self.get_redis_client()
        await redis.set(key, json.dumps(value))

    async def load(self, key):
        redis = await self.get_redis_client()
        data = await redis.get(key)
        if data:
            return json.loads(data)
        return None
