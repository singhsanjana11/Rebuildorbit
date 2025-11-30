import streamlit as st
import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

if not st.session_state.get("logged_in", False):
    st.warning("Please log in on the Home page to view your profile.")
    st.stop()

username = st.session_state.get("username")

st.title("My Profile")
st.write(f"Welcome, {username}!")

# --- Load basic user info ---
c.execute("SELECT email FROM users WHERE username = ?", (username,))
row = c.fetchone()
email = row[0] if row else ""

new_email = st.text_input("Email", value=email)

if st.button("Update Profile"):
    c.execute("UPDATE users SET email = ? WHERE username = ?", (new_email, username))
    conn.commit()
    st.success("Profile updated!")

st.markdown("---")

# --- Prediction history (if you create these tables) ---
st.subheader("My Prediction Runs")

c.execute("""
    CREATE TABLE IF NOT EXISTS prediction_run (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        run_type TEXT,        -- 'single' or 'batch'
        run_time TEXT,
        source_file_name TEXT,
        total_records INTEGER
    )
""")
conn.commit()

c.execute("SELECT run_time, run_type, source_file_name, total_records FROM prediction_run WHERE username = ? ORDER BY run_time DESC", (username,))
rows = c.fetchall()

if rows:
    import pandas as pd
    runs_df = pd.DataFrame(rows, columns=["Run Time", "Type", "File Name", "Total Records"])
    st.dataframe(runs_df)
else:
    st.info("No prediction runs recorded yet.")
