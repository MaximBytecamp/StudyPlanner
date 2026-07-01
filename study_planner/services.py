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


    def get_tasks(self, filter_name: str = FILTERS[0]) -> list[tuple[int, Task]]:
        if filter_name == FILTERS[1]:
            return [(index, task) for index, task in enumerate(self.tasks) if not task.done]

        if filter_name == FILTERS[2]:
                    return [(index, task) for index, task in enumerate(self.tasks) if task.done]

        return list(enumerate(self.tasks))


    def statistics(self) -> tuple[int, int]:
        done_count = sum(task.done for task in self.tasks)
        return len(self.tasks), done_count