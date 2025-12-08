import streamlit as st
import warnings
import logging
import os
import pandas as pd
from datetime import datetime, date
import re
import base64
import altair as alt

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
        [data-testid="stAppViewContainer"] {{
            padding-top: 160px !important;
        }}
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

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
    "All": {"password": "9021", "role": "AllViewer"},
    "managers": {"password": "9021", "role": "AllViewer"}
}

# ----------------------------
# Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

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
# Login / Logout Logic
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
    st.session_state.current_page = "dashboard"
    st.rerun()

# ----------------------------
# Pie Chart Function
# ----------------------------
def plot_total_ach_pie(selected_day):
    if not selected_day:
        return
    folder_path = os.path.join(BASE_PATH, selected_day)
    files = os.listdir(folder_path)
    
    # For 'All' or 'managers', always take 'All' sheet
    if st.session_state.username.lower() in ["all", "managers"]:
        all_files = [f for f in files if "all" in f.lower()]
        if not all_files:
            st.warning("No 'All' file found.")
            return
        file_path = os.path.join(folder_path, all_files[0])
    else:
        # Otherwise take the file for the user
        user_files = [f for f in files if is_file_for_user(f, st.session_state.username)]
        if not user_files:
            st.warning("No file for your line.")
            return
        file_path = os.path.join(folder_path, user_files[0])
    
    df = pd.read_excel(file_path)
    if "Total Ach" not in df.columns:
        st.warning("'Total Ach' column not found in the file.")
        return
    
    total_ach_value = df["Total Ach"].iloc[-1]  # آخر قيمة كما طلبت
    chart_data = pd.DataFrame({
        "Category": ["Achieved", "Remaining"],
        "Value": [total_ach_value, max(0, 100 - total_ach_value)]
    })
    
    chart = alt.Chart(chart_data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color(field="Category", type="nominal", scale=alt.Scale(range=["#00c6ff", "#d3d3d3"])),
        tooltip=["Category", "Value"]
    ).properties(
        title="📊 Total Ach Pie Chart",
        width=300,
        height=300
    ).configure_view(
        fill=None  # خلفية شفافة
    )
    
    st.altair_chart(chart, use_container_width=False)

# ----------------------------
# UI
# ----------------------------
if not st.session_state.logged_in:
    set_bg_local("data/Untitled.png", True)
else:
    set_bg_local("data/Untitled.png", False)

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    u = st.text_input("", placeholder="Enter Username")
    p = st.text_input("", type="password", placeholder="Enter Password")
    if st.button("Login"):
        if login(u, p):
            st.rerun()
        else:
            st.error("❌ Wrong Username Or Password")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DASHBOARD ----------
else:
    st.subheader("👤 Daily Sales Dashboard")
    folders = get_current_month_folders()
    if folders:
        selected_day = folders[0]
        st.markdown(f"### 📅 Date: {selected_day}")
    else:
        st.warning("No available dates.")
        selected_day = None

    # ---------- Admin File Upload / View ----------
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
        st.markdown("---")
        if selected_day:
            folder_path = os.path.join(BASE_PATH, selected_day)
            for file in os.listdir(folder_path):
                path = os.path.join(folder_path, file)
                c1, c2, c3 = st.columns([4,1,1])
                with c1:
                    st.write(file)
                with c2:
                    if st.button("🗑", key="del_"+file):
                        os.remove(path)
                        st.warning(f"❌ File '{file}' deleted successfully")
                        st.rerun()
                with c3:
                    with open(path, "rb") as f:
                        st.download_button("⬇", f, file_name=file)
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
                    st.download_button(
                        "🔽 Download Excel File", f, file_name=chosen
                    )
            else:
                st.warning("No files for your line.")

    # ---------- Plot Pie Chart ----------
    plot_total_ach_pie(selected_day)
