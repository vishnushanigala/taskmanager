import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from ttkthemes import ThemedTk

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    task_name TEXT NOT NULL,
    task_description TEXT,
    task_date TEXT NOT NULL
)
''')
conn.commit()

def register_user():
    username = username_entry.get()
    password = password_entry.get()
    
    if username and password:
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
    else:
        messagebox.showerror("Error", "Username and password are required!")

def login():
    username = login_username_entry.get()
    password = login_password_entry.get()
    
    if username and password:
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            open_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password!")
    else:
        messagebox.showerror("Error", "Username and password are required!")

def open_main_window():
    login_window.destroy()
    
    root = ThemedTk(theme="arc")
    root.title("Schedule Management App")

    ttk.Label(root, text="Task Name:").grid(row=0, column=0)
    global task_name_entry
    task_name_entry = ttk.Entry(root)
    task_name_entry.grid(row=0, column=1)

    ttk.Label(root, text="Task Description:").grid(row=1, column=0)
    global task_description_entry
    task_description_entry = tk.Text(root, height=5, width=30)
    task_description_entry.grid(row=1, column=1)

    ttk.Label(root, text="Task Date (YYYY-MM-DD):").grid(row=2, column=0)
    global task_date_entry
    task_date_entry = ttk.Entry(root)
    task_date_entry.grid(row=2, column=1)

    add_button = ttk.Button(root, text="Add Task", command=add_task)
    add_button.grid(row=3, column=0, columnspan=2)

    delete_button = ttk.Button(root, text="Delete Task", command=delete_task)
    delete_button.grid(row=4, column=0, columnspan=2)

    global tasks_list
    tasks_list = tk.Listbox(root, height=10, width=50)
    tasks_list.grid(row=5, column=0, columnspan=2)

    display_tasks()

    root.mainloop()

def add_task():
    task_name = task_name_entry.get()
    task_description = task_description_entry.get("1.0", tk.END).strip()
    task_date = task_date_entry.get()
    
    if task_name and task_date:
        cursor.execute("INSERT INTO tasks (task_name, task_description, task_date) VALUES (?, ?, ?)",
                       (task_name, task_description, task_date))
        conn.commit()
        messagebox.showinfo("Success", "Task added successfully!")
        clear_entries()
        display_tasks()
    else:
        messagebox.showerror("Error", "Task name and date are required!")

def clear_entries():
    task_name_entry.delete(0, tk.END)
    task_description_entry.delete("1.0", tk.END)
    task_date_entry.delete(0, tk.END)

def display_tasks():
    tasks_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    for row in rows:
        tasks_list.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Date: {row[3]}")

def delete_task():
    selected_task = tasks_list.curselection()
    if selected_task:
        task_id = int(selected_task[0]) + 1
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        messagebox.showinfo("Success", "Task deleted successfully!")
        display_tasks()
    else:
        messagebox.showerror("Error", "Please select a task to delete!")

login_window = ThemedTk(theme="arc")
login_window.title("Login")

ttk.Label(login_window, text="Username:").grid(row=0, column=0)
login_username_entry = ttk.Entry(login_window)
login_username_entry.grid(row=0, column=1)

ttk.Label(login_window, text="Password:").grid(row=1, column=0)
login_password_entry = ttk.Entry(login_window, show="*")
login_password_entry.grid(row=1, column=1)

register_button = ttk.Button(login_window, text="Register", command=register_user)
register_button.grid(row=2, column=0)

login_button = ttk.Button(login_window, text="Login", command=login)
login_button.grid(row=2, column=1)

def on_closing():
    login_window.destroy()
    conn.close()

login_window.protocol("WM_DELETE_WINDOW", on_closing)

login_window.mainloop()
