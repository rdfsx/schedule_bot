from abc import ABC, abstractmethod

from app.db.models import Lesson


class AbstractMessageBuilder(ABC):
    @property
    @abstractmethod
    def message(self) -> None:
        pass

    @abstractmethod
    def produce_header(self, header: str) -> None:
        pass

    @abstractmethod
    def produce_lessons(self, lessons: list[Lesson]) -> None:
        pass


class ScheduleMessage:
    def __init__(self) -> None:
        self.parts = []

    def add(self, part: str) -> None:
        self.parts.append(part)

    def list_parts(self) -> str:
        return "\n\n".join(self.parts)


class ScheduleMessageBuilder(AbstractMessageBuilder):
    def __init__(self) -> None:
        self._message: ScheduleMessage | None = None
        self.reset()

    def reset(self) -> None:
        self._message = ScheduleMessage()

    @property
    def message(self) -> ScheduleMessage:
        result = self._message
        self.reset()
        return result

    def produce_header(self, header: str) -> "ScheduleMessageBuilder":
        self._message.add(header)
        return self

    def produce_lessons(self, lessons: list[Lesson]) -> "ScheduleMessageBuilder":
        for lesson in lessons:
            self._message.add(lesson.__str__())
        return self
