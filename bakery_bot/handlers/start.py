from typing import Callable

from vk_api.longpoll import Event
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod


async def start_handler(
    event: Event, vk: VkApiMethod, state, is_admin: bool, gen_keyboard: Callable
) -> None:
    """
    Handles the start command and displays the main menu.
    Args:
        event (Event): The event object from VK API.
        vk (VkApiMethod): The VK API method instance.
        state: The current state of the bot.
        is_admin (bool): Flag indicating if the user is an admin.
        gen_keyboard (Callable): Function to generate a keyboard.
    """
    keyboard = await gen_keyboard(is_admin)
    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message="Привет! Выберите категорию:",
        keyboard=keyboard.get_keyboard(),
    )
    state.main_menu()
