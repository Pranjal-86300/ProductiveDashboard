import time
import streamlit as st

def run_timer(minutes):
    total_seconds = minutes * 60
    start_time = time.time()
    end_time = start_time + total_seconds

    with st.empty():
        while time.time() < end_time:
            remaining = int(end_time - time.time())
            mins, secs = divmod(remaining, 60)
            st.metric("⏳ Time Left", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
    st.success("🎉 Time's up! Take a short break.")
