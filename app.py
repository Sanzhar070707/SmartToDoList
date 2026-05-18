from flask import Flask, render_template, request, redirect, url_for
import json
import os
import datetime
from models import Task, UrgentTask, TaskFilter

app = Flask(__name__)
DATA_FILE = 'data/tasks.json'


# Безопасное чтение файла (Критерий Robustness - обработка исключений)
def load_tasks_from_json():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []  # Если файл пуст или поврежден, приложение не падает, а возвращает пустой список


# Сохранение данных
def save_tasks_to_json(tasks):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


# Превращение сырых данных из JSON в объекты ООП (с защитой от KeyError)
def get_all_tasks():
    raw_data = load_tasks_from_json()
    objects_list = []
    for t in raw_data:
        # Используем .get(), чтобы если какого-то поля нет, программа не падала
        t_id = t.get('task_id') if t.get('task_id') is not None else t.get('id', 0)
        title = t.get('title', 'Без названия')
        description = t.get('description', '')
        deadline = t.get('deadline', str(datetime.date.today()))
        is_completed = t.get('is_completed', False)

        if t.get('type') == 'urgent':
            urgency_level = t.get('urgency_level', 'Medium')
            objects_list.append(UrgentTask(t_id, title, description, deadline, urgency_level, is_completed))
        else:
            objects_list.append(Task(t_id, title, description, deadline, is_completed))
    return objects_list


# ================= МАРШРУТЫ (СТРАНИЦЫ ПРИЛОЖЕНИЯ) =================

# 1. ГЛАВНАЯ СТРАНИЦА: Список всех активных задач
@app.route('/')
def index():
    all_tasks = get_all_tasks()
    # Показываем только те, которые еще не выполнены
    active_tasks = [t for t in all_tasks if not t.is_completed]
    return render_template('index.html', tasks=active_tasks)


# 2. СТРАНИЦА СТАТИСТИКИ (АНАЛИТИКА)
@app.route('/analytics')
def analytics():
    all_tasks = get_all_tasks()
    total = len(all_tasks)
    completed = sum(1 for t in all_tasks if t.is_completed)
    overdue = sum(1 for t in all_tasks if not t.is_completed and t.get_date_status() == "overdue")

    efficiency = int((completed / total) * 100) if total > 0 else 0
    return render_template('analytics.html', total=total, completed=completed, overdue=overdue, efficiency=efficiency)


# 3. СТРАНИЦА СРОЧНЫХ ЗАДАЧ (Использование нашего продвинутого ООП-генератора)
@app.route('/urgent')
def urgent_page():
    all_tasks = get_all_tasks()
    # Вызываем генератор через yield для фильтрации срочных задач
    urgent_generator = TaskFilter.get_urgent_generator(all_tasks)
    urgent_tasks = list(urgent_generator)  # Превращаем результат генератора в список для вывода
    return render_template('urgent.html', tasks=urgent_tasks)


# 4. СТРАНИЦА ИСТОРИИ (Архив выполненных задач)
@app.route('/history')
def history_page():
    all_tasks = get_all_tasks()
    completed_tasks = [t for t in all_tasks if t.is_completed]
    return render_template('history.html', tasks=completed_tasks)


# ================= ВСПOМОГАТЕЛЬНАЯ ЛОГИКА (ФУНКЦИИ) =================

# Добавление новой задачи
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    deadline = request.form.get('deadline')
    is_urgent = request.form.get('is_urgent') == 'on'
    urgency_level = request.form.get('urgency_level', 'Medium')

    raw_tasks = load_tasks_from_json()
    # Генерируем новый task_id
    new_id = max([t.get('task_id', t.get('id', 0)) for t in raw_tasks], default=0) + 1

    new_task_dict = {
        "task_id": new_id,
        "title": title,
        "description": description,
        "deadline": deadline,
        "is_completed": False,
        "type": "urgent" if is_urgent else "regular",
        "urgency_level": urgency_level if is_urgent else None
    }
    raw_tasks.append(new_task_dict)
    save_tasks_to_json(raw_tasks)
    return redirect(url_for('index'))


# Отметка задачи как выполненной
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    raw_tasks = load_tasks_from_json()
    for t in raw_tasks:
        t_id = t.get('task_id') if t.get('task_id') is not None else t.get('id')
        if t_id == task_id:
            t['is_completed'] = True
    save_tasks_to_json(raw_tasks)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)