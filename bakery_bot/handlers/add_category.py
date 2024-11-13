from typing import Callable

from vk_api.longpoll import Event
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod

from services.category_service import CategoryService
from services.session_service import SessionService


async def add_category_handler(
    event: Event, vk: VkApiMethod, is_admin: bool, gen_keyboard: Callable, state
) -> None:
    """
    Handles the addition of a new category.

    Args:
        event (Event): The event object from VK API.
        vk (VkApiMethod): The VK API method instance.
        is_admin (bool): Flag indicating if the user is an admin.
        gen_keyboard (Callable): Function to generate a keyboard.
        state: The current state of the bot.
    """
    category_service = CategoryService()
    session_service = SessionService()

    if not is_admin:
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="У вас нет прав для выполнения этой команды.",
        )
        return

    if state.is_main_menu():
        keyboard = gen_keyboard()
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Введите название новой категории:",
            keyboard=keyboard.get_keyboard(),
        )
        state.new_category_name()
        await session_service.save_user_session(event.user_id, state.to_json())
        return

    if event.text.startswith("Назад"):
        keyboard = await gen_keyboard(is_admin)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Вы вернулись в главное меню.",
            keyboard=keyboard.get_keyboard(),
        )
        state.back_to_main_menu()
        await session_service.save_user_session(event.user_id, state.to_json())
        return

    if state.is_new_category_name():
        category_name = event.text
        existing_category = await category_service.get_category_by_name(category_name)
        if existing_category:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=f"Категория '{category_name}' уже существует. Введите другое название:",
            )
            return

        await category_service.add_category(category_name)

        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f"Категория '{category_name}' добавлена.",
        )

        keyboard = await gen_keyboard(is_admin)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Вы вернулись в главное меню.",
            keyboard=keyboard.get_keyboard(),
        )
        state.main_menu()
        await session_service.save_user_session(event.user_id, state.to_json())
