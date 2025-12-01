import streamlit as st
import warnings
import logging
import os
import pandas as pd
from datetime import datetime, date

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
# Paths
# ----------------------------
BASE_PATH = "data"

# ----------------------------
# Helper: Get Current Month Folders
# ----------------------------
def get_current_month_folders(base_path):
    if not os.path.exists(base_path):
        return []

    today = date.today()
    current_year_month = today.strftime("%Y-%m")

    folders = []
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path) and folder.startswith(current_year_month):
            try:
                folder_date = datetime.strptime(folder, "%Y-%m-%d").date()
                folders.append(folder_date)
            except:
                pass

    folders.sort(reverse=True)
    return folders

# ----------------------------
# Login / Logout
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

    # ==================================================
    # ✅ ADMIN DASHBOARD
    # ==================================================
    if st.session_state.user_role == "Admin":
        st.subheader("🧑‍💼 Admin Dashboard")

        # ---------- Upload ----------
        uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

        if uploaded_file is not None:
            today_folder = os.path.join(BASE_PATH, datetime.today().strftime("%Y-%m-%d"))
            os.makedirs(today_folder, exist_ok=True)

            file_path = os.path.join(today_folder, uploaded_file.name)

            # حفظ الملف بنفس التمبلت الأصلي
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success("✅ File uploaded successfully with full formatting!")

        # ---------- Filter by Current Month Days ----------
        st.markdown("---")
        st.subheader("📅 Filter by Day (Current Month)")

        available_days = get_current_month_folders(BASE_PATH)

        if available_days:
            selected_day = st.selectbox(
                "Choose a day",
                available_days,
                format_func=lambda x: x.strftime("%Y-%m-%d")
            )

            selected_folder = os.path.join(BASE_PATH, selected_day.strftime("%Y-%m-%d"))

            # ---------- Files History ----------
            st.markdown("---")
            st.subheader("📂 Uploaded Files History")

            files = os.listdir(selected_folder)

            if files:
                for file in files:
                    file_path = os.path.join(selected_folder, file)

                    col1, col2, col3 = st.columns([4, 1, 1])

                    with col1:
                        st.write(file)

                    # 👁 View
                    with col2:
                        if st.button("👁", key=f"view_{file_path}"):
                            df = pd.read_excel(file_path)
                            st.dataframe(df)

                    # ⬇ Download
                    with col3:
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="⬇",
                                data=f,
                                file_name=file,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"down_{file_path}"
                            )

                    # 🗑 Delete with Confirmation
                    confirm_key = f"confirm_{file_path}"
                    if st.button("🗑 Delete", key=f"del_{file_path}"):
                        st.session_state[confirm_key] = True

                    if st.session_state.get(confirm_key):
                        st.warning(f"Are you sure you want to delete {file}?")

                        col_yes, col_no = st.columns(2)

                        with col_yes:
                            if st.button("✅ Yes", key=f"yes_{file_path}"):
                                os.remove(file_path)
                                st.success("Deleted successfully")
                                st.session_state[confirm_key] = False
                                st.rerun()

                        with col_no:
                            if st.button("❌ No", key=f"no_{file_path}"):
                                st.session_state[confirm_key] = False

            else:
                st.warning("No files for this day.")

        else:
            st.info("No uploads for current month yet.")

    # ==================================================
    # ✅ USER DASHBOARD
    # ==================================================
    elif st.session_state.user_role == "User":
        st.subheader("👤 User Dashboard")

        available_days = get_current_month_folders(BASE_PATH)

        if available_days:
            selected_day = st.selectbox(
                "Choose a day",
                available_days,
                format_func=lambda x: x.strftime("%Y-%m-%d")
            )

            selected_folder = os.path.join(BASE_PATH, selected_day.strftime("%Y-%m-%d"))
            files = os.listdir(selected_folder)

            if files:
                selected_file = st.selectbox("Choose File", files)
                file_path = os.path.join(selected_folder, selected_file)

                df = pd.read_excel(file_path)
                st.dataframe(df)

                # ⬇ Download ORIGINAL Excel with Formatting
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="⬇ Download File",
                        data=f,
                        file_name=selected_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.warning("No files for this day.")
        else:
            st.warning("No uploads for current month yet.")

    # ----------------------------
    # Logout
    # ----------------------------
    if st.button("Logout"):
        logout()
        st.rerun()
