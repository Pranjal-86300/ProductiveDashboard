import pandas as pd
from datetime import datetime

def calculate_stats(df):
    if df.empty:
        return {"completed": 0, "pending": 0, "overdue": 0}
    
    today = datetime.today().date()
    df['due_date'] = pd.to_datetime(df['due_date']).dt.date

    completed = df[df['status'] == "Completed"].shape[0]
    pending = df[df['status'] == "Pending"].shape[0]
    overdue = df[(df['status'] == "Pending") & (df['due_date'] < today)].shape[0]

    return {"completed": completed, "pending": pending, "overdue": overdue}

def get_weekly_summary(df):
    if df.empty:
        return pd.DataFrame()

    df['date'] = pd.to_datetime(df['due_date'])
    df['status'] = df['status'].fillna('Pending')
    completed = df[df['status'] == "Completed"]
    weekly = completed.groupby(df['date'].dt.strftime('%Y-%m-%d')).size().reset_index(name='Tasks Completed')

    return weekly
