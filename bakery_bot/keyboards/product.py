from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from services.category_service import CategoryService
from services.product_service import ProductService

from .back import add_back_button


async def gen_product_keyboard(is_admin: bool, category_name: str) -> VkKeyboard:
    """
    Generates a product keyboard with products and admin options for a given category.
    Args:
        is_admin (bool): Flag indicating if the user is an admin.
        category_name (str): The name of the category for which to generate the keyboard.
    Returns:
        VkKeyboard: The generated product keyboard.
    """
    category_service = CategoryService()
    product_service = ProductService()

    category = await category_service.get_category_by_name(category_name)
    products = await product_service.get_products_by_category_id(category.id)

    keyboard = VkKeyboard(one_time=True)

    for product in products:
        keyboard.add_button(product.name, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()

    if is_admin:
        keyboard.add_button("Добавить продукт", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Удалить категорию", color=VkKeyboardColor.NEGATIVE)

    keyboard = add_back_button(keyboard)

    return keyboard
