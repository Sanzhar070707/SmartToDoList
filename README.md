
# Smart To-Do List (Flask Web Application)

A lightweight and efficient web application built with Flask for local task management, deadline tracking, and personal productivity analysis. This project is developed as part of the Object-Oriented Programming (OOP) course.

## Core Features
* **Task Management (CRUD Layout):** Add regular and urgent tasks with strict deadlines without duplicates or errors.
* **Modular Reusable Templates:** Implements layout inheritance via Jinja2 (`base.html`) to eliminate redundant HTML code.
* **Advanced OOP Concepts:** Uses strict class inheritance (`UrgentTask` inherits from `Task`) and lazy evaluation utilizing Python generators (`yield`) for high-performance data filtering.
* **Robustness & Error Handling:** Full exception handling blocks (`try-except`) for safe database file I/O operations preventing runtime crashes.
* **Interactive Analytics Dashboard:** Real-time generation of operational metrics including completion rates and overdue tracking.

## Technologies Used
* **Backend:** Python 3.11, Flask Framework
* **Frontend:** HTML5, CSS3 (Adaptive Grid & Flexbox layouts), Jinja2 Templates
* **Data Persistence:** Local structural JSON storage (`data/tasks.json`)

## Architecture Structure
* `app.py` — Core application server, handling routes and request processing.
* `models.py` — OOP class structures, properties inheritance, and filtering generators logic.
* `templates/` — UI templates folder implementing modular design structures.
  * `base.html` — Global shared layout blueprint containing core styles and nav bars.
  * `index.html` — Main board layout managing current active tasks grid.
  * `urgent.html` — Specialized layout displaying prioritized items fetched by generators.
  * `history.html` — Archive dashboard storing successfully closed operations.
  * `analytics.html` — Statistical visualization page calculating real-time execution indexes.

## How to Run the Project Locally
1. Clone the public GitHub repository by running: **git clone https://github.com/Sanzhar070707/SmartToDoList.git**
2. Navigate to the project root folder by running: **cd SmartToDoList**
3. Install the standard Flask library dependency by running: **pip install flask**
4. Fire up the backend application server by running: **python app.py**
5. Launch your internet browser and navigate to the local address: **http://127.0.0.1:5000/**