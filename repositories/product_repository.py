from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_product_by_name(self, name: str):
        result = await self.session.execute(select(Product).where(Product.name == name))
        return result.scalar()

    async def get_products_by_category_id(self, category_id: int):
        result = await self.session.execute(select(Product).where(Product.category_id == category_id))
        return result.scalars().all()
