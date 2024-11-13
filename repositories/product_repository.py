from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import Product


class ProductRepository:
    """
    Repository class for handling product-related database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the ProductRepository with a database session.
        :param session: The database session to use for operations.
        """
        self.session = session

    async def get_product_by_name(self, name: str) -> Product:
        """
        Retrieve a product by its name.
        :param name: The name of the product to retrieve.
        :return: The Product object if found, else None.
        """
        result = await self.session.execute(select(Product).where(Product.name == name))
        return result.scalar()

    async def get_products_by_category_id(self, category_id: int) -> Sequence[Product]:
        """
        Retrieve all products for a given category ID.
        :param category_id: The ID of the category.
        :return: A sequence of Product objects.
        """
        result = await self.session.execute(
            select(Product).where(Product.category_id == category_id)
        )
        return result.scalars().all()

    async def add_product(
        self, category_id: int, name: str, description: str, image_url: str
    ) -> None:
        """
        Add a new product to the database.
        :param category_id: The ID of the category to which the product belongs.
        :param name: The name of the product.
        :param description: The description of the product.
        :param image_url: The URL of the product's image.
        """
        new_product = Product(
            category_id=category_id,
            name=name,
            description=description,
            image_url=image_url,
        )
        self.session.add(new_product)
        await self.session.commit()

    async def delete_product(self, product_id: int) -> None:
        """
        Delete a product from the database by its ID.
        :param product_id: The ID of the product to delete.
        """
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar()
        if product:
            await self.session.delete(product)
            await self.session.commit()
