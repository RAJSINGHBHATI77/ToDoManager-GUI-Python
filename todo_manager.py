import tkinter as tk
from tkinter import messagebox
import csv
import os

FILE_NAME = 'tasks.csv'

def save_task(task):
    with open(FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(task)

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as f:
        return list(csv.reader(f))

def refresh_task_list():
    task_list.delete(0, tk.END)
    for idx, task in enumerate(load_tasks()):
        status = "✅" if task[2] == "Done" else "❌"
        task_list.insert(tk.END, f"{idx+1}. {task[0]} - {task[1]} ({status})")

def add_task():
    title = entry_title.get()
    desc = entry_desc.get()
    if not title or not desc:
        messagebox.showwarning("Input Error", "Please enter both title and description.")
        return
    save_task([title, desc, "Pending"])
    entry_title.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    refresh_task_list()

def mark_done():
    selected = task_list.curselection()
    if not selected:
        messagebox.showinfo("No Selection", "Please select a task.")
        return
    tasks = load_tasks()
    index = selected[0]
    tasks[index][2] = "Done"
    with open(FILE_NAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(tasks)
    refresh_task_list()

# GUI setup
root = tk.Tk()
root.title("To-Do Manager")

tk.Label(root, text="Task Title").pack()
entry_title = tk.Entry(root)
entry_title.pack()

tk.Label(root, text="Description").pack()
entry_desc = tk.Entry(root)
entry_desc.pack()

tk.Button(root, text="Add Task", command=add_task).pack(pady=5)
tk.Button(root, text="Mark as Done", command=mark_done).pack()

task_list = tk.Listbox(root, width=50)
task_list.pack(pady=10)
refresh_task_list()

root.mainloop()
