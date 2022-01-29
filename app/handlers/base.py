import typing
from abc import abstractmethod, ABC
from typing import Any

from aiogram.dispatcher.handler import InlineQueryHandler
from aiogram.methods import AnswerInlineQuery
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from app.constants.convert import ERROR

Model = typing.TypeVar("Model")


class BaseInlineHandler(InlineQueryHandler, ABC):

    buttons: list[InlineQueryResultArticle]

    @abstractmethod
    async def handle(self) -> Any:
        pass

    async def send_inline_buttons(self,
                                  items: list[Model],
                                  action: typing.Callable = None,
                                  **fields: str) -> AnswerInlineQuery:
        inline_query = self.event
        limit = 20
        offset = int(inline_query.offset or 0)
        result = []

        if not items:
            not_found = 'Ничего не найдено'
            result.append(
                InlineQueryResultArticle(
                    id='not_found',
                    title=not_found,
                    input_message_content=InputTextMessageContent(message_text=not_found),
                    thumb_url=ERROR
                )
            )
            return inline_query.answer(result, 120)

        for item in items:
            kwargs = {key: getattr(fields.get(key, ''), item, None) for key, value in fields.items()}
            kwargs['input_message_content'] = InputTextMessageContent(
                message_text=kwargs.pop('input_message_content')
            )
            kwargs['id'] = str(kwargs.pop('id'))
            if action:
                kwargs = action(item, **kwargs)
            result.append(InlineQueryResultArticle(**kwargs))

        next_offset = offset + limit if len(items) >= limit else None

        return inline_query.answer(result, 120, next_offset=str(next_offset))
