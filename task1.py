import json
import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# File to store tasks
TASKS_FILE = 'tasks.json'

# Load tasks from JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# CLI functions
def cli_add_task(tasks):
    task = input("Enter the task description: ").strip()
    if task:
        tasks.append({'task': task, 'done': False})
        save_tasks(tasks)
        print(f"Task '{task}' added.")
    else:
        print("Empty task not added.")

def cli_list_tasks(tasks):
    if not tasks:
        print("No tasks in your to-do list.")
        return
    print("\nYour Tasks:")
    for idx, task in enumerate(tasks, 1):
        status = '✓' if task['done'] else '✗'
        print(f"{idx}. [{status}] {task['task']}")
    print()

def cli_update_task(tasks):
    cli_list_tasks(tasks)
    try:
        idx = int(input("Enter task number to update: "))
        if 1 <= idx <= len(tasks):
            new_desc = input("Enter new description: ").strip()
            if new_desc:
                tasks[idx - 1]['task'] = new_desc
                save_tasks(tasks)
                print("Task updated.")
            else:
                print("Empty description. Update canceled.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def cli_mark_done(tasks):
    cli_list_tasks(tasks)
    try:
        idx = int(input("Enter task number to mark as done: "))
        if 1 <= idx <= len(tasks):
            tasks[idx - 1]['done'] = True
            save_tasks(tasks)
            print("Task marked as done.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def cli_delete_task(tasks):
    cli_list_tasks(tasks)
    try:
        idx = int(input("Enter task number to delete: "))
        if 1 <= idx <= len(tasks):
            removed_task = tasks.pop(idx - 1)
            save_tasks(tasks)
            print(f"Task '{removed_task['task']}' deleted.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def cli_main():
    tasks = load_tasks()
    while True:
        print("\n--- To-Do List CLI ---")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Mark Task as Done")
        print("5. Delete Task")
        print("6. Exit")
        choice = input("Select an option (1-6): ").strip()
        if choice == '1':
            cli_add_task(tasks)
        elif choice == '2':
            cli_list_tasks(tasks)
        elif choice == '3':
            cli_update_task(tasks)
        elif choice == '4':
            cli_mark_done(tasks)
        elif choice == '5':
            cli_delete_task(tasks)
        elif choice == '6':
            print("Exiting CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# GUI classes and functions
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List GUI")
        self.tasks = load_tasks()

        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        # Frame for listbox and scrollbar
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Listbox to display tasks
        self.listbox = tk.Listbox(frame, height=15, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Entry for new task
        self.entry = ttk.Entry(self.root, width=50)
        self.entry.pack(pady=5)

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)

        add_btn = ttk.Button(btn_frame, text="Add Task", command=self.add_task)
        add_btn.grid(row=0, column=0, padx=5)

        update_btn = ttk.Button(btn_frame, text="Update Selected", command=self.update_task)
        update_btn.grid(row=0, column=1, padx=5)

        mark_done_btn = ttk.Button(btn_frame, text="Mark as Done", command=self.mark_done)
        mark_done_btn.grid(row=0, column=2, padx=5)

        delete_btn = ttk.Button(btn_frame, text="Delete Selected", command=self.delete_task)
        delete_btn.grid(row=0, column=3, padx=5)

        refresh_btn = ttk.Button(btn_frame, text="Refresh List", command=self.refresh_task_list)
        refresh_btn.grid(row=0, column=4, padx=5)

    def refresh_task_list(self):
        self.tasks = load_tasks()
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = '✓' if task['done'] else '✗'
            display_text = f"[{status}] {task['task']}"
            self.listbox.insert(tk.END, display_text)

    def add_task(self):
        task_text = self.entry.get().strip()
        if task_text:
            self.tasks.append({'task': task_text, 'done': False})
            save_tasks(self.tasks)
            self.entry.delete(0, tk.END)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Input Error", "Please enter a task description.")

    def get_selected_index(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task.")
            return None
        return selected[0]

    def update_task(self):
        idx = self.get_selected_index()
        if idx is not None:
            current_task = self.tasks[idx]['task']
            new_task = simpledialog.askstring("Update Task", "Enter new task description:", initialvalue=current_task)
            if new_task:
                self.tasks[idx]['task'] = new_task.strip()
                save_tasks(self.tasks)
                self.refresh_task_list()

    def mark_done(self):
        idx = self.get_selected_index()
        if idx is not None:
            self.tasks[idx]['done'] = True
            save_tasks(self.tasks)
            self.refresh_task_list()

    def delete_task(self):
        idx = self.get_selected_index()
        if idx is not None:
            removed_task = self.tasks.pop(idx)
            save_tasks(self.tasks)
            self.refresh_task_list()

def run_gui():
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

# Main execution
if __name__ == '__main__':
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'cli':
            cli_main()
        elif mode == 'gui':
            run_gui()
        else:
            print("Invalid argument. Use 'cli' or 'gui'.")
            print("Example: python todo.py cli")
    else:
        # Default to CLI or GUI based on user preference
        print("Select mode:\n1. Command Line Interface (CLI)\n2. Graphical User Interface (GUI)")
        choice = input("Enter 1 or 2: ").strip()
        if choice == '1':
            cli_main()
        elif choice == '2':
            run_gui()
        else:
            print("Invalid choice. Exiting.")