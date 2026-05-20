from flask import Flask, render_template, request, redirect, url_for
import json
import os
import datetime
from models import Task, UrgentTask, TaskFilter

app = Flask(__name__)
DATA_FILE = 'data/tasks.json'


def load_tasks_from_json():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks_to_json(tasks):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def get_all_tasks():
    raw_data = load_tasks_from_json()
    objects_list = []
    for t in raw_data:
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


@app.route('/')
def index():
    all_tasks = get_all_tasks()
    active_tasks = [t for t in all_tasks if not t.is_completed]
    return render_template('index.html', tasks=active_tasks)


@app.route('/analytics')
def analytics():
    all_tasks = get_all_tasks()
    total = len(all_tasks)
    completed = sum(1 for t in all_tasks if t.is_completed)
    overdue = sum(1 for t in all_tasks if not t.is_completed and t.get_date_status() == "overdue")

    efficiency = int((completed / total) * 100) if total > 0 else 0
    return render_template('analytics.html', total=total, completed=completed, overdue=overdue, efficiency=efficiency)


@app.route('/urgent')
def urgent_page():
    all_tasks = get_all_tasks()
    urgent_generator = TaskFilter.get_urgent_generator(all_tasks)
    urgent_tasks = list(urgent_generator)
    return render_template('urgent.html', tasks=urgent_tasks)


@app.route('/history')
def history_page():
    all_tasks = get_all_tasks()
    completed_tasks = [t for t in all_tasks if t.is_completed]
    return render_template('history.html', tasks=completed_tasks)


@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    deadline = request.form.get('deadline')
    is_urgent = request.form.get('is_urgent') == 'on'
    urgency_level = request.form.get('urgency_level', 'Medium')

    raw_tasks = load_tasks_from_json()
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