import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from db.database import init_db
from handlers.start import start_handler
from handlers.category import category_handler
from handlers.product import product_handler
from states import BotStates

API_TOKEN = 'YOUR_VK_API_TOKEN'
vk_session = vk_api.VkApi(token=API_TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
state = BotStates()


async def main():
    await init_db()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if state.is_START():
                await start_handler(event, vk, state)
            elif state.is_MAIN_MENU():
                await category_handler(event, vk, state)
            elif state.is_CATEGORY():
                await product_handler(event, vk, state)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
