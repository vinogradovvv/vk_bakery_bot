import os

import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

from bakery_bot.fsm.states import BotStates
from bakery_bot.handlers.add_category import add_category_handler
from bakery_bot.handlers.add_product import add_product_handler
from bakery_bot.handlers.category import category_handler
from bakery_bot.handlers.delete_category import delete_category_handler
from bakery_bot.handlers.delete_product import delete_product_handler
from bakery_bot.handlers.product import product_handler
from bakery_bot.handlers.start import start_handler
from bakery_bot.keyboards.back import gen_back_keyboard
from bakery_bot.keyboards.main_menu import gen_main_menu_keyboard
from bakery_bot.keyboards.product import gen_product_keyboard
from bakery_bot.utils.admin_utils import admin_check
from config.logging_config import logger
from db.database import init_db
from services.session_service import SessionService

API_TOKEN = os.getenv("API_TOKEN")
vk_session = vk_api.VkApi(token=API_TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
session_service = SessionService()


async def start_bot() -> None:
    logger.info("Initializing database")
    await init_db()
    logger.info("Starting event loop")
    for event in longpoll.listen():
        peer_id = event.peer_id
        is_admin = admin_check(event.peer_id)
        user_state = await session_service.load_user_session(peer_id)
        state = BotStates()
        if user_state:
            state.load(**user_state)
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if state.is_start():
                await start_handler(event, vk, state, is_admin, gen_main_menu_keyboard)

            elif state.is_main_menu() and event.text.startswith("Добавить категорию"):
                await add_category_handler(
                    event, vk, is_admin, gen_back_keyboard, state
                )
            elif state.is_new_category_name():
                await add_category_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_keyboard=gen_main_menu_keyboard,
                )

            elif state.is_main_menu():
                await category_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_menu_keyboard=gen_main_menu_keyboard,
                    gen_product_keyboard=gen_product_keyboard,
                )

            elif state.is_category() and event.text.startswith("Добавить продукт"):
                await add_product_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_back_keyboard=gen_back_keyboard,
                    gen_menu_keyboard=gen_main_menu_keyboard,
                    gen_product_keyboard=gen_product_keyboard,
                )
            elif state.is_new_product_name():
                await add_product_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_back_keyboard=gen_back_keyboard,
                    gen_menu_keyboard=gen_main_menu_keyboard,
                    gen_product_keyboard=gen_product_keyboard,
                )
            elif state.is_new_product_description():
                await add_product_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_back_keyboard=gen_back_keyboard,
                    gen_menu_keyboard=gen_main_menu_keyboard,
                    gen_product_keyboard=gen_product_keyboard,
                )
            elif state.is_new_product_photo():
                await add_product_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_back_keyboard=gen_back_keyboard,
                    gen_menu_keyboard=gen_main_menu_keyboard,
                    gen_product_keyboard=gen_product_keyboard,
                )

            elif state.is_category() and event.text.startswith("Удалить категорию"):
                await delete_category_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_back_keyboard=gen_back_keyboard,
                    gen_menu_keyboard=gen_main_menu_keyboard,
                )

            elif state.is_product() and event.text.startswith("Удалить продукт"):
                await delete_product_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_back_keyboard=gen_back_keyboard,
                    gen_menu_keyboard=gen_main_menu_keyboard,
                )
            elif state.is_delete_product():
                await delete_product_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_back_keyboard=gen_back_keyboard,
                    gen_menu_keyboard=gen_main_menu_keyboard,
                )

            elif state.is_category():
                await product_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_back_keyboard=gen_back_keyboard,
                    gen_menu_keyboard=gen_main_menu_keyboard,
                )
            elif state.is_product():
                await product_handler(
                    event=event,
                    vk=vk,
                    state=state,
                    is_admin=is_admin,
                    gen_back_keyboard=gen_back_keyboard,
                    gen_menu_keyboard=gen_main_menu_keyboard,
                )
