import streamlit as st
import warnings
import logging
import os
import pandas as pd
from datetime import datetime

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
    "david": {"password": "1234", "role": "User"},
    "nahla": {"password": "0000", "role": "User"}
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
    username = username.lower()
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
# File storage path
# ----------------------------
BASE_PATH = "data"

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

    # ----------------------------
    # Admin Dashboard
    # ----------------------------
    if st.session_state.user_role == "Admin":
        st.subheader("🧑‍💼 Admin Dashboard")
        st.write("✅ You can see ALL data")
        st.write("✅ You can manage users")
        st.write("✅ Full control")

        # Upload Excel File
        uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
        if uploaded_file is not None:
            today_folder = os.path.join(BASE_PATH, datetime.today().strftime("%Y-%m-%d"))
            os.makedirs(today_folder, exist_ok=True)

            file_path = os.path.join(today_folder, uploaded_file.name)
            df = pd.read_excel(uploaded_file)
            df.to_excel(file_path, index=False)

            st.success(f"File uploaded successfully to {today_folder}!")
            st.dataframe(df)

    # ----------------------------
    # User Dashboard
    # ----------------------------
    elif st.session_state.user_role == "User":
        st.subheader("👤 User Dashboard")
        st.write("✅ You can see only your data")
        st.write("✅ Limited access")

        if os.path.exists(BASE_PATH):
            all_dates = sorted(os.listdir(BASE_PATH), reverse=True)
            for folder in all_dates:
                folder_path = os.path.join(BASE_PATH, folder)
                if os.path.isdir(folder_path):  # تأكد إنه فولدر
                    files = os.listdir(folder_path)
                    for file in files:
                        file_path = os.path.join(folder_path, file)
                        try:
                            df = pd.read_excel(file_path)
                            st.markdown(f"**{folder}/{file}**")
                            st.dataframe(df)
                        except Exception as e:
                            st.warning(f"Could not read {file}: {e}")
        else:
            st.warning("No data folder found yet.")

    if st.button("Logout"):
        logout()
        st.rerun()
