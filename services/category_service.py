from typing import Sequence

from db.database import get_session
from db.models import Category
from repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self) -> None:
        self.category_repo = None

    async def get_category_by_name(self, category_name: str) -> Category:
        async with get_session() as db_session:
            self.category_repo = CategoryRepository(db_session)
            return await self.category_repo.get_category_by_name(category_name)

    async def delete_category(self, category_name: str) -> None:
        async with get_session() as db_session:
            self.category_repo = CategoryRepository(db_session)
            category = await self.category_repo.get_category_by_name(category_name)
            if category:
                await self.category_repo.delete_category(category.id)

    async def add_category(self, category_name: str) -> None:
        async with get_session() as db_session:
            self.category_repo = CategoryRepository(db_session)
            await self.category_repo.add_category(category_name)

    async def get_all_categories(self) -> Sequence[Category]:
        async with get_session() as db_session:
            self.category_repo = CategoryRepository(db_session)
            return await self.category_repo.get_all_categories()
