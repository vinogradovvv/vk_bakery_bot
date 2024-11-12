import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS').split(',')))


def admin_check(user_id):
    return user_id in ADMIN_IDS
