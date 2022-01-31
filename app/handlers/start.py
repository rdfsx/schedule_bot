from typing import Any

from aiogram import types, Dispatcher
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from app.constants.convert import start_sticker
from app.constants.messages import hello_message
from app.handlers.base import BaseInlineHandler, Model
from app.keyboards.inline import GroupSearchKb, GroupStartKb
from app.keyboards.reply import MainMenuMarkup
from app.states import StartStates
from app.utils.db.commands.commands_user import update_user_group
from app.utils.db.commands.coomands_group import select_groups_limit, select_group


async def begin_registration(msg: types.Message) -> Any:
    await StartStates.GROUP.set()
    await msg.answer_sticker(sticker=start_sticker)
    return await msg.answer(f"Приветствую, {msg.from_user.full_name}!\n"
                            "Найди свою группу:", reply_markup=GroupSearchKb().get())


class GroupSetting(BaseInlineHandler):

    async def handle(self) -> Any:
        inline_query = self.event
        offset = int(inline_query.offset or 0)
        teachers = await select_groups_limit(inline_query.query, offset, 20)
        return await self.send_inline_buttons(teachers)

    def build_button(self, model: Model) -> InlineQueryResultArticle:
        return InlineQueryResultArticle(
            id=str(model.id),
            title=model.group,
            input_message_content=InputTextMessageContent(message_text=model.group),
            reply_markup=GroupStartKb().get(model.subgroups),
        )


async def update_subgroup_buttons(query: types.CallbackQuery, callback_data: GroupStartKb.ButtonCD) -> Any:
    markup = GroupStartKb().get(callback_data.amount, callback_data.num)
    return await query.message.edit_reply_markup(markup)


async def update_info(query: types.CallbackQuery, callback_data: GroupStartKb.SaveCD, state: FSMContext) -> Any:
    group = await select_group(query.message.text)
    await update_user_group(user_id=query.from_user.id, group=group.group, subgroup=callback_data.num)
    await state.clear()
    await query.message.delete()
    await query.answer('Добро пожаловать!')
    return await query.message.answer(
        hello_message,
        reply_markup=MainMenuMarkup().get(),
        disable_web_page_preview=True
    )


def setup(dp: Dispatcher):
    dp.message.register(begin_registration, commands="start")
