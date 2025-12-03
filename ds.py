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
def set_bg_local(image_file):
    with open(image_file, "rb") as f:
        img_bytes = f.read()
    b64 = base64.b64encode(img_bytes).decode()

    page_bg_img = f"""
    <style>
    html, body {{
        width: auto;
        height: auto;
        margin: auto;
        padding: auto;
        overflow: hidden;
    }}

    .stApp {{
        background: url("data:image/png;base64,{b64}") no-repeat center center fixed;
        background-size: cover;
    }}

    [data-testid="stAppViewContainer"] {{
        padding: 0 !important;
        margin: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
    }}

    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 30rem !important;
        padding-right: 30rem !important;
        max-width: 100% !important;
    }}

    header, footer {{
        visibility: hidden;
        height: 0px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_bg_local("data/background.png")

# ----------------------------
# Login UI Style
# ----------------------------
st.markdown("""
<style>
.login-box {
    background: rgba(0, 0, 0, 0.0);
    width: 420px;
    padding: 35px;
    border-radius: 18px;
    box-shadow: 0 0 0px rgba(0,0,0,0.4);
    text-align: center;
    margin: auto;
    margin-top: 120px; 
}


.stTextInput > div > div > input {
    text-align: left;
    font-size: 16px;
    padding: 10px;
    border-radius: 8px;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #0051cc, #0099cc);
    transform: scale(1.02);
    transition: 0.2s;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Users Database
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
    "All":   {"password": "9021", "role": "AllViewer"}
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
    folders = [f for f in os.listdir(BASE_PATH) if f.startswith(today)]
    return sorted(folders, reverse=True)

def is_file_for_user(filename, username):
    name = filename.replace(".xlsx", "").replace(".xls", "").lower()
    parts = re.split(r"\s*-\s*", name)
    return any(username.lower() in part.strip() for part in parts)

# ----------------------------
# Login / Logout
# ----------------------------
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

# ----------------------------
# UI
# ----------------------------


if not st.session_state.logged_in:

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
   # st.markdown('<div class="login-title">🔐 Daily Sales Login</div>', unsafe_allow_html=True)

    u = st.text_input("Username", placeholder="Enter Username")
    p = st.text_input("Password", type="password", placeholder="Enter Password")

    if st.button("Login"):
        if login(u, p):
            st.rerun()
        else:
            st.error("❌ Wrong Username Or Password")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.success(f"Welcome {st.session_state.username} 👋")

    # ================= ADMIN =================
    if st.session_state.user_role == "Admin":
        st.subheader("🧑‍💼 Admin Dashboard")
        uploaded_files = st.file_uploader(
            "Upload Excel Files", type=["xlsx","xls"], accept_multiple_files=True
        )
        if uploaded_files:
            today_folder = os.path.join(BASE_PATH, datetime.today().strftime("%Y-%m-%d"))
            os.makedirs(today_folder, exist_ok=True)
            for file in uploaded_files:
                file_path = os.path.join(today_folder, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
            st.success("✅ Files uploaded successfully")

        st.markdown("---")
        selected_day = st.selectbox("Sales Day", get_current_month_folders())
        if selected_day:
            folder_path = os.path.join(BASE_PATH, selected_day)
            files = os.listdir(folder_path)
            for file in files:
                path = os.path.join(folder_path, file)
                c1,c2,c3 = st.columns([4,1,1])
                with c1: st.write(file)
                with c2:
                    if st.button("👁", key=file):
                        df = pd.read_excel(path).astype(str)
                        st.dataframe(df)
                with c3:
                    with open(path,"rb") as f:
                        st.download_button("⬇", f, file_name=file)

    # ================= USER / ALLVIEWER =================
    elif st.session_state.user_role in ["User","AllViewer"]:
        st.subheader("👤 Sales Dashboard")
        selected_day = st.selectbox("Date", get_current_month_folders())
        if selected_day:
            folder_path = os.path.join(BASE_PATH, selected_day)
            files = os.listdir(folder_path)
            allowed_files = []
            for file in files:
                if st.session_state.user_role=="AllViewer" or is_file_for_user(file, st.session_state.username):
                    allowed_files.append(file)

            if allowed_files:
                chosen_file = st.selectbox("File Name", allowed_files)
                path = os.path.join(folder_path, chosen_file)
                df = pd.read_excel(path).astype(str)
                st.dataframe(df)

                with open(path,"rb") as f:
                    st.download_button("🔽 Download Excel File", f, file_name=chosen_file)
            else:
                st.warning("No files for your line.")

    # -------- Logout ----------
    if st.button("Logout"):
        logout()
        st.rerun()
