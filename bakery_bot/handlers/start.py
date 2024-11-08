from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


async def start_handler(event, vk, state):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Категории", color=VkKeyboardColor.PRIMARY)
    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message="Добро пожаловать! Выберите категорию:",
        keyboard=keyboard.get_keyboard()
    )
    state.go_to_main_menu()
