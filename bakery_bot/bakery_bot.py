import os
from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from db.database import init_db
from handlers.start import start_handler
from handlers.category import category_handler
from handlers.add_category import add_category_handler
from handlers.product import product_handler
from handlers.add_product import add_product_handler
from handlers.delete_product import delete_product_handler
from handlers.delete_category import delete_category_handler
from fsm.states import BotStates
from utils.admin_utils import admin_check
from keyboards.main_menu import gen_main_menu_keyboard
from keyboards.back import gen_back_keyboard
from keyboards.product import gen_product_keyboard

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
vk_session = vk_api.VkApi(token=API_TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
state = BotStates()


async def main():
    await init_db()
    for event in longpoll.listen():
        is_admin = admin_check(event.peer_id)
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if state.is_START():
                await start_handler(event, vk, state, is_admin, gen_main_menu_keyboard)

            elif state.is_MAIN_MENU() and event.text.startswith("Добавить категорию"):
                await add_category_handler(event, vk, is_admin, gen_back_keyboard, state)
            elif state.is_NEW_CATEGORY_NAME():
                await add_category_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_keyboard=gen_main_menu_keyboard)

            elif state.is_MAIN_MENU():
                await category_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_menu_keyboard=gen_main_menu_keyboard, gen_product_keyboard=gen_product_keyboard)

            elif state.is_CATEGORY() and event.text.startswith("Добавить продукт"):
                await add_product_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_back_keyboard=gen_back_keyboard, gen_menu_keyboard=gen_main_menu_keyboard, gen_product_keyboard=gen_product_keyboard)
            elif state.is_NEW_PRODUCT_NAME():
                await add_product_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_back_keyboard=gen_back_keyboard, gen_menu_keyboard=gen_main_menu_keyboard, gen_product_keyboard=gen_product_keyboard)
            elif state.is_NEW_PRODUCT_DESCRIPTION():
                await add_product_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_back_keyboard=gen_back_keyboard, gen_menu_keyboard=gen_main_menu_keyboard, gen_product_keyboard=gen_product_keyboard)
            elif state.is_NEW_PRODUCT_PHOTO():
                await add_product_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_back_keyboard=gen_back_keyboard, gen_menu_keyboard=gen_main_menu_keyboard, gen_product_keyboard=gen_product_keyboard)

            elif state.is_CATEGORY() and event.text.startswith("Удалить категорию"):
                await delete_category_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_back_keyboard=gen_back_keyboard)

            elif state.is_PRODUCT() and event.text.startswith("Удалить продукт"):
                await delete_product_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_back_keyboard=gen_back_keyboard)
            elif state.is_DELETE_PRODUCT():
                await delete_product_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_back_keyboard=gen_back_keyboard)

            elif state.is_CATEGORY():
                await product_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_back_keyboard=gen_back_keyboard, gen_menu_keyboard=gen_main_menu_keyboard)
            elif state.is_PRODUCT():
                await product_handler(event=event, vk=vk, state=state, is_admin=is_admin, gen_back_keyboard=gen_back_keyboard, gen_menu_keyboard=gen_main_menu_keyboard)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
