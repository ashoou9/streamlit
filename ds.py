import streamlit as st
import warnings
import logging
import os
import pandas as pd
from datetime import datetime, date
import re

# ======================================================
# 🎨 CUSTOM CSS DESIGN (FULL BACKGROUND WITHOUT IMAGE)
# ======================================================
page_bg = """
<style>
.stApp {
    background: #0f1a24;
    background-size: cover;
    position: relative;
    overflow: hidden;
}

/* 🔴 RED CURVE RIGHT SIDE */
.stApp:before {
    content: "";
    position: absolute;
    right: -300px;
    bottom: -200px;
    width: 900px;
    height: 900px;
    background: #d71920;
    border-radius: 50%;
    z-index: -1;
}

/* 🔺 RED TRIANGLES */
.red-triangle {
    width: 0;
    height: 0;
    border-left: 25px solid transparent;
    border-right: 25px solid transparent;
    border-bottom: 35px solid #d71920;
    position: absolute;
}

/* ⚪ WHITE TRIANGLES */
.white-triangle {
    width: 0;
    height: 0;
    border-left: 12px solid transparent;
    border-right: 12px solid transparent;
    border-top: 18px solid white;
    position: absolute;
    z-index: -1;
}

/* ⚪ DOT PATTERNS */
.dot-grid {
    position: absolute;
    display: grid;
    grid-template-columns: repeat(12, 10px);
    grid-gap: 6px;
    z-index: -1;
}
.dot-grid div {
    width: 6px;
    height: 6px;
    background: white;
    border-radius: 50%;
    opacity: 0.7;
    z-index: -1;
}

/* 🔒 LOGIN BOX IN CENTER */
.login-box {
    background: rgba(255, 255, 255, 0.1);
    padding: 40px;
    border-radius: 15px;
    width: 450px;
    margin: auto;
    margin-top: 200px;
    backdrop-filter: blur(4px);
    box-shadow: 0 0 25px rgba(0,0,0,0.3);
    z-index: 10;
}

.login-title {
    text-align: center;
    color: white;
    font-size: 45px;
    font-weight: bold;
    margin-bottom: 30px;
}

/* TEXT INPUT STYLE */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.8);
    padding: 10px;
    border-radius: 8px;
}
.stPasswordInput > div > div > input {
    background: rgba(255,255,255,0.8);
    padding: 10px;
    border-radius: 8px;
}
.stButton > button {
    background: #d71920;
    color: white;
    padding: 10px;
    font-size: 20px;
    border-radius: 8px;
    width: 100%;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Add triangles and dots
st.markdown("""
<div class="red-triangle" style="top: 120px; left: 820px;"></div>
<div class="white-triangle" style="top: 280px; left: 480px;"></div>
<div class="dot-grid" style="top: 200px; right: 200px;">
""" + "".join(["<div></div>" for _ in range(60)]) + """
</div>
""", unsafe_allow_html=True)

# ======================================================
# Hide warnings
# ======================================================
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)
os.environ["PYTHONWARNINGS"] = "ignore"

# ======================================================
# Users Database
# ======================================================
users = {
    "ahmed": {"password": "1001", "role": "Admin"},
    "CHC New": {"password": "1000", "role": "User"},
    "CNS 1": {"password": "0123", "role": "User"},
    "CNS 2": {"password": "9990", "role": "User"},
    "CNS 3": {"password": "6537", "role": "User"},
    "CNS 4": {"password": "2873", "role": "User"},
    "GIT 1": {"password": "1978", "role": "User"},
    "GIT 2": {"password": "5422", "role": "User"},
    "GIT 3": {"password": "1822", "role": "User"},
    "Primary Care": {"password": "2252", "role": "User"},
    "CVM": {"password": "0287", "role": "User"},
    "Power Team": {"password": "7211", "role": "User"},
    "DGU": {"password": "1619", "role": "User"},
    "DNU": {"password": "2938", "role": "User"},
    "Sildava": {"password": "1000", "role": "User"},
    "Ortho": {"password": "4090", "role": "User"},
    "All":   {"password": "9021", "role": "AllViewer"}
}

# ======================================================
# Session State
# ======================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

BASE_PATH = "data"

# ======================================================
# Helpers
# ======================================================
def get_current_month_folders():
    if not os.path.exists(BASE_PATH):
        return []
    today = date.today().strftime("%Y-%m")
    return sorted([f for f in os.listdir(BASE_PATH) if f.startswith(today)], reverse=True)

def is_file_for_user(filename, username):
    name = filename.replace(".xlsx", "").replace(".xls", "").lower()
    parts = re.split(r"\s*-\s*", name)
    return any(username.lower() in part.strip() for part in parts)

def read_excel_file(path):
    try:
        return pd.read_excel(path, engine="openpyxl")
    except:
        return pd.read_excel(path, engine="xlrd")

# ======================================================
# Login Functions
# ======================================================
def login(username, password):
    for user_key, user_data in users.items():
        if username.lower() == user_key.lower() and password == user_data["password"]:
            st.session_state.logged_in = True
            st.session_state.user_role = user_data["role"]
            st.session_state.username = user_key
            return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

# ======================================================
# UI
# ======================================================
st.title("Daily Sales")

if not st.session_state.logged_in:

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Daily Sales</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.rerun()
        else:
            st.error("❌ Wrong User Or Password")

    st.markdown('</div>', unsafe_allow_html=True)

# AFTER LOGIN
else:
    st.success(f"Welcome {st.session_state.username} 👋")

    # ---------------- Admin ----------------
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
                with open(os.path.join(today_folder, file.name), "wb") as f:
                    f.write(file.getbuffer())
            st.success("✅ Files uploaded successfully")

        st.markdown("---")
        selected_day = st.selectbox("Sales Day", get_current_month_folders())
        if selected_day:
            folder_path = os.path.join(BASE_PATH, selected_day)
            for file in os.listdir(folder_path):
                path = os.path.join(folder_path, file)
                c1, c2, c3 = st.columns([4,1,1])
                with c1: st.write(file)
                with c2:
                    if st.button("👁", key=file):
                        df = read_excel_file(path).astype(str)
                        st.dataframe(df)
                with c3:
                    with open(path, "rb") as f:
                        st.download_button("⬇ Download", f, file_name=file)

    # ---------------- User / AllViewer ----------------
    elif st.session_state.user_role in ["User", "AllViewer"]:
        st.subheader("👤 Sales Dashboard")
        selected_day = st.selectbox("Date", get_current_month_folders())
        if selected_day:
            folder_path = os.path.join(BASE_PATH, selected_day)
            if st.session_state.user_role == "AllViewer":
                allowed_files = os.listdir(folder_path)
            else:
                allowed_files = [f for f in os.listdir(folder_path) if is_file_for_user(f, st.session_state.username)]

            if allowed_files:
                chosen_file = st.selectbox("File Name", allowed_files)
                path = os.path.join(folder_path, chosen_file)
                df = read_excel_file(path).astype(str)
                st.dataframe(df)
                with open(path, "rb") as f:
                    st.download_button("⬇ Download Excel", f, file_name=chosen_file)
            else:
                st.warning("⚠ No files for your line.")

    if st.button("Logout"):
        logout()
        st.rerun()
