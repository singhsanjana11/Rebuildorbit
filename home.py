import streamlit as st
import sqlite3
import bcrypt

# --- DB setup ---
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password_hash TEXT
    )
''')
conn.commit()


def register_user(username, email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                  (username, email, hashed))
        conn.commit()
        return True, "Registration successful! Please log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists."


def login_user(username, password):
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    if row and bcrypt.checkpw(password.encode(), row[0]):
        return True
    return False


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# --- Dialog for Login/Signup ---
@st.dialog("Log In / Sign Up")
def show_auth_form():
    mode = st.radio("Select Mode", ["Sign In", "Sign Up"])

    if mode == "Sign In":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign In"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    else:  # Sign Up
        reg_username = st.text_input("New Username")
        reg_email = st.text_input("Email")
        reg_password = st.text_input("New Password", type="password")
        if st.button("Sign Up"):
            success, msg = register_user(reg_username, reg_email, reg_password)
            if success:
                st.success(msg)
            else:
                st.error(msg)


# ---- ALWAYS-VISIBLE SECTIONS ----
with st.container():
    col1, col2 = st.columns(2, gap="large", vertical_alignment="center")
    with col1:
        st.title("Stop guessing. Start predicting.")
        st.write(
            "Upload customer data, run automated model selection, and export actionable results — all in one place.")
        if st.button("Login/SignUp"):
            show_auth_form()
    with col2:
        st.image("assets/dashboard.png", width=750)

st.markdown("---")

with st.container():
    st.title("Why Choose Us?")
    col3, col4, col5 = st.columns(3, gap="small", vertical_alignment="center")
    with col3:
        st.subheader("Multi-Industry, One Engine")
        st.write(
            "Whether you're in telecom, OTT, or publishing, our model adapts to your data structure and audience behavior—delivering insights that are industry-aware and platform-agnostic.")
    with col4:
        st.subheader("Pure Prediction, No Prescriptions")
        st.write(
            "We specialize in what others dilute—accurate churn forecasting. No bundled strategies, no distractions—just clean, data-driven predictions you can trust.")
    with col5:
        st.subheader("Built for Analysts, Loved by Orgs")
        st.write(
            "From dashboards to exportable scores, our system is designed for clarity and speed. You get the churn risk, the confidence level, and the customer list—ready for action.")

st.markdown("---")

with st.container():
    st.title("Track Your Churn")
    st.write(
        "Churn isn't random—it's often predictable. Customers disengage when they don't find value, face friction, or feel unheard. By analyzing patterns in your data, you can spot early warning signs and intervene before it's too late. Whether it's offering a personalized discount, improving onboarding, or simply reaching out at the right moment, data-driven decisions help you build smarter retention strategies.")
    st.image("assets/dashboard1.png", width="stretch")

st.markdown("---")

with st.container():
    col6, col7 = st.columns(2, gap="small", vertical_alignment="center")
    with col6:
        st.title("How it Works?")
    with col7:
        st.subheader("Follow three simple steps to generate predictions and export results.")
        st.write("1. Register or login to your account.")
        st.write("2. Upload CSV with customer features.")
        st.write("3. Run AutoML to train and generate predictions.")
        st.write("4. Review dashboard, download results, and act.")

col9, col10, col11 = st.columns([1, 1, 1])
with col10:
    if st.button("Predict Now"):
        show_auth_form()

st.markdown("---")

# ---- LOGGED-IN EXPERIENCE ----
if st.session_state.logged_in:
    st.success(f"Welcome back, {st.session_state.username}! You are now logged in.")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
