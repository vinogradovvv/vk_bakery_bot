import requests
from vk_api.utils import get_random_id
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository
from db.database import get_session
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload


async def add_product_handler(event, vk, is_admin, gen_back_keyboard, gen_menu_keyboard, gen_product_keyboard, state):
    back_keyboard = gen_back_keyboard()

    if not is_admin:
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="У вас нет прав для выполнения этой команды."
        )
        return

    if event.text.startswith("Назад"):
        keyboard = await gen_menu_keyboard(is_admin)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Вы вернулись в главное меню.",
            keyboard=keyboard.get_keyboard()
        )
        state.main_menu()
        return

    if state.is_CATEGORY():
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Введите название нового продукта:",
            keyboard=back_keyboard.get_keyboard()
        )
        state.new_product_name()
        return

    if state.is_NEW_PRODUCT_NAME():
        product_name = event.text
        async with get_session() as db_session:
            product_repo = ProductRepository(db_session)
            existing_product = await product_repo.get_product_by_name(product_name)
            if existing_product:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=f"Продукт '{product_name}' уже существует. Введите другое название:",
                    keyboard=back_keyboard.get_keyboard()
                )
                return
        state.product_name = product_name
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Введите описание нового продукта:",
            keyboard=back_keyboard.get_keyboard()
        )
        state.new_product_description()
        return

    if state.is_NEW_PRODUCT_DESCRIPTION():
        product_description = event.text
        state.product_description = product_description

        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f"Добавьте фото продукта:",
            keyboard=back_keyboard.get_keyboard()
        )
        state.new_product_photo()
        return

    if state.is_NEW_PRODUCT_PHOTO():
        if not event.attachments or 'attach1' not in event.attachments:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Необходимо добавить фото. Попробуйте еще раз.",
                keyboard=back_keyboard.get_keyboard()
            )
            return

        # Получить данные сообщения
        message_data = vk.messages.getById(message_ids=event.message_id)
        if not message_data['items']:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Не удалось получить данные сообщения. Попробуйте еще раз.",
                keyboard=back_keyboard.get_keyboard()
            )
            return

        # Извлечь фото из вложений
        attachments = message_data['items'][0]['attachments']
        photo_attachment = next((att for att in attachments if att['type'] == 'photo'), None)
        if not photo_attachment:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Не удалось найти фото во вложениях. Попробуйте еще раз.",
                keyboard=back_keyboard.get_keyboard()
            )
            return

        photo_info = photo_attachment['photo']
        largest_photo_url = max(photo_info['sizes'], key=lambda size: size['width'])['url']

        # Получить URL сервера загрузки
        upload_server = vk.photos.getMessagesUploadServer(peer_id=event.peer_id)
        upload_url = upload_server['upload_url']

        # Загрузить фото на сервер VK
        photo_data = requests.get(largest_photo_url).content
        response = requests.post(upload_url, files={'photo': ('photo.jpg', photo_data, 'image/jpeg')})
        upload_result = response.json()

        # Проверить успешность загрузки
        if 'photo' not in upload_result or 'server' not in upload_result or 'hash' not in upload_result:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Ошибка загрузки фото. Попробуйте еще раз.",
                keyboard=back_keyboard.get_keyboard()
            )
            return

        # Сохранить фото на VK и получить URL фото
        save_result = vk.photos.saveMessagesPhoto(
            photo=upload_result['photo'],
            server=upload_result['server'],
            hash=upload_result['hash']
        )[0]
        image_url = f"photo{save_result['owner_id']}_{save_result['id']}"

        async with get_session() as db_session:
            category_repo = CategoryRepository(db_session)
            category = await category_repo.get_category_by_name(state.category_name)

            product_repo = ProductRepository(db_session)
            new_product = await product_repo.add_product(
                name=state.product_name,
                description=state.product_description,
                category_id=category.id,
                image_url=image_url  # Сохранить URL в базе данных
            )

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=f"Продукт '{state.product_name}' добавлен в категорию '{category.name}'."
            )

        # Вернуться в категорию и отобразить клавиатуру
        state.category()

        product_keyboard = await gen_product_keyboard(is_admin, state.category_name)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f"Вы вернулись в категорию '{category.name}'.",
            keyboard=product_keyboard.get_keyboard()
        )
