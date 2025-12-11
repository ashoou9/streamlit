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
# Page Background
# ----------------------------
def set_bg_local(image_file, login_page=True):
    with open(image_file, "rb") as f:
        img_bytes = f.read()
    b64 = base64.b64encode(img_bytes).decode()

    padding_top = "105px" if login_page else "180px"

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
        padding-top: 1rem !important;
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
            padding-top: 140px !important;
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
# Custom CSS Styles
# ----------------------------
st.markdown("""
<style>
/* General styles */
.stApp {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Welcome Message */
.welcome-fixed {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    text-align: center !important;
    margin: 0 auto 25px auto !important;
    color: white !important;
    font-size: 1.3rem !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    backdrop-filter: blur(10px) !important;
    max-width: 600px !important;
}

/* Feedback Card - FIXED */
.feedback-card {
    background: rgba(255, 255, 255, 0.1) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    margin-bottom: 20px !important;
    border-left: 5px solid #00c6ff !important;
    backdrop-filter: blur(10px) !important;
}

.feedback-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.feedback-username {
    font-size: 1.1rem;
    font-weight: bold;
    color: white;
    margin: 0;
}

.feedback-date {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.7);
    margin: 0;
}

/* Comment Box - FIXED */
.comment-content {
    background: rgba(0, 0, 0, 0.25) !important;
    padding: 15px !important;
    border-radius: 10px !important;
    margin: 10px 0 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    line-height: 1.6 !important;
    font-size: 0.95rem !important;
    color: rgba(255, 255, 255, 0.95) !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white;
    border: none;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #0051cc, #0099cc);
    transform: scale(1.02) !important;
    box-shadow: 0 5px 15px rgba(0,114,255,0.4) !important;
}

.stButton > button[kind="secondary"] {
    background: linear-gradient(90deg, #FF9800, #FF5722) !important;
}

.stButton > button[kind="secondary"]:hover {
    background: linear-gradient(90deg, #F57C00, #E64A19) !important;
}

/* Delete button */
.delete-btn {
    background: linear-gradient(90deg, #ff4444, #cc0000) !important;
}

.delete-btn:hover {
    background: linear-gradient(90deg, #cc0000, #990000) !important;
}

/* Logout button fix */
.logout-btn {
    min-width: 100px !important;
    width: auto !important;
    padding: 0 15px !important;
}

/* Login box */
.login-box {
    background: rgba(255, 255, 255, 0.1) !important;
    width: 420px;
    max-width: 90%;
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    margin: 60px auto 0 auto;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2) !important;
}

/* Text colors */
h1, h2, h3, h4, h5, h6,
.stSubheader,
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stText"] {
    color: white !important;
    font-weight: bold !important;
}

label[data-baseweb="label"] {
    color: white !important;
    font-weight: bold !important;
}

/* Custom card */
.custom-card {
    background: rgba(255, 255, 255, 0.1) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    margin-bottom: 15px !important;
    border-left: 5px solid #00c6ff !important;
    backdrop-filter: blur(10px) !important;
}

/* Notification card */
.notification-card {
    background: rgba(255,255,255,0.15) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    margin-bottom: 15px !important;
    border-left: 5px solid #FF9800 !important;
    backdrop-filter: blur(10px) !important;
}

.notification-card.read {
    border-left: 5px solid #4CAF50 !important;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

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

if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

if "replying_to" not in st.session_state:
    st.session_state.replying_to = None

# ----------------------------
# Paths
# ----------------------------
BASE_PATH = "data"
FEEDBACK_FILE = os.path.join(BASE_PATH, "feedback.csv")

# ----------------------------
# Helper Functions
# ----------------------------
def clean_text(text):
    """
    Clean text from HTML tags and escape special characters
    """
    if not isinstance(text, str):
        return str(text)
    
    # إزالة جميع HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # تنظيف الأحرف الخاصة
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = text.strip()
    
    return text

def get_current_month_folders():
    """Get all folders for current month"""
    if not os.path.exists(BASE_PATH):
        return []
    today = date.today().strftime("%Y-%m")
    return sorted([f for f in os.listdir(BASE_PATH) if f.startswith(today)], reverse=True)

def is_file_for_user(filename, username):
    """Check if file belongs to specific user"""
    name = filename.replace(".xlsx", "").replace(".xls", "").lower()
    parts = re.split(r"\s*-\s*", name)
    return any(username.lower() in p.strip() for p in parts)

def add_feedback(username, comment, replied_to=None, replied_by=None):
    """Add feedback to CSV file with notification support"""
    os.makedirs(BASE_PATH, exist_ok=True)
    
    cleaned_comment = clean_text(comment) if comment else ""
    
    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_csv(FEEDBACK_FILE)
        for col in ["id", "replied_to", "replied_by", "is_read"]:
            if col not in df.columns:
                df[col] = None
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
    """Load feedback from CSV file"""
    if os.path.exists(FEEDBACK_FILE):
        try:
            df = pd.read_csv(FEEDBACK_FILE)
            if 'comment' in df.columns:
                df['comment'] = df['comment'].apply(lambda x: clean_text(x) if isinstance(x, str) else x)
            
            required_columns = ["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"]
            for col in required_columns:
                if col not in df.columns:
                    df[col] = None
            
            if df['id'].isna().any():
                df['id'] = df.apply(lambda x: str(uuid.uuid4())[:8] if pd.isna(x['id']) else x['id'], axis=1)
            
            if df['is_read'].isna().any():
                df['is_read'] = df['is_read'].fillna(False)
            
            return df
        except Exception as e:
            st.error(f"Error loading feedback: {e}")
            return pd.DataFrame(columns=["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"])
    else:
        return pd.DataFrame(columns=["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"])

def get_notifications(username):
    """Get notifications for specific user"""
    df = load_feedback()
    
    if df.empty:
        return pd.DataFrame()
    
    user_notifications = df[
        (df['replied_to'] == username) & 
        (df['is_read'] == False)
    ].copy()
    
    return user_notifications

def get_unread_count(username):
    """Get count of unread notifications"""
    notifications = get_notifications(username)
    return len(notifications)

def mark_as_read(feedback_id):
    """Mark notification as read"""
    df = load_feedback()
    
    if not df.empty and 'id' in df.columns:
        df.loc[df['id'] == feedback_id, 'is_read'] = True
        df.to_csv(FEEDBACK_FILE, index=False)
        return True
    return False

def mark_all_as_read(username):
    """Mark all notifications as read for a user"""
    df = load_feedback()
    
    if not df.empty:
        mask = (df['replied_to'] == username) & (df['is_read'] == False)
        df.loc[mask, 'is_read'] = True
        df.to_csv(FEEDBACK_FILE, index=False)
        return True
    return False

def delete_feedback(feedback_id):
    """Delete feedback by ID"""
    df = load_feedback()
    
    if not df.empty and 'id' in df.columns:
        initial_count = len(df)
        df = df[df['id'] != feedback_id]
        
        if len(df) < initial_count:
            df.to_csv(FEEDBACK_FILE, index=False)
            return True
    
    return False

def delete_all_feedback():
    """Delete all feedback"""
    if os.path.exists(FEEDBACK_FILE):
        os.remove(FEEDBACK_FILE)
        return True
    return False

# ----------------------------
# Login / Logout Logic
# ----------------------------
def login(username, password):
    """Authenticate user"""
    for key, data in users.items():
        if username.lower() == key.lower() and password == data["password"]:
            st.session_state.logged_in = True
            st.session_state.user_role = data["role"]
            st.session_state.username = key
            st.session_state.show_welcome = True
            return True
    return False

def logout():
    """Logout user and reset session"""
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.current_page = "dashboard"
    st.session_state.show_welcome = True
    st.session_state.replying_to = None

# ----------------------------
# Navigation Buttons (Top-Right)
# ----------------------------
def top_right_buttons():
    """Display navigation buttons at top-right"""
    unread_count = 0
    if st.session_state.logged_in and st.session_state.current_page != "notifications":
        unread_count = get_unread_count(st.session_state.username)
    
    # استخدام أعمدة متساوية
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📊 Dashboard", key="nav_dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("💬 Feedback", key="nav_feedback"):
            st.session_state.current_page = "feedback"
            st.rerun()
    
    with col3:
        button_label = "🔔 Notifications"
        if unread_count > 0:
            button_label = f"🔔 ({unread_count})"
        
        if st.button(button_label, key="nav_notifications"):
            st.session_state.current_page = "notifications"
            st.rerun()
    
    with col4:
        if st.button("ℹ️ About", key="nav_about"):
            st.session_state.current_page = "about"
            st.rerun()
    
    with col5:
        # جعل زر Logout نوع secondary ليكون بلون مختلف وأكبر
        if st.button("🚪 Logout", key="nav_logout", type="secondary"):
            logout()
            st.rerun()

# ----------------------------
# Welcome Message Component
# ----------------------------
def show_welcome_message():
    """Display welcome message that stays in dashboard"""
    if st.session_state.show_welcome and st.session_state.logged_in:
        username = st.session_state.username
        
        unread_count = get_unread_count(username)
        notification_badge = ""
        if unread_count > 0 and st.session_state.current_page != "notifications":
            notification_badge = f'<span style="background: #FF5252; color: white; padding: 2px 8px; border-radius: 10px; margin-left: 10px; font-size: 0.9rem;">{unread_count} new</span>'
        
        st.markdown(f"""
        <div class="welcome-fixed">
            <h3>👋 Hello {username.capitalize()} Team! {notification_badge}</h3>
            <p>Welcome to the Sales Dashboard</p>
            <div style="margin-top: 10px; font-size: 1.2rem;">
                📅 {date.today().strftime('%B %d, %Y')}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Display Feedback Function - FIXED
# ----------------------------
def display_feedback_card(row, is_admin=False):
    """Display a single feedback card - SIMPLIFIED VERSION"""
    with st.container():
        # استخدام Streamlit components مباشرة
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**👤 {row['username']}**")
        with col2:
            st.caption(f"📅 {row['datetime']}")
        
        # عرض التعليق في مربع نص
        st.markdown(
            f'<div class="comment-content">{row["comment"]}</div>',
            unsafe_allow_html=True
        )
        
        # إذا كان هناك رد
        if pd.notna(row.get('replied_by')) and str(row.get('replied_by')).strip() != '':
            st.info(f"↩️ Replied by: {row['replied_by']}")
        
        # أزرار الإجراءات للمسؤول
        if is_admin:
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🗑️ Delete", key=f"delete_{row['id']}", type="secondary"):
                    if delete_feedback(row['id']):
                        st.success("✅ Feedback deleted!")
                        time.sleep(1)
                        st.rerun()
            
            with col_btn2:
                if st.button("📤 Reply", key=f"reply_{row['id']}", type="primary"):
                    st.session_state.replying_to = row['id']
                    st.rerun()
            
            # نموذج الرد إذا كان مفعلاً
            if st.session_state.replying_to == row['id']:
                with st.form(key=f"reply_form_{row['id']}"):
                    reply_text = st.text_area(
                        "Your reply:",
                        placeholder=f"Type your reply to {row['username']}...",
                        height=100,
                        key=f"reply_text_{row['id']}"
                    )
                    
                    col_sub1, col_sub2 = st.columns(2)
                    with col_sub1:
                        submit_reply = st.form_submit_button("Send Reply", type="primary")
                    with col_sub2:
                        cancel_reply = st.form_submit_button("Cancel")
                    
                    if cancel_reply:
                        st.session_state.replying_to = None
                        st.rerun()
                    
                    if submit_reply and reply_text.strip():
                        add_feedback(
                            username=st.session_state.username,
                            comment=reply_text,
                            replied_to=row['username'],
                            replied_by=st.session_state.username
                        )
                        st.session_state.replying_to = None
                        
                        st.success(f"✅ Reply sent to {row['username']}!")
                        time.sleep(1)
                        st.rerun()
                    elif submit_reply:
                        st.warning("Please write a reply first.")

# ----------------------------
# Main Application UI
# ----------------------------
if not st.session_state.logged_in:
    set_bg_local("data/Untitled.png", True)
else:
    set_bg_local("data/Untitled.png", False)

# ---------- LOGIN PAGE ----------
if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: white; margin-bottom: 5px;">🔐 Login</h2>
        <p style="color: rgba(255,255,255,0.8);">Enter your credentials</p>
    </div>
    """, unsafe_allow_html=True)
    
    u = st.text_input("", placeholder="👤 Username", key="login_username")
    p = st.text_input("", type="password", placeholder="🔒 Password", key="login_password")
    
    if st.button("🚀 Login to Dashboard", key="login_button", type="primary"):
        if u and p:
            if login(u, p):
                st.success(f"✅ Login successful! Welcome {u} Team! 👋")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Wrong Username Or Password")
        else:
            st.warning("⚠️ Please enter both username and password")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DASHBOARD (Logged In) ----------
else:
    # Show navigation buttons
    top_right_buttons()
    
    # Show welcome message
    show_welcome_message()
    
    # ----- DASHBOARD PAGE -----
    if st.session_state.current_page == "dashboard":
        st.subheader("📊 Daily Sales Dashboard")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #00c6ff; margin: 0;">📅 Today</h4>
                <p style="font-size: 1.5rem; margin: 5px 0;">{date}</p>
            </div>
            """.format(date=date.today().strftime('%d %b')), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="custom-card">
                <h4 style="color: #00c6ff; margin: 0;">👤 Role</h4>
                <p style="font-size: 1.5rem; margin: 5px 0;">{role}</p>
            </div>
            """.format(role=st.session_state.user_role), unsafe_allow_html=True)
        
        with col3:
            unread_count = get_unread_count(st.session_state.username)
            notification_text = f"{unread_count} unread" if unread_count > 0 else "All read"
            badge_color = "#FF5252" if unread_count > 0 else "#4CAF50"
            
            st.markdown(f"""
            <div class="custom-card">
                <h4 style="color: #00c6ff; margin: 0;">🔔 Notifications</h4>
                <p style="font-size: 1.5rem; margin: 5px 0;">
                    <span style="color: {badge_color};">{notification_text}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        folders = get_current_month_folders()
        
        if folders:
            selected_day = st.selectbox(
                "📅 Select Date:",
                folders,
                format_func=lambda x: f"📅 {x}",
                index=0,
                key="date_selector"
            )
            
            if selected_day:
                folder_path = os.path.join(BASE_PATH, selected_day)
                
                if st.session_state.user_role == "Admin":
                    st.markdown("---")
                    st.subheader("👨‍💼 Admin Controls")
                    
                    with st.expander("📤 Upload Files", expanded=True):
                        uploaded_files = st.file_uploader(
                            "Choose Excel files", 
                            type=["xlsx","xls"], 
                            accept_multiple_files=True,
                            key="admin_uploader"
                        )
                        
                        if uploaded_files and st.button("🚀 Upload Files", type="primary", key="upload_button"):
                            today_folder = os.path.join(BASE_PATH, selected_day)
                            os.makedirs(today_folder, exist_ok=True)
                            
                            success_count = 0
                            for file in uploaded_files:
                                with open(os.path.join(today_folder, file.name), "wb") as f:
                                    f.write(file.getbuffer())
                                success_count += 1
                            
                            st.success(f"✅ {success_count} file(s) uploaded successfully!")
                            time.sleep(1)
                            st.rerun()
                    
                    st.markdown("---")
                    st.subheader("📁 File Management")
                    
                    if os.path.exists(folder_path):
                        files = os.listdir(folder_path)
                        if files:
                            for file in files:
                                path = os.path.join(folder_path, file)
                                with st.container():
                                    c1, c2, c3 = st.columns([6, 1, 2])
                                    
                                    with c1:
                                        st.write(f"📄 **{file}**")
                                    
                                    with c2:
                                        if st.button("🗑️", key=f"del_{file}"):
                                            os.remove(path)
                                            st.warning(f"Deleted: {file}")
                                            time.sleep(1)
                                            st.rerun()
                                    
                                    with c3:
                                        with open(path, "rb") as f:
                                            st.download_button(
                                                "📥 Download",
                                                f,
                                                file_name=file,
                                                key=f"dl_{file}"
                                            )
                        else:
                            st.info("📭 No files available for this date.")
                    else:
                        st.info("📁 Folder doesn't exist yet.")
                
                else:
                    st.markdown("---")
                    
                    if os.path.exists(folder_path):
                        allowed_files = [
                            f for f in os.listdir(folder_path)
                            if st.session_state.user_role == "AllViewer"
                            or is_file_for_user(f, st.session_state.username)
                        ]
                        
                        if allowed_files:
                            st.subheader("📥 Your Files")
                            
                            cols = st.columns(2)
                            for idx, file in enumerate(allowed_files):
                                with cols[idx % 2]:
                                    with st.container():
                                        st.markdown(f"""
                                        <div style="
                                            background: rgba(255,255,255,0.1);
                                            padding: 15px;
                                            border-radius: 10px;
                                            margin-bottom: 10px;
                                        ">
                                            <p style="margin: 0;"><strong>📄 {file}</strong></p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        path = os.path.join(folder_path, file)
                                        with open(path, "rb") as f:
                                            file_bytes = f.read()
                                        
                                        st.download_button(
                                            "Download",
                                            data=file_bytes,
                                            file_name=file,
                                            key=f"user_file_{idx}",
                                            use_container_width=True
                                        )
                        else:
                            st.warning("📭 No files available for your team yet.")
                    else:
                        st.warning("📁 No data available for this date.")
        else:
            st.info("📅 No data available for current month.")
    
    # ----- FEEDBACK PAGE - FIXED VERSION -----
    elif st.session_state.current_page == "feedback":
        st.subheader("💬 Feedback System")
        
        if st.session_state.user_role == "Admin":
            df = load_feedback()
            if not df.empty:
                st.markdown(f"### 📋 Total Feedback: {len(df)}")
                
                # زر حذف الكل
                if st.button("🗑️ Delete All Feedback", type="secondary", key="delete_all_btn"):
                    if delete_all_feedback():
                        st.success("✅ All feedback deleted!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete feedback")
                
                st.markdown("---")
                
                # عرض الفيدباك باستخدام الدالة المصححة
                for idx, row in df.sort_values("datetime", ascending=False).iterrows():
                    display_feedback_card(row, is_admin=True)
                    st.markdown("---")
            else:
                st.info("📭 No feedback yet.")
        else:
            # نموذج إرسال الفيدباك للمستخدمين العاديين
            with st.form("feedback_form", clear_on_submit=True):
                st.markdown("### 📝 Share Your Thoughts")
                
                comment = st.text_area(
                    "Your feedback:",
                    placeholder="What's on your mind? Suggestions, issues, or comments...",
                    height=150,
                    key="user_feedback"
                )
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    submit = st.form_submit_button("📤 Submit", type="primary")
                
                if submit and comment.strip():
                    add_feedback(st.session_state.username, comment.strip())
                    st.success("✅ Thank you for your feedback! 🌟")
                    time.sleep(1.5)
                    st.rerun()
                elif submit:
                    st.warning("⚠️ Please write something before submitting.")
    
    # ----- NOTIFICATIONS PAGE -----
    elif st.session_state.current_page == "notifications":
        st.subheader("🔔 Your Notifications")
        
        notifications = get_notifications(st.session_state.username)
        
        if not notifications.empty:
            if st.button("✅ Mark All as Read", type="primary", key="mark_all_read"):
                if mark_all_as_read(st.session_state.username):
                    st.success("All notifications marked as read!")
                    time.sleep(0.5)
                    st.rerun()
            
            st.markdown(f"### 📩 You have {len(notifications)} notification(s)")
            
            for idx, row in notifications.sort_values("datetime", ascending=False).iterrows():
                with st.container():
                    is_new = not row.get('is_read', False)
                    replied_by = row.get('replied_by', '')
                    
                    st.markdown(f"""
                    <div class="notification-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <p style="margin: 0; font-size: 1.1rem; color: white;">
                                    <strong>👤 {replied_by if replied_by else row['username']}</strong>
                                    {' replied to your feedback' if replied_by else ' posted new feedback'}
                                </p>
                                <p style="margin: 5px 0 10px 0; font-size: 0.9rem; color: rgba(255,255,255,0.8);">
                                    📅 {row['datetime']}
                                    {' | 🔔 NEW' if is_new else ' | ✅ Read'}
                                </p>
                            </div>
                        </div>
                        
                        <div class="comment-content">
                            {row['comment']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if is_new:
                        if st.button("✓ Mark as Read", key=f"read_{row.get('id', idx)}"):
                            if mark_as_read(row.get('id', idx)):
                                st.success("Notification marked as read!")
                                time.sleep(0.5)
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("📭 No new notifications.")
            
            df = load_feedback()
            user_notifications = df[
                (df['replied_to'] == st.session_state.username) | 
                (df['username'] == st.session_state.username)
            ]
            
            if not user_notifications.empty:
                st.markdown("---")
                st.subheader("📜 Notification History")
                
                for idx, row in user_notifications.sort_values("datetime", ascending=False).iterrows():
                    with st.container():
                        is_reply = pd.notna(row.get('replied_by')) and str(row.get('replied_by')).strip() != ''
                        
                        st.markdown(f"""
                        <div class="notification-card read">
                            <div>
                                <p style="margin: 0; color: white;">
                                    <strong>👤 {row['username']}</strong>
                                    {f"<span style='color: #FF9800; font-size: 0.9rem; margin-left: 10px;'>↩️ {row['replied_by']}</span>" if is_reply else ""}
                                </p>
                                <p style="margin: 5px 0; font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                                    📅 {row['datetime']}
                                </p>
                            </div>
                            <div class="comment-content">
                                {row['comment']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("---")
        
        st.markdown("---")
        if st.button("← Back to Dashboard", key="back_to_dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    # ----- ABOUT PAGE -----
    elif st.session_state.current_page == "about":
        st.subheader("ℹ️ About This Dashboard")
        
        with st.container():
            st.markdown("""
            <div class="custom-card">
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🎯 Mission")
            st.markdown("Streamline daily sales operations and provide real-time insights for all teams.")
            
            st.markdown("---")
            
            st.markdown("#### ✨ Features")
            st.markdown("""
            ✅ **File Management** - Upload and download sales files  
            ✅ **Feedback System** - Share thoughts and suggestions  
            ✅ **Notifications** - Get alerts for replies  
            ✅ **Admin Controls** - Manage feedback and files  
            ✅ **Team-Based Access** - Different views for different teams  
            """)
            
            st.markdown("---")
            
            st.markdown("#### 👥 Teams")
            st.markdown("""
            • **Admin** - Full system control  
            • **CHC** - Healthcare Division  
            • **CNS** - Neuroscience Division  
            • **GIT** - Gastroenterology  
            • **Primary Care** - General Medicine  
            • **CVM** - Cardiology Division  
            • **Power Team** - Special Operations  
            • **All Teams** - Comprehensive access
            """)
            
            st.markdown("---")
            
            st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Footer
# ----------------------------
if st.session_state.logged_in:
    st.markdown("---")
    if st.session_state.logged_in and st.session_state.current_page != "notifications":
        unread_count = get_unread_count(st.session_state.username)
        notification_text = f" | 🔔 {unread_count} unread notification(s)" if unread_count > 0 else ""
    else:
        notification_text = ""
    
    st.markdown(f"""
    <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem; padding: 15px;">
        <p>📊 Sales Dashboard | © 2024 | 🔒 Secure Access {notification_text}</p>
    </div>
    """, unsafe_allow_html=True)