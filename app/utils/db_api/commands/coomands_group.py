import re
from typing import Optional

from asyncpg import UniqueViolationError
from sqlalchemy import func

from app.models.fuckult import Fuckult
from app.utils.db_api.db_gino import db
from app.utils.db_api.schemas.group import Groups


async def add_group(group: str, fuck: Fuckult, subgroups: Optional[int] = 1):
    try:
        new_group = Groups(group=group, fuck=fuck, subgroups=subgroups)
        await new_group.create()

    except UniqueViolationError:
        group_obj = await select_group_exact_match(group)
        if group_obj.fuck != fuck or group_obj.subgroups != subgroups:
            await group_obj.update(fuck=fuck, subgroups=subgroups).apply()


async def select_groups_limit(group: str, offset: Optional[int] = 0, limit: Optional[int] = 20):
    group = re.sub('[ -]', '', group.casefold())
    return await Groups.query.where(func.replace(Groups.group, '-', '').ilike(f"{group}%"))\
        .order_by(Groups.id).limit(limit).offset(offset).gino.all()


async def select_all_groups():
    return await Groups.query.gino.all()


async def select_group_id(group_id: int):
    return await Groups.query.where(Groups.id == group_id).gino.first()


async def select_group(group: str):
    group = re.sub('[ -]', '', group.casefold())
    return await Groups.query.where(func.replace(Groups.group, '-', '').ilike(f"{group}%")).gino.first()


async def select_group_exact_match(group: str):
    return await Groups.query.where(Groups.group == group).gino.first()


async def delete_group(group: str):
    return await Groups.delete.where(Groups.group == group).gino.status()


async def count_groups():
    return await db.func.count(Groups.id).gino.scalar()


async def update_group(group: str, fuck: Fuckult, subgroups: Optional[int]):
    group_obj = await Groups.get(group)
    if group_obj.fuck != fuck or group_obj.subgroups != subgroups:
        group_obj.update(fuck=fuck, subgroups=subgroups).apply()
