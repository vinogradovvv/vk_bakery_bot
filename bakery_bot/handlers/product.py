from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from repositories.product_repository import ProductRepository
from repositories.category_repository import CategoryRepository
from db.database import get_session


async def product_handler(event, vk, state, is_admin, gen_back_keyboard, gen_menu_keyboard):
    product_name = event.text
    state.product_name = product_name
    back_keyboard = gen_back_keyboard()
    menu_keyboard = await gen_menu_keyboard(is_admin)

    if event.text.startswith("Назад"):
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Вы вернулись в главное меню.",
            keyboard=menu_keyboard.get_keyboard()
        )
        state.back_to_main_menu()
        return

    async with get_session() as db_session:
        product_repo = ProductRepository(db_session)
        product = await product_repo.get_product_by_name(product_name)
        if not product:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Продукт не найден.",
                keyboard=back_keyboard.get_keyboard()
            )
            return

    if is_admin:
        back_keyboard.add_button('Удалить продукт', color=VkKeyboardColor.NEGATIVE)

    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=f"Название: {product.name}\nОписание: {product.description}",
        attachment=product.image_url,
        keyboard=back_keyboard.get_keyboard()
    )
    state.product()
