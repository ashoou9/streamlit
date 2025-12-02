import streamlit as st
import warnings
import logging
import os
import pandas as pd
from datetime import datetime, date
import re
from PIL import Image, ImageDraw, ImageFont

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
    for part in parts:
        if username.lower() in part.strip():
            return True
    return False


def excel_to_image_pure(df, img_path):
    df = df.astype(str)

    cell_width = 180
    cell_height = 40
    padding = 10

    rows, cols = df.shape
    width = cols * cell_width + padding * 2
    height = (rows + 1) * cell_height + padding * 2

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    # Header
    for j, col in enumerate(df.columns):
        x = padding + j * cell_width
        y = padding
        draw.rectangle([x, y, x + cell_width, y + cell_height], outline="black")
        draw.text((x + 5, y + 10), col, fill="black", font=font)

    # Data
    for i in range(rows):
        for j in range(cols):
            x = padding + j * cell_width
            y = padding + (i + 1) * cell_height
            draw.rectangle([x, y, x + cell_width, y + cell_height], outline="black")
            draw.text((x + 5, y + 10), df.iloc[i, j], fill="black", font=font)

    img.save(img_path)

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
st.title("Daily Sales")

if not st.session_state.logged_in:
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(u, p):
            st.rerun()
        else:
            st.error("Wrong User Or Password")

# =======================
# ✅ AFTER LOGIN
# =======================
else:
    st.success("Welcome To Your Daily Sales 👋")

    # ================= ADMIN =================
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

        st.markdown("---")
        selected_day = st.selectbox("Sales Day", get_current_month_folders())

        if selected_day:
            folder_path = os.path.join(BASE_PATH, selected_day)
            files = os.listdir(folder_path)

            for file in files:
                path = os.path.join(folder_path, file)
                c1, c2, c3 = st.columns([4, 1, 1])
                with c1:
                    st.write(file)
                with c2:
                    if st.button("👁", key=file):
                        df = pd.read_excel(path).astype(str)
                        st.dataframe(df)
                with c3:
                    with open(path, "rb") as f:
                        st.download_button("⬇", f, file_name=file)

    # ================= USER =================
    elif st.session_state.user_role in ["User", "AllViewer"]:
        st.subheader("👤 Sales Dashboard")

        selected_day = st.selectbox("Date", get_current_month_folders())

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
                chosen_file = st.selectbox("File Name", allowed_files)
                path = os.path.join(folder_path, chosen_file)

                df = pd.read_excel(path).astype(str)

                # ✅ عرض الجدول
                st.dataframe(df)

                # ✅ إنشاء الصورة
                img_path = "temp_sheet.png"
                excel_to_image_pure(df, img_path)

                # ✅ عرض الصورة بسكرول
                st.markdown("""
                    <div style="height:450px; overflow-y:scroll; border:2px solid #ddd; padding:10px;">
                """, unsafe_allow_html=True)

                st.image(img_path, use_container_width=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # ✅ تحميل Excel
                with open(path, "rb") as f:
                    st.download_button(
                        "🔽 Download Excel File",
                        f,
                        file_name=chosen_file
                    )

                # ✅ تحميل الصورة PNG
                with open(img_path, "rb") as img_file:
                    st.download_button(
                        "📥 Download Image",
                        img_file,
                        file_name="sheet.png"
                    )

            else:
                st.warning("No files for your line.")

    # ---------------- Logout ----------------
    if st.button("Logout"):
        logout()
        st.rerun()
