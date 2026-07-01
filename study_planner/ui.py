import tkinter as tk 
from .storage import JsonTaskRepository
from .config import FILTERS, PRIORITIES, TASKS_FILE
from tkinter import messagebox, ttk
from .services import TaskService

class StudyPlannerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Study Planner")
        self.root.geometry("760x520")
        self.root.minsize(640, 440)

        repository = JsonTaskRepository(TASKS_FILE)
        self.service = TaskService(repository)

        self.visible_indexes: list[int] = []

        self.title_var= tk.StringVar()
        self.deadline_var = tk.StringVar()
        self.priority_var = tk.StringVar(value=PRIORITIES[1])
        self.filter_var = tk.StringVar(value=FILTERS[0])
        self.stats_var = tk.StringVar()

        self._build_ui()
        self._refresh_tasks()

    def run(self) -> None:
        self.root.mainloop()


    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        form = ttk.LabelFrame(self.root, text="Новая задача", padding=12)
        form.grid(row=0, column=0, padx=12, pady=(12, 6), sticky="ew")
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Название:").grid(row=0, column=0, padx=(0,8), pady=4, sticky="w")
        ttk.Entry(form, textvariable=self.title_var).grid(row=0, column=1, padx=(0,8), pady=4, sticky="ew")

        ttk.Label(form, text="Дедлайн:").grid(row=1, column=0, padx=(0,8), pady=4, sticky="w")
        ttk.Entry(form, textvariable=self.deadline_var).grid(row=1, column=1, padx=(0,8), pady=4, sticky="ew")
        ttk.Label(form, text="ДД.ММ.ГГГГ").grid(row=1, column=2, pady=4, sticky="w")


        ttk.Label(form, text="Приоритет: ").grid(row=2, column=0, padx=(0,8), pady=4, sticky="w")
        ttk.Combobox(
            form,
            textvariable=self.priority_var,
            values=PRIORITIES,
            state="readonly",
            width=18
        ).grid(row=2, column=1, padx=(0,8), pady=4, sticky="w")

        buttons = ttk.Frame(form)
        buttons.grid(row=3, column=1, pady=(8,0), sticky="w")
        ttk.Button(buttons, text="Добавить задачу", command=self._add_task).grid(row=0, column=0, padx=(0,8))
        ttk.Button(buttons, text="Очистить", command=self._clear_form).grid(row=0, column=1)

        content = ttk.LabelFrame(self.root, text="Список задач", padding=12)
        content.grid(row=1, column=0, padx=12, pady=6, sticky="nsew")
        content.rowconfigure(1, weight=1)   
        content.columnconfigure(0, weight=1)

        filter_row = ttk.Frame(content)
        filter_row.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,8))

        ttk.Label(filter_row, text="Фильтр: ").grid(row=0, column=0, padx=(0,8), sticky="w")
        filter_box = ttk.Combobox(
            filter_row,
            textvariable=self.filter_var,
            values=FILTERS, 
            state="readonly",
            width=18
        )
        filter_box.grid(row=0, column=1, sticky="w")

        self.listbox = tk.Listbox(content, height=12, activestyle="dotbox")
        self.listbox.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(self.root, padding=(12,6))
        actions.grid(row=2, column=0, sticky="ew")

        ttk.Button(actions, text="Выполнено", command=...).grid(row=0, column=0, padx=(0,8))
        ttk.Button(actions, text="Удалить", command=...).grid(row=0, column=1, padx=(0,8))
        ttk.Button(actions, text="Сохранить", command=self._save_tasks).grid(row=0, column=2, padx=(0,8))
        ttk.Button(actions, text="Сбросить все", command=...).grid(row=0, column=3, padx=(0,8))

        footer = ttk.Frame(self.root, padding=(12,6,12,12))
        footer.grid(row=3, column=0, sticky="ew")
        ttk.Label(footer, textvariable=self.stats_var).grid(row=0, column=0, sticky="w")

    def _clear_form(self) -> None:
        self.title_var.set("")
        self.deadline_var.set("")
        self.priority_var.set(PRIORITIES[1])

    def _add_task(self) -> None:
        try:
            self.service.add_task(
                self.title_var.get(),
                self.deadline_var.get(), 
                self.priority_var.get()
            )
        except ValueError as error:
            messagebox.showerror("Ошибка", str(error))
            return 

        self._clear_form()
        self._refresh_tasks()


    def _save_tasks(self) -> None: 
        self.service.save()
        messagebox.showinfo("Сохранение", "Задачи сохранены в tasks.json")


    def _refresh_tasks(self) -> None:
        self.listbox.delete(0, tk.END)
        self.visible_indexes.clear()

        for visible_position, (task_index, task) in enumerate(self.service.get_tasks(self.filter_var.get())):
            self.visible_indexes.append(task_index)
            self.listbox.insert(tk.END, task.display_text())
            self._paint_task(visible_position, task.priority, task.done)


        total_count, done_count = self.service.statistics()
        self.stats_var.set(f"Всего задач: {total_count} | Выполнено: {done_count}")


    def _paint_task(self, visible_position: int, priority: str, done: bool) -> None:
        if done:
            self.listbox.itemconfig(visible_position, foreground="#777777")
            return 

        colors = {
            "Низкий": "#1f7a3f",
            "Средний": "#9f6500",
            "Высокий": "#b42318"
        }

        self.listbox.itemconfig(visible_position, foreground=colors.get(priority, "#000000"))


    def _reset_tasks(self) -> None:
        if not self.service.tasks:
            return 

        confirmed = messagebox.askyesno("Подтверждение", "Удалить все задачи?")
        if not confirmed:
            return 

        self.service.reset_tasks()


