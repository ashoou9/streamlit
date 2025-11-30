import streamlit as st
import warnings
import logging
import os
import sys

# ----------------------------
# Hide Warnings and Streamlit Logs
# ----------------------------
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)
os.environ["PYTHONWARNINGS"] = "ignore"

# ----------------------------
# Users Database
# ----------------------------
users = {
    "ahmed": {"password": "2811", "role": "Admin"},
    "david": {"password": "1234", "role": "User"}
}

# ----------------------------
# Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

# ----------------------------
# Login Function
# ----------------------------
def login(username, password):
    username = username.lower()  # ignore case
    if username in users:
        if users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user_role = users[username]["role"]
            st.session_state.username = username
            return True
    return False

# ----------------------------
# Logout Function
# ----------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

# ----------------------------
# UI
# ----------------------------
st.title("🔐 Login Page")

if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.success("✅ Login Successful")
            st.rerun()
        else:
            st.error("❌ Wrong Username or Password")

else:
    st.success(f"Welcome {st.session_state.username.upper()} 👋")
    st.info(f"Your Role: {st.session_state.user_role}")

    # Role-Based Pages
    if st.session_state.user_role == "Admin":
        st.subheader("🧑‍💼 Admin Dashboard")
        st.write("✅ You can see ALL data")
        st.write("✅ You can manage users")
        st.write("✅ Full control")

    elif st.session_state.user_role == "User":
        st.subheader("👤 User Dashboard")
        st.write("✅ You can see only your data")
        st.write("✅ Limited access")

    if st.button("Logout"):
        logout()
        st.rerun()
