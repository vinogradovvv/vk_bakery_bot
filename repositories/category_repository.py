from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_categories(self):
        result = await self.session.execute(select(Category))
        return result.scalars().all()

    async def get_category_by_name(self, name: str):
        result = await self.session.execute(select(Category).where(Category.name == name))
        return result.scalar()
