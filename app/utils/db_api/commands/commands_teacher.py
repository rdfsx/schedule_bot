from asyncpg import UniqueViolationError
from sqlalchemy import func, or_

from app.utils.db_api.schemas.teacher import Teacher
from app.utils.db_api.schemas.teacher_rating import TeacherRating


async def add_teacher(full_name: str) -> int:
    try:
        text = ' '.join(full_name.rstrip().split())
        if len(text.split(" ")) != 3:
            raise ValueError("The number of words must be divisible by 3!")
        teacher = await Teacher.query.where(Teacher.full_name == full_name).gino.first()
        if teacher:
            return teacher.id
        teacher = Teacher(full_name=text)
        await teacher.create()
        return teacher.id

    except UniqueViolationError:
        pass
    except ValueError:
        pass


async def select_all_teachers(teacher: str, offset: int = 0, limit: int = 20):
    teacher = teacher.replace(' ', '').casefold()
    return await Teacher.query\
        .where(func.replace(Teacher.full_name, ' ', '').ilike(f"%{teacher}%"))\
        .order_by(Teacher.full_name).limit(limit).offset(offset).gino.all()


async def select_teacher_by_name(teacher: str):
    teacher_formatted = teacher.replace(' ', '').casefold()
    return await Teacher.query.where(
        or_(
            Teacher.full_name == teacher,
            Teacher.full_name.ilike(f"{teacher_formatted} %")
        )
    ).order_by(Teacher.full_name).gino.all()


async def select_teacher_id(teacher_id: int):
    teacher = await Teacher.query.where(Teacher.id == teacher_id).gino.first()
    return teacher


async def set_rating(teacher_id: int, user_id: int, rate: int):
    try:
        await TeacherRating.create(teacher_id=teacher_id, user_id=user_id, rate=rate)
        teacher = await Teacher.get(teacher_id)
        teacher.rating = teacher.rating + rate
        teacher.count = teacher.count + 1
        await teacher.update(rating=teacher.rating, count=teacher.count).apply()

    except UniqueViolationError:
        pass


async def get_rating(teacher_id: int, user_id: int):
    return await TeacherRating.query\
        .where(TeacherRating.teacher_id == teacher_id)\
        .where(TeacherRating.user_id == user_id).gino.first()


async def delete_rating(teacher_id: int, user_id: int):
    rating = await TeacherRating.query\
        .where(TeacherRating.teacher_id == teacher_id)\
        .where(TeacherRating.user_id == user_id).gino.first()
    if rating:
        await TeacherRating.delete\
            .where(TeacherRating.teacher_id == teacher_id)\
            .where(TeacherRating.user_id == user_id).gino.status()
        teacher = await Teacher.get(teacher_id)
        teacher.rating = teacher.rating - rating.rate
        teacher.count = teacher.count - 1
        if teacher.rating >= 0 and teacher.count >= 0:
            await teacher.update(rating=teacher.rating, count=teacher.count).apply()
