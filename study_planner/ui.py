import tkinter as tk 
from .storage import JsonTaskRepository
from .config import FILTERS, PRIORITIES, TASKS_FILE

class StudyPlannerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Study Planner")
        self.root.geometry("760x520")
        self.root.minsize(640, 440)

        repository = JsonTaskRepository(TASKS_FILE)

        self.title_var= tk.StringVar()
        self.deadline_var = tk.StringVar()
        self.priority_var = tk.StringVar(value=PRIORITIES[1])
        self.filter_var = tk.StringVar(value=FILTERS[0])
        self.stats_var = tk.StringVar()

    def run(self) -> None:
        self.root.mainloop()


    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)