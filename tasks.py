from datetime import datetime, timedelta
import pandas as pd

def suggest_tasks(df):
    if df.empty:
        return pd.DataFrame()

    df['due_date'] = pd.to_datetime(df['due_date']).dt.date
    today = datetime.today().date()
    df = df[df['status'] == "Pending"]

    urgent = df[df['due_date'] <= today]
    high_priority = df[df['priority'] == "High"]
    upcoming = df[df['due_date'] <= today + timedelta(days=1)]

    suggested = pd.concat([urgent, high_priority, upcoming]).drop_duplicates()
    return suggested.sort_values(by=['due_date', 'priority']).head(3)

def get_stats():
    today = datetime.today().date()
    stats = {"completed": 0, "pending": 0, "overdue": 0}

    df = pd.read_csv("data/tasks.csv") if not pd.read_sql else None
    df = df if df is not None else pd.DataFrame()

    try:
        df['due_date'] = pd.to_datetime(df['due_date']).dt.date
        stats['completed'] = len(df[df['status'] == "Completed"])
        stats['pending'] = len(df[df['status'] == "Pending"])
        stats['overdue'] = len(df[(df['status'] == "Pending") & (df['due_date'] < today)])
    except:
        pass
    return stats
