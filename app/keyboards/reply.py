from app.utils.markup_constructor import ReplyMarkupConstructor


class MainMenuMarkup(ReplyMarkupConstructor):
    def get(self):
        schema = [6, 4]
        actions = [
            {'text': 'ПН'}, {'text': 'ВТ'}, {'text': 'СР'}, {'text': 'ЧТ'}, {'text': 'ПТ'}, {'text': 'СБ'},
            {'text': 'Сегодня'}, {'text': 'Сейчас'}, {'text': 'Завтра'}, {'text': 'Ещё'},
        ]
        return self.markup(actions, schema)
