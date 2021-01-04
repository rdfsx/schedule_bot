import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

STATISTICS_TOKEN = str(os.getenv('STATISTICS_TOKEN'))

LOGS_BASE_PATH = "./"

admins = [
    os.getenv('ADMIN_ID')
]

ip = os.getenv('ip')

redis_ip = os.getenv('redis_ip')

aiogram_redis = {
    'host': redis_ip
}

redis = {
    'address': (redis_ip, 6379),
    'encoding': 'utf8'
}

DATABASE = str(os.getenv('DATABASE'))

PGUSER = str(os.getenv('PGUSER'))

PGPASSWORD = str(os.getenv('PGPASSWORD'))

db_host = ip

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{db_host}/{DATABASE}"
