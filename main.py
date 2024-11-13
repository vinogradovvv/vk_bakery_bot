import asyncio
import signal
import sys

from bakery_bot.bakery_bot import start_bot
from bakery_bot.utils.env_check import check_env
from config.logging_config import logger
from services.session_service import SessionService

session_service = SessionService()


def shutdown(signal, frame):
    logger.info("Shutting down...")
    for task in asyncio.all_tasks():
        task.cancel()
    loop = asyncio.get_event_loop()
    loop.create_task(session_service.close())
    sys.exit(0)


if __name__ == "__main__":
    check_env()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, shutdown)
    try:
        asyncio.run(start_bot())
    except asyncio.CancelledError:
        logger.warning("Main coroutine cancelled")
