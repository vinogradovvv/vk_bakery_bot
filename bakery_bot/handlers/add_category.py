from vk_api.utils import get_random_id
from repositories.category_repository import CategoryRepository
from db.database import get_session


async def add_category_handler(event, vk, is_admin, gen_keyboard, state):

    if not is_admin:
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="У вас нет прав для выполнения этой команды."
        )
        return

    if state.is_MAIN_MENU():
        keyboard = gen_keyboard()
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Введите название новой категории:",
            keyboard=keyboard.get_keyboard()
        )
        state.new_category_name()
        return

    if event.text.startswith("Назад"):
        keyboard = await gen_keyboard(is_admin)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Вы вернулись в главное меню.",
            keyboard=keyboard.get_keyboard()
        )
        state.back_to_main_menu()
        return

    if state.is_NEW_CATEGORY_NAME():
        category_name = event.text
        async with get_session() as db_session:
            category_repo = CategoryRepository(db_session)
            existing_category = await category_repo.get_category_by_name(category_name)
            if existing_category:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=f"Категория '{category_name}' уже существует. Введите другое название:"
                )
                return

            await category_repo.add_category(category_name)

        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f"Категория '{category_name}' добавлена."
        )

        keyboard = await gen_keyboard(is_admin)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Вы вернулись в главное меню.",
            keyboard=keyboard.get_keyboard()
        )
        state.main_menu()
