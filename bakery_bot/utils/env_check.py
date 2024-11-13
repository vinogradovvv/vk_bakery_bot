import os


def check_env():
    if not os.getenv("POSTGRES_HOST"):
        raise ValueError("POSTGRES_HOST not set! Check your .env file!")
    if not os.getenv("POSTGRES_USER"):
        raise ValueError("POSTGRES_USER not set! Check your .env file!")
    if not os.getenv("POSTGRES_PASSWORD"):
        raise ValueError("POSTGRES_PASSWORD not set! Check your .env file!")
    if not os.getenv("POSTGRES_DB"):
        raise ValueError("POSTGRES_DB not set! Check your .env file!")
    if not os.getenv("REDIS_HOST"):
        raise ValueError("REDIS_HOST not set! Check your .env file!")
    if not os.getenv("REDIS_PORT"):
        raise ValueError("REDIS_PORT not set! Check your .env file!")
    if not os.getenv("REDIS_DB"):
        raise ValueError("REDIS_DB not set! Check your .env file!")
    if not os.getenv("API_TOKEN"):
        raise ValueError("API_TOKEN not set! Check your .env file!")
