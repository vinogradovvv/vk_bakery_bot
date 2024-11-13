from typing import Callable

from vk_api.longpoll import Event
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod

from services.product_service import ProductService


async def delete_product_handler(
    event: Event,
    vk: VkApiMethod,
    is_admin: bool,
    gen_back_keyboard: Callable,
    gen_menu_keyboard: Callable,
    state,
) -> None:
    """
    Handles the deletion of a product.
    Args:
        event (Event): The event object from VK API.
        vk (VkApiMethod): The VK API method instance.
        is_admin (bool): Flag indicating if the user is an admin.
        gen_back_keyboard (Callable): Function to generate a back keyboard.
        gen_menu_keyboard (Callable): Function to generate a menu keyboard.
        state: The current state of the bot.
    """
    product_service = ProductService()
    back_keyboard = gen_back_keyboard()
    menu_keyboard = await gen_menu_keyboard(is_admin)

    if not is_admin:
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="У вас нет прав для выполнения этой команды.",
            keyboard=menu_keyboard.get_keyboard(),
        )
        return

    if event.text.startswith("Назад"):
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Вы вернулись в главное меню.",
            keyboard=menu_keyboard.get_keyboard(),
        )
        state.back_to_main_menu()
        return

    product_name = event.text
    product = await product_service.get_product_by_name(product_name)
    if not product:
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Продукт не найден.",
            keyboard=back_keyboard.get_keyboard(),
        )
        return

    await product_service.delete_product(product_name)
    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=f"Продукт '{product_name}' удален.",
        keyboard=menu_keyboard.get_keyboard(),
    )
    state.back_to_main_menu()
