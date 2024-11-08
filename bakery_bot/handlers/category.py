from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from repositories.category_repository import CategoryRepository
from db.database import session


async def category_handler(event, vk, state):
    if event.text == "Категории":
        async with session() as db_session:
            category_repo = CategoryRepository(db_session)
            categories = await category_repo.get_all_categories()

        keyboard = VkKeyboard(one_time=True)
        for category in categories:
            keyboard.add_button(category.name, color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
        keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)

        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Выберите категорию:",
            keyboard=keyboard.get_keyboard()
        )
        state.select_category()
