# Task Manager — CustomTkinter

![Task Manager GUI](./assets/docs/Task-Manager-GUI.png)
![Task Manager GUI - Adding a task](./assets/docs/Task-Manager-GUI_adding-a-task.png)
![Task Manager GUI - Completing a task](./assets/docs/Task-Manager-GUI_completing-a-task.png)

A simple desktop Task Manager project.

## 1. Install

```bash
python -m pip install -r requirements.txt
```

Or:

```bash
python -m pip install customtkinter
```

## 2. Run

```bash
python main.py
```

## Features

- Add tasks
- Mark tasks as completed / pending
- Delete individual tasks
- Clear all completed tasks
- Live task statistics
- Activity log
- Save and load tasks using `tasks.json`
- Dark appearance

The application creates `tasks.json` next to `main.py` after the first task is saved.
