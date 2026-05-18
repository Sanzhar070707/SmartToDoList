from datetime import datetime
import json
import os

FILE_PATH = os.path.join("data", "tasks.json")


class Task:
    """Базовый класс для описания обычной задачи (Родительский класс)"""

    def __init__(self, task_id, title, description, deadline):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.is_completed = False

    def mark_as_done(self):
        """Метод для изменения статуса задачи на 'Выполнено'"""
        self.is_completed = True

    def get_date_status(self):
        """Возвращает статус дедлайна: 'overdue' (просрочено), 'today' (сегодня) или 'normal'"""
        if self.is_completed:
            return "normal"
        try:
            # Превращаем строку "ГГГГ-ММ-ДД" в реальный объект даты
            deadline_date = datetime.strptime(self.deadline, "%Y-%m-%d").date()
            today = datetime.today().date()

            if deadline_date < today:
                return "overdue"
            elif deadline_date == today:
                return "today"
            return "normal"
        except Exception:
            return "normal"

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "is_completed": self.is_completed,
            "type": "regular"
        }


class UrgentTask(Task):
    """Класс для срочных задач, который наследуется от Task (Класс-наследник)"""

    def __init__(self, task_id, title, description, deadline, urgency_level="High"):
        super().__init__(task_id, title, description, deadline)
        self.urgency_level = urgency_level

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "urgent"
        data["urgency_level"] = self.urgency_level
        return data


# --- Функции работы с файлом ---

def save_tasks_to_file(tasks_list):
    try:
        dict_tasks = [task.to_dict() for task in tasks_list]
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(dict_tasks, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка сохранения: {e}")


def load_tasks_from_file():
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            dict_tasks = json.load(file)
        loaded_tasks = []
        for item in dict_tasks:
            if item.get("type") == "urgent":
                task = UrgentTask(item["task_id"], item["title"], item["description"], item["deadline"],
                                  item.get("urgency_level", "High"))
            else:
                task = Task(item["task_id"], item["title"], item["description"], item["deadline"])
            if item.get("is_completed"):
                task.mark_as_done()
            loaded_tasks.append(task)
        return loaded_tasks
    except Exception:
        return []