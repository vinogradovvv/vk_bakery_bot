import asyncio
import signal
import sys

from bakery_bot.bakery_bot import start_bot
from config.logging_config import logger


def shutdown(signal, frame):
    logger.info("Shutting down...")
    for task in asyncio.all_tasks():
        task.cancel()
    sys.exit(0)


if __name__ == "__main__":
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, shutdown)
    try:
        asyncio.run(start_bot())
    except asyncio.CancelledError:
        logger.warning("Main coroutine cancelled")
