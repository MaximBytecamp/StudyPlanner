from __future__ import annotations


from dataclasses import dataclass 
from datetime import date, datetime

from .config import PRIORITIES


DATE_FORMAT = "%d.%m.%Y"

@dataclass 
class Task:
    title: str 
    deadline: date 
    priority: str 
    done: bool = False 

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            title = str(data.get("title", "")).strip(),
            deadline = parse_deadline(data.get("deadline", "")),
            priority = str(data.get("priority", PRIORITIES[1])).strip(),
            done = bool(data.get("done", False))
        )

    def validate(self) -> None:
        if not self.title:
            raise ValueError("Введите название задачи")

        if self.priority not in PRIORITIES:
            raise ValueError("Выберите корректный приоритет")

        if not isinstance(self.deadline, date):
            raise ValueError("Введите дедлайн в формате ДД.ММ.ГГГГ")


def parse_deadline(value: str | date) -> date:
    if isinstance(value, date):
        return value 

    text = str(value).strip()

    if not text:
        raise ValueError("Введите дедлайн")

    try:
        return datetime.strptime(text, DATE_FORMAT).date()
    except ValueError as error:
        raise ValueError(f"Введите дедлайн в фомрате ДД.ММ.ГГГГ - {error}")


def format_deadline(value: date) -> str:
    return value.strftime(DATE_FORMAT)

