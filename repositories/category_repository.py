from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import Category


class CategoryRepository:
    """
    Repository class for handling category-related database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the CategoryRepository with a database session.
        :param session: The database session to use for operations.
        """
        self.session = session

    async def get_all_categories(self) -> Sequence[Category]:
        """
        Retrieve all categories from the database.
        :return: A sequence of Category objects.
        """
        result = await self.session.execute(select(Category))
        return result.scalars().all()

    async def get_category_by_name(self, name: str) -> Category:
        """
        Retrieve a category by its name.
        :param name: The name of the category to retrieve.
        :return: The Category object if found, else None.
        """
        result = await self.session.execute(
            select(Category).where(Category.name == name)
        )
        return result.scalar()

    async def add_category(self, name: str) -> None:
        """
        Add a new category to the database.
        :param name: The name of the category to add.
        """
        new_category = Category(name=name)
        self.session.add(new_category)
        await self.session.commit()

    async def delete_category(self, category_id: int) -> None:
        """
        Delete a category from the database by its ID.
        :param category_id: The ID of the category to delete.
        """
        result = await self.session.execute(
            select(Category).where(Category.id == category_id)
        )
        category = result.scalar()
        if category:
            await self.session.delete(category)
            await self.session.commit()
