from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

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

    async def add_category(self, name: str):
        new_category = Category(name=name)
        self.session.add(new_category)
        await self.session.commit()

    async def delete_category(self, category_id: int):
        result = await self.session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar()
        if category:
            await self.session.delete(category)
            await self.session.commit()
