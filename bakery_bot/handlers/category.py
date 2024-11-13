from typing import Callable

from vk_api.longpoll import Event
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod

from services.category_service import CategoryService
from services.product_service import ProductService
from services.session_service import SessionService


async def category_handler(
    event: Event,
    vk: VkApiMethod,
    state,
    is_admin: bool,
    gen_menu_keyboard: Callable,
    gen_product_keyboard: Callable,
) -> None:
    """
    Handles the category selection and displays products in the selected category.
    Args:
        event (Event): The event object from VK API.
        vk (VkApiMethod): The VK API method instance.
        state: The current state of the bot.
        is_admin (bool): Flag indicating if the user is an admin.
        gen_menu_keyboard (Callable): Function to generate a menu keyboard.
        gen_product_keyboard (Callable): Function to generate a product keyboard.
    """
    category_service = CategoryService()
    product_service = ProductService()
    session_service = SessionService()

    category_name = event.text
    category = await category_service.get_category_by_name(category_name)
    if not category:
        keyboard = await gen_menu_keyboard(is_admin)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Категория не найдена.",
            keyboard=keyboard.get_keyboard(),
        )
        return

    products = await product_service.get_products_by_category_id(category.id)

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
        keyboard=keyboard.get_keyboard(),
    )

    state.category()
    await session_service.save_user_session(event.user_id, state.to_json())
