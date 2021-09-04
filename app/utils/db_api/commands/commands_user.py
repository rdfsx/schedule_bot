from typing import Optional

from asyncpg import UniqueViolationError

from app.loader import dp
from app.utils.db_api.db_gino import db
from app.utils.db_api.schemas.group import Groups
from app.utils.db_api.schemas.user import User
from app.utils.notify_admins import notify_new_user


async def add_user(user_id: int, group: Optional[str] = None, subgroup: Optional[int] = 1):
    group_id = await Groups.select('id').where(Groups.group == group).gino.scalar()
    user = await User.get(user_id)
    if user:
        return
    try:
        user = User(id=user_id, group_id=group_id, subgroup=subgroup)
        await user.create()

    except UniqueViolationError:
        if not user.group_id and group is not None:
            await notify_new_user(dp, user_id, group)
        await user.update(group_id=group_id, subgroup=subgroup).apply()


async def select_all_users():
    return await User.query.gino.all()


async def select_user(user_id: int):
    return await User.query.where(User.id == user_id).gino.first()


async def count_users():
    return await db.func.count(User.id).gino.scalar()


async def count_users_with_group():
    return await db.func.count(User.group_id).gino.scalar()


async def update_user_group(user_id: int, group: str, subgroup: Optional[int] = 1):
    user = await User.get(user_id)
    group_id = await Groups.select('id').where(Groups.group == group).gino.scalar()
    if not user.group_id:
        await notify_new_user(dp, user_id, group)
    await user.update(group_id=group_id, subgroup=subgroup).apply()
