from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from repositories.product_repository import ProductRepository
from repositories.category_repository import CategoryRepository
from db.database import session


async def product_handler(event, vk, state):
    category_name = event.text
    async with session() as db_session:
        category_repo = CategoryRepository(db_session)
        category = await category_repo.get_category_by_name(category_name)
        if not category:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Категория не найдена."
            )
            return

        product_repo = ProductRepository(db_session)
        products = await product_repo.get_products_by_category_id(category.id)

    keyboard = VkKeyboard(one_time=True)
    for product in products:
        keyboard.add_button(product.name, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)

        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f"Товары в категории {category_name}:",
            keyboard=keyboard.get_keyboard()
        )
        state.select_product()
