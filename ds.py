import streamlit as st
import warnings
import logging
import os
import pandas as pd
from datetime import datetime, date
import re  # لاستعمال regex لتقسيم اسم الملف

# ----------------------------
# Hide Warnings and Logs
# ----------------------------
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)
os.environ["PYTHONWARNINGS"] = "ignore"

# ----------------------------
# Users Database
# ----------------------------
users = {
    "ahmed": {"password": "2811", "role": "Admin"},
    "git 1": {"password": "1111", "role": "User"},
    "cns 2": {"password": "2222", "role": "User"},
    "all":   {"password": "9999", "role": "AllViewer"}
}

# ----------------------------
# Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

# ----------------------------
# Paths
# ----------------------------
BASE_PATH = "data"

# ----------------------------
# Helpers
# ----------------------------
def get_current_month_folders():
    if not os.path.exists(BASE_PATH):
        return []
    today = date.today().strftime("%Y-%m")
    folders = []
    for f in os.listdir(BASE_PATH):
        if f.startswith(today):
            folders.append(f)
    return sorted(folders, reverse=True)

def is_file_for_user(filename, username):
    """
    تتحقق إذا كان الملف يخص المستخدم.
    username لازم يكون lower case
    """
    name = filename.replace(".xlsx", "").replace(".xls", "").lower()
    # تقسيم الاسم على أي dash مع أو بدون مسافات
    parts = re.split(r"\s*-\s*", name)
    for part in parts:
        if username.lower() in part.strip():
            return True
    return False

# ----------------------------
# Login / Logout
# ----------------------------
def login(username, password):
    username = username.lower()
    if username in users and users[username]["password"] == password:
        st.session_state.logged_in = True
        st.session_state.user_role = users[username]["role"]
        st.session_state.username = username
        return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

# ----------------------------
# UI
# ----------------------------
st.title("🔐 Login Page")

if not st.session_state.logged_in:
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(u, p):
            st.rerun()
        else:
            st.error("Wrong login")

# =======================
# ✅ AFTER LOGIN
# =======================
else:
    st.success(f"Welcome {st.session_state.username.upper()} 👋")

    # ==================================================
    # ✅ ADMIN
    # ==================================================
    if st.session_state.user_role == "Admin":
        st.subheader("🧑‍💼 Admin Dashboard")

        uploaded_files = st.file_uploader(
            "Upload Excel Files",
            type=["xlsx", "xls"],
            accept_multiple_files=True
        )

        if uploaded_files:
            today_folder = os.path.join(BASE_PATH, datetime.today().strftime("%Y-%m-%d"))
            os.makedirs(today_folder, exist_ok=True)

            for file in uploaded_files:
                file_path = os.path.join(today_folder, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

            st.success("✅ Files uploaded successfully")

        # --------- History ----------
        st.markdown("---")
        selected_day = st.selectbox("Choose Day", get_current_month_folders())

        if selected_day:
            folder_path = os.path.join(BASE_PATH, selected_day)
            files = os.listdir(folder_path)

            for file in files:
                path = os.path.join(folder_path, file)
                c1, c2, c3 = st.columns([4,1,1])
                with c1:
                    st.write(file)
                with c2:
                    if st.button("👁", key=file):
                        df = pd.read_excel(path)
                        df = df.astype(str)  # حل مشكلة PyArrow
                        st.dataframe(df)
                with c3:
                    with open(path, "rb") as f:
                        st.download_button("⬇", f, file_name=file)

    # ==================================================
    # ✅ USER / ALLVIEWER
    # ==================================================
    elif st.session_state.user_role in ["User", "AllViewer"]:
        st.subheader("👤 User Dashboard")

        selected_day = st.selectbox("Choose Day", get_current_month_folders())

        if selected_day:
            folder_path = os.path.join(BASE_PATH, selected_day)
            files = os.listdir(folder_path)

            allowed_files = []
            for file in files:
                if st.session_state.user_role == "AllViewer":
                    allowed_files.append(file)
                elif is_file_for_user(file, st.session_state.username):
                    allowed_files.append(file)

            if allowed_files:
                chosen_file = st.selectbox("Choose File", allowed_files)
                path = os.path.join(folder_path, chosen_file)

                df = pd.read_excel(path)
                df = df.astype(str)  # حل مشكلة PyArrow
                st.dataframe(df)

                with open(path, "rb") as f:
                    st.download_button(
                        "⬇ Download Original File",
                        f,
                        file_name=chosen_file
                    )
            else:
                st.warning("No files for your line.")

    # -------- Logout ----------
    if st.button("Logout"):
        logout()
        st.rerun()
