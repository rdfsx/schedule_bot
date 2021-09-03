from enum import Enum
from typing import List

from app.data.convert import lessons_emoji, university_time


class LessonKind(Enum):
    lec = 'лекц.'
    prac = 'практ.'
    lab = 'лаб.'

    def to_str(self) -> str:
        return f"<i>({self.value})</i>"


class Lesson(Enum):
    les_1, les_2, les_3, les_4, les_5, les_6, les_7, les_8 = range(1, 9)

    def to_emoji(self) -> str:
        text = str(lessons_emoji.get(self.value))
        return text

    def to_time(self) -> str:
        return f"<i><u>{university_time.get(self.value)}</u></i>"

    def to_float_list(self) -> List[float]:
        text = str(university_time.get(self.value))
        time = text.replace(" ", "").split('-')
        return [float(time[0]), float(time[1])]

    def do_lesson_str(self, lesson: str, lesson_kind: LessonKind, teacher: str) -> str:
        if not teacher:
            teacher = ''
        return f"{self.to_emoji()} {lesson_kind.to_str()} {lesson} <code>{teacher}</code> {self.to_time()}"
