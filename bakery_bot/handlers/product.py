from typing import Callable

from vk_api.keyboard import VkKeyboardColor
from vk_api.longpoll import Event
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod

from services.product_service import ProductService
from services.session_service import SessionService


async def product_handler(
    event: Event,
    vk: VkApiMethod,
    state,
    is_admin: bool,
    gen_back_keyboard: Callable,
    gen_menu_keyboard: Callable,
) -> None:
    """
    Handles the product selection and displays product details.
    Args:
        event (Event): The event object from VK API.
        vk (VkApiMethod): The VK API method instance.
        state: The current state of the bot.
        is_admin (bool): Flag indicating if the user is an admin.
        gen_back_keyboard (Callable): Function to generate a back keyboard.
        gen_menu_keyboard (Callable): Function to generate a menu keyboard.
    """
    product_service = ProductService()
    ses_service = SessionService()
    product_name = event.text
    state.product_name = product_name
    back_keyboard = gen_back_keyboard()
    menu_keyboard = await gen_menu_keyboard(is_admin)

    if event.text.startswith("Назад"):
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Вы вернулись в главное меню.",
            keyboard=menu_keyboard.get_keyboard(),
        )
        state.back_to_main_menu()
        async with ses_service.manage_session() as session_service:
            await session_service.save_user_session(event.user_id, state.to_json())
        return

    product = await product_service.get_product_by_name(product_name)
    if not product:
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Продукт не найден.",
            keyboard=back_keyboard.get_keyboard(),
        )
        return

    if is_admin:
        back_keyboard.add_button("Удалить продукт", color=VkKeyboardColor.NEGATIVE)

    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=f"Название: {product.name}\nОписание: {product.description}",
        attachment=product.image_url,
        keyboard=back_keyboard.get_keyboard(),
    )
    state.product()
    async with ses_service.manage_session() as session_service:
        await session_service.save_user_session(event.user_id, state.to_json())
