from app.utils.markup_constructor import InlineMarkupConstructor


class GroupSearchKb(InlineMarkupConstructor):

    def get(self):
        schema = [1]
        actions = [
            {'text': 'Найти группу', 'switch_inline_query_current_chat': ''},
        ]
        return self.markup(actions, schema)
