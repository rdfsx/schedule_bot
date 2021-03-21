import hashlib

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from data.convert import ERROR, start_sticker
from data.messages import hello_message
from filters import GroupFilter
from keyboards.default import menu
from keyboards.inline import search_kb
from keyboards.inline.callback_datas import group_subgroups
from keyboards.inline.inline_buttons import subgroup_menu
from loader import dp
from states import States
from utils.db_api.commands.commands_user import add_user, update_user_group
from utils.db_api.commands.coomands_group import select_groups_limit, select_group, select_group_id


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await States.GROUP.set()
    await message.answer_sticker(sticker=start_sticker)
    await add_user(message.from_user.id)
    await message.answer(f"Приветствую, {message.from_user.full_name}!\n"
                         "Найди свою группу:", reply_markup=search_kb)


@dp.inline_handler(state=States.GROUP)
async def get_all_groups(inline_query: InlineQuery):
    limit = 20
    offset = 0 if inline_query.offset == '' else int(inline_query.offset)
    results = []
    data = await select_groups_limit(inline_query.query, offset, limit)
    if data:
        for group in data:
            results.append(InlineQueryResultArticle(
                id=str(group.id),
                title=group.group,
                input_message_content=(InputTextMessageContent(group.group)), )
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
        await update_user_group(user_id=message.from_user.id, group=group.group)
        await state.reset_state()
        return await message.answer(hello_message, reply_markup=menu, disable_web_page_preview=True)
    await States.SUBGROUP.set()
    await state.update_data(group=group.id)
    await message.answer('Выберите свою подгруппу:', reply_markup=subgroup_menu(group.subgroups))


@dp.message_handler(state=States.GROUP)
async def failed_process_group(message: types.Message):
    await message.answer('Что-то не так. Найдите свою группу:', reply_markup=search_kb)


@dp.callback_query_handler(group_subgroups.filter(), state=States.SUBGROUP)
async def set_subgroup(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    subgroup = str(callback_data.get('number'))
    data = await state.get_data()
    group = await select_group_id(int(data.get('group')))
    await update_user_group(user_id=call.from_user.id, group=group.group, subgroup=int(subgroup))
    await state.reset_state()
    await call.message.delete()
    await call.answer('Добро пожаловать!')
    await call.message.answer(hello_message, reply_markup=menu, disable_web_page_preview=True)


@dp.message_handler(state=States.SUBGROUP)
async def failed_process_subgroup(message: types.Message):
    await message.answer('Выберите свою подгруппу☝️')
