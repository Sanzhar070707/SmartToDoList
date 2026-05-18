from flask import Flask, render_template, request, redirect, url_for
# Импортируем наши классы и функции из соседнего файла models.py
from models import Task, UrgentTask, load_tasks_from_file, save_tasks_to_file
import time

app = Flask(__name__)


@app.route('/')
def index():
    """Главная страница: загружает задачи и отображает их"""
    tasks = load_tasks_from_file()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    """Обработчик формы: создание новой задачи"""
    # Получаем данные из полей HTML-формы
    title = request.form.get('title')
    description = request.form.get('description')
    deadline = request.form.get('deadline')
    is_urgent = request.form.get('is_urgent')  # Получаем галочку "Срочно"
    urgency_level = request.form.get('urgency_level', 'High')

    if title and deadline:
        tasks = load_tasks_from_file()

        # Генерируем уникальный ID на основе текущего времени
        task_id = int(time.time() * 1000)

        # ООП в действии: выбираем, какой класс создать
        if is_urgent:
            new_task = UrgentTask(task_id, title, description, deadline, urgency_level)
        else:
            new_task = Task(task_id, title, description, deadline)

        tasks.append(new_task)
        save_tasks_to_file(tasks)  # Сохраняем обновленный список в JSON

    return redirect('/')


@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    """Маршрут для того, чтобы отметить задачу выполненной"""
    tasks = load_tasks_from_file()
    for task in tasks:
        if task.task_id == task_id:
            task.mark_as_done()  # Вызываем метод нашего класса Task
            break
    save_tasks_to_file(tasks)
    return redirect('/')


@app.route('/analytics')
def analytics():
    """Вторая страница: Аналитика и статистика задач"""
    tasks = load_tasks_from_file()
    total = len(tasks)
    completed = sum(1 for t in tasks if t.is_completed)

    # Считаем просроченные среди невыполненных
    overdue = sum(1 for t in tasks if t.get_date_status() == 'overdue')

    # Считаем процент выполнения, защищаясь от деления на ноль
    efficiency = round((completed / total) * 100) if total > 0 else 0

    return render_template('analytics.html', total=total, completed=completed, overdue=overdue, efficiency=efficiency)


if __name__ == '__main__':
    # Запуск сервера в режиме отладки (debug=True автоматически перезапускает сайт при изменениях)
    app.run(debug=True)