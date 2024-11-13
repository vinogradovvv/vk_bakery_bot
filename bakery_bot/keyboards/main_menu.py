from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from services.category_service import CategoryService


async def gen_main_menu_keyboard(is_admin: bool) -> VkKeyboard:
    """
    Generates the main menu keyboard with categories and admin options.
    Args:
        is_admin (bool): Flag indicating if the user is an admin.
    Returns:
        VkKeyboard: The generated main menu keyboard.
    """
    keyboard = VkKeyboard(one_time=True)
    category_service = CategoryService()

    categories = await category_service.get_all_categories()

    for category in categories:
        keyboard.add_button(category.name, color=VkKeyboardColor.PRIMARY)

    if is_admin:
        keyboard.add_line()
        keyboard.add_button("Добавить категорию", color=VkKeyboardColor.POSITIVE)

    return keyboard
