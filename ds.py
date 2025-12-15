import streamlit as st
import warnings
import logging
import os
import pandas as pd
from datetime import datetime, date
import re
import base64
import time
import random
import uuid

# ----------------------------
# Hide Warnings and Logs
# ----------------------------
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)
os.environ["PYTHONWARNINGS"] = "ignore"

# ----------------------------
# Create Required Folders & Files
# ----------------------------
BASE_PATH = "data"
FEEDBACK_FILE = os.path.join(BASE_PATH, "feedback.csv")

# إنشاء المجلدات الضرورية
os.makedirs(BASE_PATH, exist_ok=True)
current_month = date.today().strftime("%Y-%m")
current_month_folder = os.path.join(BASE_PATH, current_month)
os.makedirs(current_month_folder, exist_ok=True)

if not os.path.exists(FEEDBACK_FILE):
    pd.DataFrame(columns=["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"]).to_csv(FEEDBACK_FILE, index=False)

# ----------------------------
# Simple Background - بدون صور معقدة
# ----------------------------
def set_simple_background():
    st.markdown("""
    <style>
    /* خلفية بسيطة */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
    }
    
    /* تحسين الهيدر */
    .st-emotion-cache-1avcm0n {
        background: rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(10px);
    }
    
    /* تحسين الكونتينر الرئيسي */
    .main .block-container {
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 1200px;
    }
    
    /* تحسين البطاقات */
    .card {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* تحسين الأزرار */
    .stButton > button {
        background: linear-gradient(90deg, #0072ff, #00c6ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #0051cc, #0099cc) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0, 114, 255, 0.4) !important;
    }
    
    /* تحسين حقول الإدخال */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* تحسين النصوص */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: white !important;
    }
    
    /* تحسين السايدبار */
    .st-emotion-cache-6qob1r {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px);
    }
    
    /* تحسين الـ selectbox */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    
    /* تحسين الـ textarea */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* تحسين التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        padding: 5px !important;
    }
    
    /* تحسين التنبيهات */
    .stAlert {
        border-radius: 10px !important;
    }
    
    /* تحسين الجداول */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    /* تحسين الـ expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
    
    /* تحسين الـ file uploader */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# تطبيق الخلفية
set_simple_background()

# ----------------------------
# Users Database
# ----------------------------
users = {
    "admin": {"password": "1001", "role": "Admin"},
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
    "managers": {"password": "9021", "role": "AllViewer"},
    "khalid": {"password": "9090", "role": "AllViewer"}
}

# ----------------------------
# Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.current_page = "dashboard"

# ----------------------------
# Helper Functions
# ----------------------------
def clean_text(text):
    if not isinstance(text, str):
        return str(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text.strip()

def get_current_month_folders():
    if not os.path.exists(BASE_PATH):
        return []
    today = date.today().strftime("%Y-%m")
    return sorted([f for f in os.listdir(BASE_PATH) if f.startswith(today)], reverse=True)

def add_feedback(username, comment, replied_to=None, replied_by=None):
    os.makedirs(BASE_PATH, exist_ok=True)
    cleaned_comment = clean_text(comment) if comment else ""
    
    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_csv(FEEDBACK_FILE)
    else:
        df = pd.DataFrame(columns=["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"])
    
    feedback_id = str(uuid.uuid4())[:8]
    
    new_feedback = {
        "id": feedback_id,
        "username": username,
        "comment": cleaned_comment,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "replied_to": replied_to,
        "replied_by": replied_by,
        "is_read": False
    }
    
    df = pd.concat([df, pd.DataFrame([new_feedback])], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)
    
    return feedback_id

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        try:
            return pd.read_csv(FEEDBACK_FILE)
        except:
            return pd.DataFrame(columns=["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"])
    return pd.DataFrame(columns=["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"])

def get_notifications(username):
    df = load_feedback()
    if df.empty:
        return pd.DataFrame()
    user_notifications = df[(df['replied_to'] == username) & (df['is_read'] == False)].copy()
    return user_notifications

def get_unread_count(username):
    return len(get_notifications(username))

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
    st.session_state.current_page = "dashboard"

# ----------------------------
# Main Application
# ----------------------------
if not st.session_state.logged_in:
    # Login Page
    st.title("🔐 Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            username = st.text_input("👤 Username", key="login_user")
            password = st.text_input("🔒 Password", type="password", key="login_pass")
            
            if st.button("🚀 Login", type="primary", use_container_width=True):
                if username and password:
                    if login(username, password):
                        st.success(f"Welcome {username}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")
            
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # Navigation Bar
    st.markdown("""
    <div style="background: rgba(0, 0, 0, 0.5); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    cols = st.columns(5)
    pages = ["📊 Dashboard", "💬 Feedback", "🔔 Notifications", "ℹ️ About", "🚪 Logout"]
    
    for idx, col in enumerate(cols):
        with col:
            if st.button(pages[idx], use_container_width=True):
                if idx == 4:  # Logout
                    logout()
                    st.rerun()
                else:
                    st.session_state.current_page = pages[idx].split()[1].lower()
                    st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Welcome Message
    unread_count = get_unread_count(st.session_state.username)
    badge = f" 🔔 ({unread_count})" if unread_count > 0 else ""
    
    st.markdown(f"""
    <div class="card">
        <h2>👋 Hello {st.session_state.username} Team!{badge}</h2>
        <p>📅 {date.today().strftime('%B %d, %Y')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Page Content
    if st.session_state.current_page == "dashboard":
        st.subheader("📊 Daily Sales Dashboard")
        
        # Get current month folders
        folders = get_current_month_folders()
        
        if folders:
            selected_day = st.selectbox("📅 Select Date:", folders)
            folder_path = os.path.join(BASE_PATH, selected_day)
            
            # Admin Controls - ظاهرة بوضوح
            if st.session_state.user_role == "Admin":
                st.markdown("---")
                st.subheader("👨‍💼 Admin Controls")
                
                with st.expander("📤 Upload Files", expanded=True):
                    uploaded_files = st.file_uploader(
                        "Choose Excel files", 
                        type=["xlsx", "xls"], 
                        accept_multiple_files=True,
                        key="admin_uploader"
                    )
                    
                    if uploaded_files:
                        if st.button("🚀 Upload Files", type="primary"):
                            for file in uploaded_files:
                                file_path = os.path.join(folder_path, file.name)
                                with open(file_path, "wb") as f:
                                    f.write(file.getbuffer())
                            st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
                            time.sleep(1)
                            st.rerun()
                
                st.markdown("---")
                st.subheader("📁 File Management")
                
                if os.path.exists(folder_path):
                    files = os.listdir(folder_path)
                    if files:
                        for file in files:
                            col1, col2, col3 = st.columns([3, 1, 1])
                            with col1:
                                st.write(f"📄 {file}")
                            with col2:
                                if st.button("🗑️", key=f"del_{file}"):
                                    os.remove(os.path.join(folder_path, file))
                                    st.rerun()
                            with col3:
                                with open(os.path.join(folder_path, file), "rb") as f:
                                    st.download_button("📥", f, file_name=file, key=f"dl_{file}")
                    else:
                        st.info("📭 No files available.")
            
            # User Files
            st.markdown("---")
            st.subheader("📂 Available Files")
            
            if os.path.exists(folder_path):
                if st.session_state.user_role == "Admin":
                    files = os.listdir(folder_path)
                else:
                    files = [f for f in os.listdir(folder_path)]
                
                if files:
                    for file in files:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"📄 {file}")
                        with col2:
                            with open(os.path.join(folder_path, file), "rb") as f:
                                st.download_button("Download", f, file_name=file, key=f"user_dl_{file}")
                else:
                    st.info("📭 No files available.")
        else:
            st.info("📅 No data available for current month.")
    
    elif st.session_state.current_page == "feedback":
        st.subheader("💬 Feedback System")
        
        if st.session_state.user_role == "Admin":
            df = load_feedback()
            if not df.empty:
                st.write(f"Total feedback: {len(df)}")
                
                if st.button("🗑️ Delete All Feedback", type="secondary"):
                    if os.path.exists(FEEDBACK_FILE):
                        os.remove(FEEDBACK_FILE)
                        st.success("All feedback deleted!")
                        st.rerun()
                
                for _, row in df.sort_values("datetime", ascending=False).iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class="card">
                            <strong>👤 {row['username']}</strong><br>
                            <small>📅 {row['datetime']}</small><br><br>
                            {row['comment']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"🗑️ Delete", key=f"del_{row['id']}"):
                            df = df[df['id'] != row['id']]
                            df.to_csv(FEEDBACK_FILE, index=False)
                            st.rerun()
            else:
                st.info("📭 No feedback yet.")
        else:
            with st.form("feedback_form"):
                comment = st.text_area("Your feedback:", height=150)
                if st.form_submit_button("📤 Submit", type="primary"):
                    if comment.strip():
                        add_feedback(st.session_state.username, comment.strip())
                        st.success("✅ Thank you for your feedback!")
                        time.sleep(1)
                        st.rerun()
    
    elif st.session_state.current_page == "notifications":
        st.subheader("🔔 Notifications")
        
        notifications = get_notifications(st.session_state.username)
        if not notifications.empty:
            st.write(f"You have {len(notifications)} unread notification(s)")
            for _, row in notifications.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <strong>👤 {row['username']}</strong><br>
                        <small>📅 {row['datetime']}</small><br><br>
                        {row['comment']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("📭 No new notifications.")
    
    elif st.session_state.current_page == "about":
        st.subheader("ℹ️ About")
        st.markdown("""
        <div class="card">
            <h3>Sales Dashboard System</h3>
            <p>This system helps teams manage daily sales data efficiently.</p>
            
            <h4>Features:</h4>
            <ul>
                <li>📊 Dashboard for sales data</li>
                <li>💬 Feedback system</li>
                <li>🔔 Notifications</li>
                <li>👨‍💼 Admin controls</li>
            </ul>
            
            <h4>Teams:</h4>
            <p>Admin, CHC, CNS, GIT, Primary Care, CVM, Power Team, DGU, DNU, Sildava, Ortho</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
if st.session_state.logged_in:
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>📊 Sales Dashboard | © 2024 | 🔒 Secure Access</p>", unsafe_allow_html=True)