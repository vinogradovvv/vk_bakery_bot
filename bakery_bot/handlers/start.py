from vk_api.utils import get_random_id


async def start_handler(event, vk, state, is_admin, gen_keyboard):
    keyboard = await gen_keyboard(is_admin)
    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message="Привет! Выберите категорию:",
        keyboard=keyboard.get_keyboard()
    )
    state.main_menu()
