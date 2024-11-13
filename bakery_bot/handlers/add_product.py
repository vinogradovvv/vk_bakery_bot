from typing import Callable

import requests
from vk_api.longpoll import Event
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod

from services.category_service import CategoryService
from services.product_service import ProductService
from services.session_service import SessionService


async def add_product_handler(
    event: Event,
    vk: VkApiMethod,
    is_admin: bool,
    gen_back_keyboard: Callable,
    gen_menu_keyboard: Callable,
    gen_product_keyboard: Callable,
    state,
) -> None:
    """
    Handles the addition of a new product.
    Args:
        event (Event): The event object from VK API.
        vk (VkApiMethod): The VK API method instance.
        is_admin (bool): Flag indicating if the user is an admin.
        gen_back_keyboard (Callable): Function to generate a back keyboard.
        gen_menu_keyboard (Callable): Function to generate a menu keyboard.
        gen_product_keyboard (Callable): Function to generate a product keyboard.
        state: The current state of the bot.
    """
    back_keyboard = gen_back_keyboard()
    product_service = ProductService()
    category_service = CategoryService()
    ses_service = SessionService()

    if not is_admin:
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="У вас нет прав для выполнения этой команды.",
        )
        return

    if event.text.startswith("Назад"):
        keyboard = await gen_menu_keyboard(is_admin)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Вы вернулись в главное меню.",
            keyboard=keyboard.get_keyboard(),
        )
        state.main_menu()
        async with ses_service.manage_session() as session_service:
            await session_service.save_user_session(event.user_id, state.to_json())
        return

    if state.is_category():
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Введите название нового продукта:",
            keyboard=back_keyboard.get_keyboard(),
        )
        state.new_product_name()
        async with ses_service.manage_session() as session_service:
            await session_service.save_user_session(event.user_id, state.to_json())
        return

    if state.is_new_product_name():
        product_name = event.text
        existing_product = await product_service.get_product_by_name(product_name)
        if existing_product:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=f"Продукт '{product_name}' уже существует. Введите другое название:",
                keyboard=back_keyboard.get_keyboard(),
            )
            return
        state.product_name = product_name
        async with ses_service.manage_session() as session_service:
            await session_service.save_user_session(event.user_id, state.to_json())
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Введите описание нового продукта:",
            keyboard=back_keyboard.get_keyboard(),
        )
        state.new_product_description()
        async with ses_service.manage_session() as session_service:
            await session_service.save_user_session(event.user_id, state.to_json())
        return

    if state.is_new_product_description():
        product_description = event.text
        state.product_description = product_description

        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Добавьте фото продукта:",
            keyboard=back_keyboard.get_keyboard(),
        )
        state.new_product_photo()
        async with ses_service.manage_session() as session_service:
            await session_service.save_user_session(event.user_id, state.to_json())
        return

    if state.is_new_product_photo():
        if not event.attachments or "attach1" not in event.attachments:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Необходимо добавить фото. Попробуйте еще раз.",
                keyboard=back_keyboard.get_keyboard(),
            )
            return

        message_data = vk.messages.getById(message_ids=event.message_id)
        if not message_data["items"]:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Не удалось получить данные сообщения. Попробуйте еще раз.",
                keyboard=back_keyboard.get_keyboard(),
            )
            return

        attachments = message_data["items"][0]["attachments"]
        photo_attachment = next(
            (att for att in attachments if att["type"] == "photo"), None
        )
        if not photo_attachment:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Не удалось найти фото во вложениях. Попробуйте еще раз.",
                keyboard=back_keyboard.get_keyboard(),
            )
            return

        photo_info = photo_attachment["photo"]
        largest_photo_url = max(photo_info["sizes"], key=lambda size: size["width"])[
            "url"
        ]

        upload_server = vk.photos.getMessagesUploadServer(peer_id=event.peer_id)
        upload_url = upload_server["upload_url"]

        photo_data = requests.get(largest_photo_url).content
        response = requests.post(
            upload_url, files={"photo": ("photo.jpg", photo_data, "image/jpeg")}
        )
        upload_result = response.json()

        if (
            "photo" not in upload_result
            or "server" not in upload_result
            or "hash" not in upload_result
        ):
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Ошибка загрузки фото. Попробуйте еще раз.",
                keyboard=back_keyboard.get_keyboard(),
            )
            return

        save_result = vk.photos.saveMessagesPhoto(
            photo=upload_result["photo"],
            server=upload_result["server"],
            hash=upload_result["hash"],
        )[0]
        image_url = f"photo{save_result['owner_id']}_{save_result['id']}"

        category = await category_service.get_category_by_name(state.category_name)
        await product_service.add_product(
            name=state.product_name,
            description=state.product_description,
            category_name=state.category_name,
            image_url=image_url,
        )

        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f"Продукт '{state.product_name}' добавлен в категорию '{category.name}'.",
        )

        state.category()
        async with ses_service.manage_session() as session_service:
            await session_service.save_user_session(event.user_id, state.to_json())

        product_keyboard = await gen_product_keyboard(is_admin, state.category_name)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f"Вы вернулись в категорию '{category.name}'.",
            keyboard=product_keyboard.get_keyboard(),
        )
