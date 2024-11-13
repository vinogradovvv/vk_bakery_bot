from typing import Optional, Sequence

from db.database import get_session
from db.models import Product
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self):
        self.product_repo = None
        self.category_repo = None

    async def get_product_by_name(self, product_name: str) -> Optional[Product]:
        async with get_session() as db_session:
            self.product_repo = ProductRepository(db_session)
            return await self.product_repo.get_product_by_name(product_name)

    async def get_products_by_category_id(self, category_id: int) -> Sequence[Product]:
        async with get_session() as db_session:
            self.product_repo = ProductRepository(db_session)
            return await self.product_repo.get_products_by_category_id(category_id)

    async def add_product(
        self, name: str, description: str, category_name: str, image_url: str
    ) -> None:
        async with get_session() as db_session:
            self.product_repo = ProductRepository(db_session)
            self.category_repo = CategoryRepository(db_session)
            category = await self.category_repo.get_category_by_name(category_name)
            return await self.product_repo.add_product(
                name=name,
                description=description,
                category_id=category.id,
                image_url=image_url,
            )

    async def delete_product(self, product_name: str) -> None:
        async with get_session() as db_session:
            self.product_repo = ProductRepository(db_session)
            product = await self.product_repo.get_product_by_name(product_name)
            if product:
                await self.product_repo.delete_product(product.id)
