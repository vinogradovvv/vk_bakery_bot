import os
import sys

from dotenv import load_dotenv

from config.logging_config import logger

sys.path.append(".")
if os.path.exists("./envs/dev.env"):
    logger.info("Loading dev.env")
    load_dotenv("./envs/dev.env", override=True)
