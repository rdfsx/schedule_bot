from asyncpg import UniqueViolationError

from loader import dp

from utils.db_api.db_gino import db
from utils.db_api.schemas.group import Groups
from utils.db_api.schemas.user import User
from utils.notify_admins import notify_new_user


async def add_user(user_id: int, group: str, subgroup: int = 1) -> None:
    group_id = await Groups.select('id').where(Groups.group == group).gino.scalar()
    try:
        user = User(id=user_id, group_id=group_id, subgroup=subgroup)
        await user.create()
        await notify_new_user(dp, user_id, group)

    except UniqueViolationError:
        user = await User.get(user_id)
        await user.update(group_id=group_id, subgroup=subgroup).apply()


async def select_all_users():
    return await User.query.gino.all()


async def select_user(user_id: int):
    return await User.query.where(User.id == user_id).gino.first()


async def count_users():
    return await db.func.count(User.id).gino.scalar()


async def update_user_group(user_id: int, group: str, subgroup: int=1):
    user = await User.get(user_id)
    await user.update(group=group, subgroup=subgroup).apply()
