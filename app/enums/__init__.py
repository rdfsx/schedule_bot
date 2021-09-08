# noinspection PyTypeChecker
class NextMixin:
    def next(self):
        cls = self.__class__

        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]
