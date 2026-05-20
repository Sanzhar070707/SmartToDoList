import datetime

class Task:
    def __init__(self, task_id, title, description, deadline, is_completed=False):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.is_completed = is_completed
        self.type = "regular"

    def get_date_status(self):
        try:
            deadline_date = datetime.datetime.strptime(self.deadline, "%Y-%m-%d").date()
            today = datetime.date.today()
            if deadline_date < today:
                return "overdue"
            elif deadline_date == today:
                return "today"
            return "normal"
        except (ValueError, TypeError):
            return "normal"


class UrgentTask(Task):
    def __init__(self, task_id, title, description, deadline, urgency_level="Medium", is_completed=False):
        super().__init__(task_id, title, description, deadline, is_completed)
        self.urgency_level = urgency_level
        self.type = "urgent"


class TaskFilter:
    @staticmethod
    def get_urgent_generator(tasks_list):
        for task in tasks_list:
            if task.type == "urgent" and not task.is_completed:
                yield task