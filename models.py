import datetime

# Базовый класс для обычной задачи
class Task:
    def __init__(self, task_id, title, description, deadline, is_completed=False):
        self.task_id = task_id  # Вернули твой родной task_id, чтобы не было ошибок!
        self.title = title
        self.description = description
        self.deadline = deadline
        self.is_completed = is_completed
        self.type = "regular"

    # Метод проверки дедлайна
    def get_date_status(self):
        try:
            deadline_date = datetime.datetime.strptime(self.deadline, "%Y-%m-%d").date()
            today = datetime.date.today()
            if deadline_date < today:
                return "overdue"  # Просрочено
            elif deadline_date == today:
                return "today"    # Сделать сегодня
            return "normal"
        except (ValueError, TypeError):
            return "normal"

# Дочерний класс для срочной задачи (Наследование строго по критериям!)
class UrgentTask(Task):
    def __init__(self, task_id, title, description, deadline, urgency_level="Medium", is_completed=False):
        # Наследуем базовые поля от родительского класса Task
        super().__init__(task_id, title, description, deadline, is_completed)
        self.urgency_level = urgency_level
        self.type = "urgent"

# Продвинутая концепция ООП: Класс-генератор (Advanced Concept по требованиям)
class TaskFilter:
    @staticmethod
    def get_urgent_generator(tasks_list):
        """Продвинутый генератор (yield), который поочередно выдает только важные задачи"""
        for task in tasks_list:
            if task.type == "urgent" and not task.is_completed:
                yield task