import hashlib

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from config import faculties, ERROR
from data.messages import hello_message
from filters import GroupFilter

from keyboards.default import menu, subgroup_menu
from keyboards.inline import search_kb

from loader import dp
from states import States

from utils.db_api.commands.commands_user import add_user
from utils.db_api.commands.coomands_group import select_all_groups, select_group, select_group_id


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await States.GROUP.set()
    await message.answer(f"Приветствую, {message.from_user.full_name}!\n"
                         "Найди свою группу:", reply_markup=search_kb)


@dp.inline_handler(state=States.GROUP)
async def get_all_groups(inline_query: InlineQuery):
    limit = 20
    offset = 0 if inline_query.offset == '' else int(inline_query.offset)
    results = []
    data = await select_all_groups(inline_query.query, offset, limit)
    if data:
        for group in data:
            results.append(InlineQueryResultArticle(
                id=str(hashlib.md5(group.group.encode()).hexdigest()),
                title=group.group,
                input_message_content=(InputTextMessageContent(group.group)),
                thumb_url=faculties.get(group.fuck.name))
            )
    else:
        not_found = 'Нет такой группы'
        results = [InlineQueryResultArticle(
            id=str(hashlib.md5(not_found.encode()).hexdigest()),
            title=not_found,
            input_message_content=InputTextMessageContent(not_found),
            thumb_url=ERROR
        )]
    next_offset = str(offset + limit) if len(data) >= limit else ''
    await inline_query.answer(results=results, next_offset=next_offset)


@dp.message_handler(GroupFilter(), state=States.GROUP)
async def check_group(message: types.Message, state: FSMContext):
    group = await select_group(message.text)
    if group.subgroups == 1:
        await add_user(user_id=message.from_user.id, group=group.group)
        await state.reset_state()
        return await message.answer(hello_message, reply_markup=menu)
    await States.SUBGROUP.set()
    await state.update_data(group=group.id)
    await message.answer('Выберите свою подгруппу:', reply_markup=subgroup_menu(group.subgroups))


@dp.message_handler(state=States.GROUP)
async def failed_process_group(message: types.Message):
    await message.answer('Что-то не так. Найдите свою группу:', reply_markup=search_kb)


@dp.message_handler(state=States.SUBGROUP)
async def final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group = await select_group_id(int(data.get('group')))
    if not message.text.isdigit() or int(message.text) > group.subgroups:
        return await message.answer('Выберите свою подгруппу:', reply_markup=subgroup_menu(group.subgroups))
    await add_user(user_id=message.from_user.id, group=group.group, subgroup=int(message.text))
    await state.reset_state()
    await message.answer(hello_message, reply_markup=menu)
