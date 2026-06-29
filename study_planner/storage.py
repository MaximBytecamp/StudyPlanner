from __future__ import annotations 

import json
from pathlib import Path 
from .models import Task 


class JsonTaskRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path


    def load(self) -> list[Task]:
        if not self.file_path.exisits():
            return []


        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                raw_tasks = json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

        if not isinstance(raw_tasks, list):
            return []

        tasks = []
        for item in raw_tasks:
            if not isinstance(item, dict):
                continue

            try:
                tasks.append(Task.from_dict(item))
            except ValueError:
                continue 

        return tasks 


    def save(self, tasks: list[Task]) -> None:
        data = [task.to_dict() for task in tasks]

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

