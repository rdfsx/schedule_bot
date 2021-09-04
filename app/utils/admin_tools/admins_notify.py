from app.config import admins
from app.loader import bot


async def notify_admins(text: str):
    for admin in admins:
        await bot.send_message(admin, text)
