from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from repositories.category_repository import CategoryRepository
from db.database import get_session


async def gen_main_menu_keyboard(is_admin):
    keyboard = VkKeyboard(one_time=True)

    async with get_session() as db_session:
        category_repo = CategoryRepository(db_session)
        categories = await category_repo.get_all_categories()

    for category in categories:
        keyboard.add_button(category.name, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()

    if is_admin:
        keyboard.add_button("Добавить категорию", color=VkKeyboardColor.POSITIVE)

    return keyboard
