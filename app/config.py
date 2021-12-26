import os
from pathlib import Path
from typing import NamedTuple

from dotenv import load_dotenv
from environs import Env

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

STATISTICS_TOKEN = str(os.getenv('STATISTICS_TOKEN'))

LOGS_BASE_PATH = "../"

admins = [
    os.getenv('ADMIN_ID')
]

REDIS_HOST = str(os.getenv("REDIS_HOST"))
REDIS_PORT = 6379

aiogram_redis = {
    'host': REDIS_HOST
}

redis = {
    'address': (REDIS_HOST, REDIS_PORT),
    'encoding': 'utf8'
}

POSTGRES_DB = str(os.getenv('POSTGRES_DB'))

POSTGRES_USER = str(os.getenv('POSTGRES_USER'))

POSTGRES_PASSWORD = str(os.getenv('POSTGRES_PASSWORD'))

POSTGRES_HOST = str(os.getenv('POSTGRES_HOST'))

POSTGRES_PORT = 5432

POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

CARD_FOR_DONUTS = str(os.getenv('CARD_FOR_DONUTS'))
CARD_VALID_THRU_DONUTS = str(os.getenv('CARD_VALID_THRU_DONUTS'))
ETHEREUM_DONUTS = str(os.getenv('ETHEREUM_DONUTS'))
BITCOIN_DONUTS = str(os.getenv('BITCOIN_DONUTS'))


class Config(NamedTuple):
    __env = Env()
    __env.read_env()

    BASE_DIR = Path(__name__).resolve().parent.parent
    LOCALES_PATH = BASE_DIR / 'locales'

    BOT_TOKEN = __env.str('BOT_TOKEN')

    ADMINS = __env.list('ADMIN_ID')

    MONGODB_DATABASE = __env.str('MONGODB_DATABASE')
    MONGODB_USERNAME = __env.str('MONGODB_USERNAME')
    MONGODB_PASSWORD = __env.str('MONGODB_PASSWORD')
    MONGODB_HOSTNAME = __env.str('MONGODB_HOSTNAME')
    MONGODB_PORT = __env.str('MONGODB_PORT')
    MONGODB_URI = 'mongodb://'

    if MONGODB_USERNAME and MONGODB_PASSWORD:
        MONGODB_URI += f"{MONGODB_USERNAME}:{MONGODB_PASSWORD}@"
    MONGODB_URI += f"{MONGODB_HOSTNAME}:{MONGODB_PORT}"

    STATISTICS_TOKEN = __env.str('STATISTICS_TOKEN')
