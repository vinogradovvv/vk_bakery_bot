# bakery_bot/handlers/delete_product.py

from vk_api.utils import get_random_id
from repositories.product_repository import ProductRepository
from db.database import get_session


async def delete_product_handler(event, vk, is_admin, gen_back_keyboard, state):
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

    product_name = state.product_name
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

        await product_repo.delete_product(product.id)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f"Продукт '{product_name}' удален.",
            keyboard=back_keyboard.get_keyboard()
        )
