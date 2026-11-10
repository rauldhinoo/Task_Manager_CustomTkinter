import customtkinter as ctk
import json
from pathlib import Path
from datetime import datetime

# -------------------- Configuration --------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

DATA_FILE = Path(__file__).with_name("tasks.json")


class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Task Manager")
        self.geometry("900x680")
        self.minsize(720, 560)

        self.tasks = self.load_tasks()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_input_panel()
        self.create_task_panel()
        self.create_log_panel()

        self.refresh_tasks()
        self.log("Application started")

    # -------------------- Data --------------------
    def load_tasks(self):
        if not DATA_FILE.exists():
            return []
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def save_tasks(self):
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=4, ensure_ascii=False)

    # -------------------- UI layout --------------------
    def create_header(self):
        header = ctk.CTkFrame(self, corner_radius=12)
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text="My Task Manager",
            font=ctk.CTkFont(size=26, weight="bold")
        ).grid(row=0, column=0, padx=18, pady=(14, 2), sticky="w")

        ctk.CTkLabel(
            header, text="A simple productivity dashboard",
            text_color=("gray40", "gray70")
        ).grid(row=1, column=0, padx=18, pady=(0, 14), sticky="w")

        self.status_label = ctk.CTkLabel(
            header, text="● READY", text_color="#16A34A",
            font=ctk.CTkFont(weight="bold")
        )
        self.status_label.grid(row=0, column=1, rowspan=2, padx=20)

    def create_input_panel(self):
        panel = ctk.CTkFrame(self, corner_radius=12)
        panel.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel, text="Add a new task",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=(13, 8), sticky="w")

        self.task_entry = ctk.CTkEntry(
            panel, placeholder_text="Example: Practice Python for 30 minutes"
        )
        self.task_entry.grid(row=1, column=0, padx=(15, 8), pady=(0, 15), sticky="ew")
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        ctk.CTkButton(
            panel, text="+ Add Task", width=125, command=self.add_task
        ).grid(row=1, column=1, padx=(0, 15), pady=(0, 15))

    def create_task_panel(self):
        panel = ctk.CTkFrame(self, corner_radius=12)
        panel.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(panel, fg_color="transparent")
        top.grid(row=0, column=0, padx=15, pady=12, sticky="ew")
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top, text="My Tasks",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        self.stats_label = ctk.CTkLabel(top, text="Total: 0 | Done: 0 | Pending: 0")
        self.stats_label.grid(row=0, column=1, padx=8)

        ctk.CTkButton(
            top, text="Clear completed", width=125, fg_color="#64748B",
            hover_color="#475569", command=self.clear_completed
        ).grid(row=0, column=2, padx=(8, 0))

        self.task_list = ctk.CTkScrollableFrame(panel, corner_radius=8)
        self.task_list.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.task_list.grid_columnconfigure(0, weight=1)

    def create_log_panel(self):
        panel = ctk.CTkFrame(self, corner_radius=12)
        panel.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel, text="Activity Log",
            font=ctk.CTkFont(size=15, weight="bold")
        ).grid(row=0, column=0, padx=15, pady=(10, 4), sticky="w")

        self.log_box = ctk.CTkTextbox(panel, height=90, state="disabled")
        self.log_box.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="ew")

    # -------------------- Actions --------------------
    def add_task(self):
        title = self.task_entry.get().strip()

        if not title:
            self.status_label.configure(text="● INPUT REQUIRED", text_color="#D97706")
            self.log("Add task failed: task name is empty")
            return

        task = {
            "title": title,
            "done": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        self.task_entry.delete(0, "end")
        self.status_label.configure(text="● TASK ADDED", text_color="#16A34A")
        self.log(f"Task added: {title}")
        self.refresh_tasks()

    def toggle_task(self, index):
        self.tasks[index]["done"] = not self.tasks[index].get("done", False)
        state = "completed" if self.tasks[index]["done"] else "pending"
        self.save_tasks()
        self.log(f"Task marked as {state}: {self.tasks[index]['title']}")
        self.refresh_tasks()

    def delete_task(self, index):
        title = self.tasks[index]["title"]
        del self.tasks[index]
        self.save_tasks()
        self.log(f"Task deleted: {title}")
        self.refresh_tasks()

    def clear_completed(self):
        before = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task.get("done", False)]
        removed = before - len(self.tasks)
        self.save_tasks()
        self.log(f"Cleared {removed} completed task(s)")
        self.refresh_tasks()

    # -------------------- Display updates --------------------
    def refresh_tasks(self):
        for widget in self.task_list.winfo_children():
            widget.destroy()

        if not self.tasks:
            ctk.CTkLabel(
                self.task_list, text="No tasks yet. Add your first task above.",
                text_color=("gray40", "gray70")
            ).grid(row=0, column=0, padx=10, pady=25)
        else:
            for index, task in enumerate(self.tasks):
                row = ctk.CTkFrame(self.task_list, corner_radius=8)
                row.grid(row=index, column=0, padx=3, pady=4, sticky="ew")
                row.grid_columnconfigure(1, weight=1)

                checkbox = ctk.CTkCheckBox(
                    row, text="", width=24,
                    command=lambda i=index: self.toggle_task(i)
                )
                checkbox.grid(row=0, column=0, padx=(12, 8), pady=12)
                if task.get("done", False):
                    checkbox.select()

                title_color = ("gray50", "gray60") if task.get("done", False) else ("gray10", "gray90")
                title_label = ctk.CTkLabel(
                    row, text=task["title"], anchor="w",
                    text_color=title_color
                )
                title_label.grid(row=0, column=1, padx=5, sticky="ew")

                state_text = "DONE" if task.get("done", False) else "PENDING"
                state_color = "#16A34A" if task.get("done", False) else "#D97706"
                ctk.CTkLabel(
                    row, text=state_text, text_color=state_color,
                    font=ctk.CTkFont(size=11, weight="bold")
                ).grid(row=0, column=2, padx=10)

                ctk.CTkButton(
                    row, text="Delete", width=65, height=28,
                    fg_color="#B91C1C", hover_color="#991B1B",
                    command=lambda i=index: self.delete_task(i)
                ).grid(row=0, column=3, padx=(0, 10), pady=8)

        total = len(self.tasks)
        done = sum(1 for task in self.tasks if task.get("done", False))
        pending = total - done
        self.stats_label.configure(
            text=f"Total: {total} | Done: {done} | Pending: {pending}"
        )

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{timestamp}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
