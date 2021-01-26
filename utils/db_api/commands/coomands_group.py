import re
from typing import Optional

from asyncpg import UniqueViolationError

from sqlalchemy import func

from models.fuckult import Fuckult
from utils.db_api.db_gino import db
from utils.db_api.schemas.group import Groups


async def add_group(group: str, fuck: Fuckult, subgroups: int = 1):
    try:
        group = Groups(group=group, fuck=fuck, subgroups=subgroups)
        await group.create()

    except UniqueViolationError:
        pass


async def select_groups_limit(group: str, offset: int = 0, limit: int = 20):
    group = re.sub('[ -]', '', group.casefold())
    return await Groups.query.where(func.replace(Groups.group, '-', '').ilike(f"%{group}%"))\
        .order_by(Groups.id).limit(limit).offset(offset).gino.all()


async def select_all_groups():
    return await Groups.query.gino.all()


async def select_group_id(group_id: int):
    return await Groups.query.where(Groups.id == group_id).gino.first()


async def select_group(group: str):
    group = re.sub('[ -]', '', group.casefold())
    return await Groups.query.where(func.replace(Groups.group, '-', '').ilike(f"%{group}%")).gino.first()


async def delete_group(group: str):
    return await Groups.delete.where(Groups.group == group).gino.status()


async def count_groups():
    return await db.func.count(Groups.id).gino.scalar()
