from contextlib import asynccontextmanager
from repositories.redis_repository import RedisRepository


class SessionService:
    def __init__(self):
        self.repository = RedisRepository()

    async def save_user_session(self, user_id, state):
        await self.repository.save(f"user_session:{user_id}", state)

    async def load_user_session(self, user_id):
        return await self.repository.load(f"user_session:{user_id}")

    async def close(self):
        if self.repository.redis_client:
            await self.repository.redis_client.close()

    @asynccontextmanager
    async def manage_session(self):
        try:
            yield self
        finally:
            await self.close()
