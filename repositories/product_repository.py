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

    async def add_product(self, category_id: int, name: str, description: str, image_url: str):
        new_product = Product(category_id=category_id, name=name, description=description, image_url=image_url)
        self.session.add(new_product)
        await self.session.commit()

    async def delete_product(self, product_id: int):
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar()
        if product:
            await self.session.delete(product)
            await self.session.commit()
