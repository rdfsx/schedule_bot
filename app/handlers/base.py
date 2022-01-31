import typing
from abc import abstractmethod, ABC
from typing import Any

from aiogram.dispatcher.handler import InlineQueryHandler
from aiogram.methods import AnswerInlineQuery
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from app.constants.convert import ERROR

Model = typing.TypeVar("Model")


class BaseInlineHandler(InlineQueryHandler, ABC):

    @abstractmethod
    async def handle(self) -> Any:
        pass

    @abstractmethod
    async def build_button(self, model: Model) -> InlineQueryResultArticle:
        pass

    def send_inline_buttons(self,
                            items: list[Model],
                            limit: int = 20,
                            cache_time: int = 120) -> AnswerInlineQuery:
        inline_query = self.event
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
            return inline_query.answer(result, cache_time)

        for item in items:
            result.append(self.build_button(item))

        next_offset = offset + limit if len(items) >= limit else None

        return inline_query.answer(result, cache_time, next_offset=str(next_offset))
