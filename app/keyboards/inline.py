from aiogram.dispatcher.filters.callback_data import CallbackData

from app.utils.markup_constructor import InlineMarkupConstructor


class GroupSearchKb(InlineMarkupConstructor):

    def get(self):
        schema = [1]
        actions = [
            {'text': 'Найти группу', 'switch_inline_query_current_chat': ''},
        ]
        return self.markup(actions, schema)


class GroupStartKb(InlineMarkupConstructor):

    class SaveCD(CallbackData, prefix="save"):
        num: int | None
        amount: int

    class ButtonCD(CallbackData, prefix="save"):
        num: int
        amount: int

    def get(self, amount: int, active: int | None = None):
        actions = []

        if amount > 1:
            for i in range(amount):
                actions.append({
                    'text': f'{"☑️" if active and active == i else ""}{i} подгруппа',
                    'cb': self.ButtonCD(num=i, amount=amount).pack()
                })

        actions.append({'text': 'Сохранить', 'cb': self.SaveCD(num=active, amount=amount).pack()})
        actions.append({'text': 'Найти группу', 'switch_inline_query_current_chat': ''})

        return self.markup(actions, [1] * len(actions))
