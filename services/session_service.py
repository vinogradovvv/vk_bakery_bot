# session_service.py
from repositories.redis_repository import RedisRepository


class SessionService:
    def __init__(self):
        self.repository = RedisRepository()

    async def save_user_session(self, user_id, state):
        await self.repository.save(f"user_session:{user_id}", state)

    async def load_user_session(self, user_id):
        return await self.repository.load(f"user_session:{user_id}")
