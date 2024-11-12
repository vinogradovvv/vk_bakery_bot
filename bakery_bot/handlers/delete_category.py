from vk_api.utils import get_random_id
from repositories.category_repository import CategoryRepository
from db.database import get_session


async def delete_category_handler(event, vk, is_admin, gen_back_keyboard, state):
    back_keyboard = gen_back_keyboard()

    if not is_admin:
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="У вас нет прав для выполнения этой команды."
        )
        return

    if event.text.startswith("Назад"):
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Вы вернулись в главное меню.",
            keyboard=back_keyboard.get_keyboard()
        )
        state.back_to_main_menu()
        return

    category_name = state.category_name
    async with get_session() as db_session:
        category_repo = CategoryRepository(db_session)
        category = await category_repo.get_category_by_name(category_name)
        if not category:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Категория не найдена.",
                keyboard=back_keyboard.get_keyboard()
            )
            return

        await category_repo.delete_category(category.id)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f"Категория '{category_name}' и все её продукты удалены.",
            keyboard=back_keyboard.get_keyboard()
        )
        state.main_menu()
