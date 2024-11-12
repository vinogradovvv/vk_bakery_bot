from vk_api.utils import get_random_id
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository
from db.database import get_session


async def category_handler(event, vk, state, is_admin, gen_menu_keyboard, gen_product_keyboard):
    category_name = event.text
    async with get_session() as db_session:
        category_repo = CategoryRepository(db_session)
        category = await category_repo.get_category_by_name(category_name)
        if not category:
            keyboard = await gen_menu_keyboard(is_admin)
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Категория не найдена.",
                keyboard=keyboard.get_keyboard()
            )
            return

        product_repo = ProductRepository(db_session)
        products = await product_repo.get_products_by_category_id(category.id)

    state.category_name = category_name
    keyboard = await gen_product_keyboard(is_admin, category_name)

    if not products:
        message = f"В категории '{category_name}' нет продуктов."
    else:
        message = f"Товары в категории '{category_name}':"

    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=message,
        keyboard=keyboard.get_keyboard()
    )

    state.category()
