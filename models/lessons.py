from enum import Enum

from typing import List, Tuple

from data.convert import lessons_emoji, university_time


class Lesson(Enum):
    les_1, les_2, les_3, les_4, les_5, les_6, les_7, les_8 = range(1, 9)

    def to_emoji(self) -> str:
        return lessons_emoji.get(self.value)

    def to_str(self) -> str:
        return f"<i><u>{university_time.get(self.value)}</u></i>"

    def to_float_list(self) -> List[float]:
        time = university_time.get(self.value).replace(" ", "").split('-')
        return [float(time[0]), float(time[1])]

    def do_lesson_str(self, lesson: str) -> str:
        return f"{self.to_emoji()} {lesson} {self.to_str()}"
