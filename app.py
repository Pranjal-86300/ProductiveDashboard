import streamlit as st
import pandas as pd
from datetime import date
from db import init_db, get_tasks, add_task, update_task_status, delete_task
from tasks import suggest_tasks
from timer import run_timer
from stats import calculate_stats, get_weekly_summary

# Page setup
st.set_page_config("Smart Productivity Dashboard", layout="wide")
st.title("🧠 Smart Productivity Dashboard")
init_db()

# Navigation
menu = st.sidebar.radio("Go to", ["📋 Task Manager", "⏳ Focus Timer", "📊 Productivity Stats", "🧠 Smart Suggestions"])

# --- 📋 Task Manager ---
if menu == "📋 Task Manager":
    st.subheader("Manage Your Tasks")

    # Task input form
    with st.form("task_form", clear_on_submit=True):
        task = st.text_input("Task Title")
        due = st.date_input("Due Date", date.today())
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        submitted = st.form_submit_button("Add Task")
        if submitted and task.strip():
            add_task(task.strip(), priority, due)
            st.success("✅ Task added successfully!")

    # Display tasks
    df = get_tasks()
    if df.empty:
        st.info("You have no tasks yet. Add one above!")
    else:
        st.markdown("### Your Tasks")
        for _, row in df.iterrows():
            cols = st.columns([3, 1, 1, 1, 1])
            cols[0].markdown(f"**{row['task']}**")
            cols[1].markdown(row['priority'])
            cols[2].markdown(row['due_date'])
            if cols[3].checkbox("Done", value=row['status'] == "Completed", key=f"done{row['id']}"):
                update_task_status(row['id'], "Completed")
            if cols[4].button("🗑", key=f"del{row['id']}"):
                delete_task(row['id'])
                st.experimental_rerun()

# --- ⏳ Focus Timer ---
elif menu == "⏳ Focus Timer":
    st.subheader("Pomodoro Focus Timer")
    minutes = st.number_input("Duration (minutes)", min_value=1, max_value=60, value=25)
    if st.button("Start Timer"):
        run_timer(minutes)

# --- 📊 Productivity Stats ---
elif menu == "📊 Productivity Stats":
    st.subheader("Task Completion Overview")
    df = get_tasks()
    stats = calculate_stats(df)
    st.write(f"✅ Completed: {stats['completed']} | ❌ Pending: {stats['pending']} | 🕒 Overdue: {stats['overdue']}")

    # Bar chart of status
    st.bar_chart(pd.DataFrame({
        "Tasks": [stats["completed"], stats["pending"], stats["overdue"]],
    }, index=["Completed", "Pending", "Overdue"]))

    # Weekly line chart
    weekly_df = get_weekly_summary(df)
    if not weekly_df.empty:
        st.line_chart(weekly_df.set_index('date'))
    else:
        st.info("Not enough completed tasks to show weekly progress.")

# --- 🧠 Smart Suggestions ---
elif menu == "🧠 Smart Suggestions":
    st.subheader("Top 3 Tasks You Should Focus On Today")
    df = get_tasks()
    suggestions = suggest_tasks(df)
    if not suggestions.empty:
        for _, row in suggestions.iterrows():
            st.markdown(f"➡️ **{row['task']}** (Priority: `{row['priority']}`, Due: `{row['due_date']}`)")
    else:
        st.info("No high-priority or urgent tasks for today.")

    # Export all tasks
    st.download_button("📤 Download All Tasks (CSV)", df.to_csv(index=False), "tasks.csv")
