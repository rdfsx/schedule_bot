from config import admins
from loader import bot


async def notify_admins(text: str):
    for admin in admins:
        await bot.send_message(admin, text)
