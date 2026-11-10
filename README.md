# My Task Manager — CustomTkinter

A simple desktop To-Do List project.

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
- Dark/light appearance follows the system setting

## What to study in this project

1. `class TodoApp(ctk.CTk)`: creating an application window with a class.
2. `CTkFrame`, `CTkLabel`, `CTkEntry`, `CTkButton`: building the interface.
3. `command=self.add_task`: connecting a button to a function.
4. `self.tasks`: storing task data in a list of dictionaries.
5. `refresh_tasks()`: updating the visible task list.
6. `json.load()` and `json.dump()`: saving and loading data.
7. `log()`: displaying activity messages.

The application creates `tasks.json` next to `main.py` after the first task is saved.
