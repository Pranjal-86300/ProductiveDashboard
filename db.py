import sqlite3
import pandas as pd

def connect():
    return sqlite3.connect("data/tasks.db", check_same_thread=False)

def init_db():
    conn = connect()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT,
            priority TEXT,
            due_date TEXT,
            status TEXT DEFAULT "Pending"
        )
    ''')
    conn.commit()
    conn.close()

def add_task(task, priority, due_date):
    conn = connect()
    conn.execute("INSERT INTO tasks (task, priority, due_date) VALUES (?, ?, ?)", (task, priority, due_date))
    conn.commit()
    conn.close()

def get_tasks():
    conn = connect()
    df = pd.read_sql_query("SELECT * FROM tasks ORDER BY due_date", conn)
    conn.close()
    return df

def update_task_status(task_id, status):
    conn = connect()
    conn.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = connect()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
