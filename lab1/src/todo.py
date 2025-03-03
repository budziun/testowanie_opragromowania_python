class TodoList:
    def __init__(self):
        self.active_tasks = []
        self.completed_tasks = []

    def add_task(self, task):
        self.active_tasks.append(task)

    def complete_task(self, task):
        if task in self.active_tasks:
            self.active_tasks.remove(task)
            self.completed_tasks.append(task)

    def get_active_tasks(self):
        return self.active_tasks

    def get_completed_tasks(self):
        return self.completed_tasks