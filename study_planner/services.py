from __future__ import annotations

from .config import FILTERS
from .models import Task, parse_deadline
from .storage import JsonTaskRepository


class TaskService:
    def __init__(self, repository: JsonTaskRepository) -> None:
        self.repository = repository
        self.tasks = self.repository.load()


    def add_task(self, title: str, deadline: str, priority: str) -> Task:
        task = Task(
            title=title.strip(),
            deadline=parse_deadline(deadline),
            priority=priority.strip()
        )
        task.validate()

        self.tasks.append(task)
        self.save()
        return task 

    def save(self) -> None: 
        self.repository.save(self.tasks)
        