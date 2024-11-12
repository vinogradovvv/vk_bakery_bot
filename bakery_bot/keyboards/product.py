from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository
from db.database import get_session
from .back import add_back_button


async def gen_product_keyboard(is_admin, category_name):
    async with get_session() as db_session:
        category_repo = CategoryRepository(db_session)
        category = await category_repo.get_category_by_name(category_name)
        product_repo = ProductRepository(db_session)
        products = await product_repo.get_products_by_category_id(category.id)

    keyboard = VkKeyboard(one_time=True)

    for product in products:
        keyboard.add_button(product.name, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()

    if is_admin:
        keyboard.add_button("Добавить продукт", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Удалить категорию", color=VkKeyboardColor.NEGATIVE)

    keyboard = add_back_button(keyboard)

    return keyboard
