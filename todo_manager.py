import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

FILE_NAME = "tasks.csv"

# Load tasks from CSV
def load_tasks():
    tasks = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            tasks = list(reader)
    return tasks

# Save tasks to CSV
def save_tasks(tasks):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(tasks)

# Refresh the task view
def refresh_tasks():
    tree.delete(*tree.get_children())
    for idx, task in enumerate(load_tasks(), start=1):
        tree.insert("", "end", values=(idx, task[0], task[1], task[2], task[3]))

# Add a new task
def add_task():
    title = entry_title.get().strip()
    desc = entry_desc.get().strip()
    priority = combo_priority.get()
    status = "Pending"
    if not title:
        messagebox.showerror("Input Error", "Task title is required.")
        return
    tasks = load_tasks()
    tasks.append([title, desc, priority, status])
    save_tasks(tasks)
    entry_title.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    combo_priority.set("Normal")
    refresh_tasks()

# Mark selected task as done
def mark_done():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a task to mark as done.")
        return
    item = tree.item(selected)
    values = item["values"]
    tasks = load_tasks()
    index = values[0] - 1
    tasks[index][3] = "Done"
    save_tasks(tasks)
    refresh_tasks()

# Delete selected task
def delete_task():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a task to delete.")
        return
    item = tree.item(selected)
    index = item["values"][0] - 1
    tasks = load_tasks()
    tasks.pop(index)
    save_tasks(tasks)
    refresh_tasks()

# Set up GUI
root = tk.Tk()
root.title("📋 Advanced To-Do Manager")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Task Title").grid(row=0, column=0)
entry_title = tk.Entry(frame, width=40)
entry_title.grid(row=0, column=1, columnspan=3)

tk.Label(frame, text="Description").grid(row=1, column=0)
entry_desc = tk.Entry(frame, width=40)
entry_desc.grid(row=1, column=1, columnspan=3)

tk.Label(frame, text="Priority").grid(row=2, column=0)
combo_priority = ttk.Combobox(frame, values=["Low", "Normal", "High"], width=15)
combo_priority.set("Normal")
combo_priority.grid(row=2, column=1)

tk.Button(frame, text="➕ Add Task", command=add_task).grid(row=3, column=1, pady=10)
tk.Button(frame, text="✅ Mark as Done", command=mark_done).grid(row=3, column=2)
tk.Button(frame, text="❌ Delete Task", command=delete_task).grid(row=3, column=3)

columns = ("#", "Title", "Description", "Priority", "Status")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)
tree.pack(padx=10, pady=10)

refresh_tasks()
root.mainloop()
