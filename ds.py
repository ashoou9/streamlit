import streamlit as st
import warnings
import logging
import os
import pandas as pd
from datetime import datetime, date
import re
import base64

# ----------------------------
# Hide Warnings and Logs
# ----------------------------
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)
os.environ["PYTHONWARNINGS"] = "ignore"

# ----------------------------
# Page Background
# ----------------------------
def set_bg_local(image_file, login_page=True):
    with open(image_file, "rb") as f:
        img_bytes = f.read()
    b64 = base64.b64encode(img_bytes).decode()

    padding_top = "105px" if login_page else "210px"

    page_bg_img = f"""
    <style>
    html, body {{
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }}

    .stApp {{
        background: url("data:image/png;base64,{b64}") no-repeat center top fixed;
        background-size: cover;
    }}

    [data-testid="stAppViewContainer"] {{
        padding-top: {padding_top} !important;
        margin: 0 !important;
    }}

    .block-container {{
        padding-top: 2rem !important;
        padding-left: 30rem !important;
        padding-right: 30rem !important;
        padding-bottom: 100px !important;
        max-width: 100% !important;
    }}

    header, footer {{
        visibility: hidden !important;
        height: 0px;
    }}

    @media only screen and (max-width: 768px) {{
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# ----------------------------
# GLOBAL UI
# ----------------------------
st.markdown("""
<style>

.top-actions {
    position: fixed;
    top: 15px;
    right: 20px;
    display: flex;
    gap: 10px;
    z-index: 100000;
}

.top-actions .stButton > button {
    width: 140px;
    height: 40px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    color: white !important;
    border: none;
}

.about-btn .stButton > button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
}

.logout-btn .stButton > button {
    background: linear-gradient(90deg, #ff4b4b, #ff0000);
}

.stDownloadButton button {
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white !important;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Users
# ----------------------------
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
    "All": {"password": "9021", "role": "AllViewer"}
}

# ----------------------------
# Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

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
    return sorted([f for f in os.listdir(BASE_PATH) if f.startswith(today)], reverse=True)

def is_file_for_user(filename, username):
    name = filename.replace(".xlsx", "").replace(".xls", "").lower()
    parts = re.split(r"\s*-\s*", name)
    return any(username.lower() in p.strip() for p in parts)

# ----------------------------
# Login / Logout
# ----------------------------
def login(username, password):
    for key, data in users.items():
        if username.lower() == key.lower() and password == data["password"]:
            st.session_state.logged_in = True
            st.session_state.user_role = data["role"]
            st.session_state.username = key
            return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.page = "dashboard"

# ----------------------------
# Background
# ----------------------------
if not st.session_state.logged_in:
    set_bg_local("data/background.png", True)
else:
    set_bg_local("data/background.png", False)

# ----------------------------
# LOGIN
# ----------------------------
if not st.session_state.logged_in:
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(u, p):
            st.rerun()
        else:
            st.error("Wrong Username Or Password")

# ----------------------------
# DASHBOARD
# ----------------------------
else:

    # ===== TOP BUTTONS =====
    st.markdown('<div class="top-actions">', unsafe_allow_html=True)

    if st.button("ℹ About Us"):
        st.session_state.page = "about"
        st.rerun()

    if st.button("🔴 Logout"):
        logout()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ===== ABOUT PAGE =====
    if st.session_state.page == "about":
        st.subheader("About Us")
        st.write("Ahmed Mahmoud")
        st.write("Data Analyst")
        st.write("Python & Streamlit Developer")

        if st.button("⬅ Back"):
            st.session_state.page = "dashboard"
            st.rerun()

    # ===== MAIN DASHBOARD =====
    else:

        st.subheader("👤 Sales Dashboard")

        folders = get_current_month_folders()
        selected_day = folders[0] if folders else None

        if selected_day:
            st.markdown(f"### 📅 Date: {selected_day}")
        else:
            st.warning("No available dates.")

        # ========== ADMIN ==========
        if st.session_state.user_role == "Admin":

            st.subheader("🧑‍💼 Admin Dashboard")

            uploaded_files = st.file_uploader(
                "Upload Excel Files", type=["xlsx","xls"], accept_multiple_files=True
            )

            if uploaded_files:
                today_folder = os.path.join(BASE_PATH, datetime.today().strftime("%Y-%m-%d"))
                os.makedirs(today_folder, exist_ok=True)

                for file in uploaded_files:
                    with open(os.path.join(today_folder, file.name), "wb") as f:
                        f.write(file.getbuffer())

                st.success("✅ Files uploaded successfully")

            if selected_day:
                folder_path = os.path.join(BASE_PATH, selected_day)

                for file in os.listdir(folder_path):
                    path = os.path.join(folder_path, file)

                    c1, c2, c3 = st.columns([4,1,1])
                    with c1:
                        st.write(file)

                    with c2:
                        with open(path, "rb") as f:
                            st.download_button("⬇", f, file_name=file)

                    with c3:
                        if st.button("🗑", key=file):
                            os.remove(path)
                            st.rerun()

        # ========== USER ==========
        else:
            if selected_day:
                folder_path = os.path.join(BASE_PATH, selected_day)

                allowed_files = [
                    f for f in os.listdir(folder_path)
                    if st.session_state.user_role == "AllViewer"
                    or is_file_for_user(f, st.session_state.username)
                ]

                if allowed_files:
                    chosen = st.selectbox("File Name", allowed_files)
                    path = os.path.join(folder_path, chosen)

                    with open(path, "rb") as f:
                        st.download_button("🔽 Download Excel File", f, file_name=chosen)
                else:
                    st.warning("No files for your line.")
