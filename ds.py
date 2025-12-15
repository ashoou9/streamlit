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
# إنشاء المجلدات والملفات المطلوبة
# ----------------------------
BASE_PATH = "data"
FEEDBACK_FILE = os.path.join(BASE_PATH, "feedback.csv")

# تأكد من وجود المجلدات الضرورية
os.makedirs(BASE_PATH, exist_ok=True)
current_month = date.today().strftime("%Y-%m")
current_month_folder = os.path.join(BASE_PATH, current_month)
os.makedirs(current_month_folder, exist_ok=True)

# إنشاء ملف feedback إذا لم يكن موجودًا
if not os.path.exists(FEEDBACK_FILE):
    pd.DataFrame(columns=["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"]).to_csv(FEEDBACK_FILE, index=False)

# ----------------------------
# Page Background - معدل
# ----------------------------
def set_bg_local(image_file, login_page=True):
    try:
        with open(image_file, "rb") as f:
            img_bytes = f.read()
        b64 = base64.b64encode(img_bytes).decode()
    except:
        # إذا الصورة مش موجودة، استخدم خلفية لونية
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        </style>
        """, unsafe_allow_html=True)
        return
    
    padding_top = "105px" if login_page else "80px"  # قللت المسافة علشان ما يتراكبش

    page_bg_img = f"""
    <style>
    html, body {{
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
    }}

    .stApp {{
        background: url("data:image/png;base64,{b64}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}

    .main .block-container {{
        padding-top: {padding_top} !important;
        padding-bottom: 20px !important;
        max-width: 1200px !important;
    }}
    
    /* تحسين الأزرار */
    .stButton > button {{
        background: linear-gradient(90deg, #0072ff, #00c6ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        margin: 5px 0 !important;
    }}
    
    /* تحسين حقول الإدخال */
    .stTextInput > div > div > input {{
        background: rgba(255, 255, 255, 0.9) !important;
        color: black !important;
        border-radius: 8px !important;
    }}
    
    /* تحسين النصوص */
    h1, h2, h3, h4, h5, h6 {{
        color: white !important;
    }}
    
    /* تنسيق البطاقات */
    .custom-card {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    /* تنسيق التعليقات */
    .comment-box {{
        background: rgba(0, 0, 0, 0.3) !important;
        padding: 10px !important;
        border-radius: 8px !important;
        margin: 5px 0 !important;
    }}
    
    /* تنسيق التنبيهات */
    .stAlert {{
        border-radius: 8px !important;
    }}
    
    /* تنسيق الـ expander */
    .streamlit-expanderHeader {{
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }}
    
    /* تنسيق الـ selectbox */
    .stSelectbox > div > div {{
        background: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* تنسيق الـ textarea */
    .stTextArea > div > div > textarea {{
        background: rgba(255, 255, 255, 0.9) !important;
        color: black !important;
    }}
    
    /* تنسيق الـ file uploader */
    .stFileUploader > div {{
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# ----------------------------
# Custom Animations Functions
# ----------------------------
def show_confetti_animation():
    """Show confetti animation effect"""
    confetti_html = """
    <script>
    function createConfetti() {
        const colors = ['#FF5252', '#FF4081', '#E040FB', '#7C4DFF', '#536DFE', '#448AFF', '#40C4FF', '#18FFFF', '#64FFDA', '#69F0AE'];
        for(let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.width = Math.random() * 10 + 5 + 'px';
            confetti.style.height = Math.random() * 10 + 5 + 'px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.top = '-10px';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.borderRadius = '50%';
            confetti.style.zIndex = '9999';
            
            const animation = confetti.animate([
                { transform: 'translateY(0) rotate(0deg)', opacity: 1 },
                { transform: 'translateY(100vh) rotate(360deg)', opacity: 0 }
            ], {
                duration: Math.random() * 3000 + 2000,
                easing: 'cubic-bezier(0.215, 0.610, 0.355, 1)'
            });
            
            document.body.appendChild(confetti);
            animation.onfinish = () => confetti.remove();
        }
    }
    setTimeout(createConfetti, 100);
    </script>
    """
    st.components.v1.html(confetti_html, height=0)

# ----------------------------
# Users Database - نفسها
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
# Session State - نفسها
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

if "animation_shown" not in st.session_state:
    st.session_state.animation_shown = False

if "replying_to" not in st.session_state:
    st.session_state.replying_to = None

# ----------------------------
# Helper Functions - نفسها
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

def is_file_for_user(filename, username):
    name = filename.replace(".xlsx", "").replace(".xls", "").lower()
    parts = re.split(r"\s*-\s*", name)
    return any(username.lower() in p.strip() for p in parts)

def add_feedback(username, comment, replied_to=None, replied_by=None):
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
    df = load_feedback()
    
    if df.empty:
        return pd.DataFrame()
    
    user_notifications = df[
        (df['replied_to'] == username) & 
        (df['is_read'] == False)
    ].copy()
    
    return user_notifications

def get_unread_count(username):
    notifications = get_notifications(username)
    return len(notifications)

def mark_as_read(feedback_id):
    df = load_feedback()
    
    if not df.empty and 'id' in df.columns:
        df.loc[df['id'] == feedback_id, 'is_read'] = True
        df.to_csv(FEEDBACK_FILE, index=False)
        return True
    return False

def mark_all_as_read(username):
    df = load_feedback()
    
    if not df.empty:
        mask = (df['replied_to'] == username) & (df['is_read'] == False)
        df.loc[mask, 'is_read'] = True
        df.to_csv(FEEDBACK_FILE, index=False)
        return True
    return False

def delete_feedback(feedback_id):
    df = load_feedback()
    
    if not df.empty and 'id' in df.columns:
        initial_count = len(df)
        df = df[df['id'] != feedback_id]
        
        if len(df) < initial_count:
            df.to_csv(FEEDBACK_FILE, index=False)
            return True
    
    return False

def delete_all_feedback():
    if os.path.exists(FEEDBACK_FILE):
        os.remove(FEEDBACK_FILE)
        return True
    return False

def show_login_animation(username):
    with st.spinner(f"Welcome {username} Team! 🚀"):
        time.sleep(1.5)
    st.success(f"✅ Login successful! Welcome {username} Team! 👋")
    time.sleep(1)

# ----------------------------
# Login / Logout Logic
# ----------------------------
def login(username, password):
    for key, data in users.items():
        if username.lower() == key.lower() and password == data["password"]:
            st.session_state.logged_in = True
            st.session_state.user_role = data["role"]
            st.session_state.username = key
            st.session_state.show_welcome = True
            return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.current_page = "dashboard"
    st.session_state.show_welcome = True
    st.session_state.animation_shown = False
    st.session_state.replying_to = None

# ----------------------------
# Navigation Buttons - معدلة علشان تكون منظمة
# ----------------------------
def top_right_buttons():
    unread_count = 0
    if st.session_state.logged_in and st.session_state.current_page != "notifications":
        unread_count = get_unread_count(st.session_state.username)
    
    # استخدام columns منظمة
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("💬 Feedback", use_container_width=True):
            st.session_state.current_page = "feedback"
            st.rerun()
    
    with col3:
        button_label = "🔔 Notifications"
        if unread_count > 0:
            button_label = f"🔔 ({unread_count})"
        
        if st.button(button_label, use_container_width=True):
            st.session_state.current_page = "notifications"
            st.rerun()
    
    with col4:
        if st.button("ℹ️ About", use_container_width=True):
            st.session_state.current_page = "about"
            st.rerun()
    
    with col5:
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout()
            st.rerun()

# ----------------------------
# Welcome Message Component
# ----------------------------
def show_welcome_message():
    if st.session_state.show_welcome and st.session_state.logged_in:
        team_messages = {
            "Admin": "🎯 Admin Dashboard - Full Control",
            "CHC": "🏥 CHC Team - Healthcare Division",
            "CNS": "🧠 CNS Team - Neuroscience Division", 
            "GIT": "🩺 GIT Team - Gastroenterology",
            "Primary Care": "👨‍⚕️ Primary Care - General Medicine",
            "CVM": "❤️ CVM Team - Cardiology",
            "Power Team": "⚡ Power Team - Special Operations",
            "DGU": "🔧 DGU Team - Technical Division",
            "DNU": "📊 DNU Team - Data Analysis",
            "Sildava": "🌟 Sildava Team",
            "Ortho": "🦴 Ortho Team - Orthopedics",
            "All": "👁️ All Viewer - Full Access",
            "managers": "👨‍💼 Management View",
            "khalid": "👨‍💻 Developer View"
        }
        
        username = st.session_state.username
        message = team_messages.get(username.split()[0] if ' ' in username else username, 
                                   f"👋 Welcome {username.capitalize()} Team!")
        
        team_emojis = {
            "Admin": "👑",
            "CHC": "🏥",
            "CNS": "🧠", 
            "GIT": "🩺",
            "Primary": "👨‍⚕️",
            "CVM": "❤️",
            "Power": "⚡",
            "DGU": "🔧",
            "DNU": "📊",
            "Sildava": "🌟",
            "Ortho": "🦴",
            "khalid": "👨‍💻"
        }
        
        emoji = team_emojis.get(username.split()[0] if ' ' in username else username, "👋")
        
        unread_count = get_unread_count(username)
        notification_badge = ""
        if unread_count > 0 and st.session_state.current_page != "notifications":
            notification_badge = f'<span style="background: #FF5252; color: white; padding: 2px 8px; border-radius: 10px; margin-left: 10px; font-size: 0.9rem;">{unread_count} new</span>'
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin: 20px auto;
            color: white;
            font-size: 1.3rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            border: 2px solid rgba(255,255,255,0.3);
            backdrop-filter: blur(10px);
            max-width: 800px;
        ">
            <h3 style="color: white; margin-bottom: 8px;">{emoji} Hello {username.capitalize()} Team! {notification_badge}</h3>
            <p style="color: rgba(255,255,255,0.9); margin-top: 8px;">{message}</p>
            <div style="margin-top: 10px; font-size: 1.2rem;">
                📅 {date.today().strftime('%B %d, %Y')}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Display Feedback Card - معدلة
# ----------------------------
def display_feedback_card(row, is_admin=False):
    has_reply = pd.notna(row.get('replied_by')) and str(row.get('replied_by')).strip() != ''
    
    with st.container():
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 5px solid {'#00c6ff' if not has_reply else '#FF9800'};
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div><strong>👤 {row['username']}</strong></div>
                <div><small>📅 {row['datetime']}</small></div>
            </div>
            <div style="
                background: rgba(0, 0, 0, 0.3);
                padding: 10px;
                border-radius: 8px;
                margin: 10px 0;
                white-space: pre-wrap;
                word-break: break-word;
            ">
                {row['comment']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if has_reply:
            st.info(f"↩️ Replied by: {row['replied_by']}")
        
        if is_admin:
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🗑️ Delete", key=f"delete_{row['id']}", type="secondary", use_container_width=True):
                    if delete_feedback(row['id']):
                        st.success("✅ Feedback deleted!")
                        time.sleep(1)
                        st.rerun()
            
            with col_btn2:
                if st.button("📤 Reply", key=f"reply_{row['id']}", use_container_width=True):
                    st.session_state.replying_to = row['id']
                    st.rerun()
            
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
                        submit_reply = st.form_submit_button("Send Reply", type="primary", use_container_width=True)
                    with col_sub2:
                        cancel_reply = st.form_submit_button("Cancel", use_container_width=True)
                    
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

# ----------------------------
# Main Application UI
# ----------------------------
if not st.session_state.logged_in:
    set_bg_local("data/Untitled.png", True)
else:
    set_bg_local("data/Untitled.png", False)

# ---------- LOGIN PAGE ----------
if not st.session_state.logged_in:
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.1);
        width: 90%;
        max-width: 400px;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 100px auto;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    ">
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: white; margin-bottom: 30px;'>🔐 Login</h2>", unsafe_allow_html=True)
    
    u = st.text_input("", placeholder="👤 Username", key="login_username")
    p = st.text_input("", type="password", placeholder="🔒 Password", key="login_password")
    
    if st.button("🚀 Login to Dashboard", key="login_button", type="primary", use_container_width=True):
        if u and p:
            if login(u, p):
                show_login_animation(u)
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
        
        # Info Cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                border-left: 5px solid #00c6ff;
            ">
                <h4 style="color: #00c6ff; margin: 0;">📅 Today</h4>
                <p style="font-size: 1.5rem; margin: 5px 0;">{date.today().strftime('%d %b')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                border-left: 5px solid #00c6ff;
            ">
                <h4 style="color: #00c6ff; margin: 0;">👤 Role</h4>
                <p style="font-size: 1.5rem; margin: 5px 0;">{st.session_state.user_role}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            unread_count = get_unread_count(st.session_state.username)
            notification_text = f"{unread_count} unread" if unread_count > 0 else "All read"
            badge_color = "#FF5252" if unread_count > 0 else "#4CAF50"
            
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                border-left: 5px solid #00c6ff;
            ">
                <h4 style="color: #00c6ff; margin: 0;">🔔 Notifications</h4>
                <p style="font-size: 1.5rem; margin: 5px 0; color: {badge_color};">{notification_text}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Get folders
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
                
                # Admin Controls - ظاهرة بوضوح
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
                        
                        if uploaded_files and st.button("🚀 Upload Files", type="primary", key="upload_button", use_container_width=True):
                            os.makedirs(folder_path, exist_ok=True)
                            
                            success_count = 0
                            for file in uploaded_files:
                                file_path = os.path.join(folder_path, file.name)
                                with open(file_path, "wb") as f:
                                    f.write(file.getbuffer())
                                success_count += 1
                            
                            st.success(f"✅ {success_count} file(s) uploaded successfully!")
                            show_confetti_animation()
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
                                    col1, col2, col3 = st.columns([6, 1, 2])
                                    
                                    with col1:
                                        st.write(f"📄 **{file}**")
                                    
                                    with col2:
                                        if st.button("🗑️", key=f"del_{file}"):
                                            os.remove(path)
                                            st.success(f"Deleted: {file}")
                                            time.sleep(1)
                                            st.rerun()
                                    
                                    with col3:
                                        with open(path, "rb") as f:
                                            st.download_button(
                                                "📥 Download",
                                                f,
                                                file_name=file,
                                                key=f"dl_{file}",
                                                use_container_width=True
                                            )
                        else:
                            st.info("📭 No files available for this date.")
                    else:
                        st.info("📁 Folder doesn't exist yet.")
                
                st.markdown("---")
                st.subheader("📂 Available Files")
                
                if os.path.exists(folder_path):
                    if st.session_state.user_role == "AllViewer" or st.session_state.user_role == "Admin":
                        allowed_files = os.listdir(folder_path)
                    else:
                        allowed_files = [
                            f for f in os.listdir(folder_path)
                            if is_file_for_user(f, st.session_state.username)
                        ]
                    
                    if allowed_files:
                        for idx, file in enumerate(allowed_files):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"""
                                <div style="
                                    background: rgba(255,255,255,0.1);
                                    padding: 10px;
                                    border-radius: 8px;
                                    margin-bottom: 5px;
                                ">
                                    <p style="margin: 0;"><strong>📄 {file}</strong></p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col2:
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
    
    # ----- FEEDBACK PAGE -----
    elif st.session_state.current_page == "feedback":
        st.subheader("💬 Feedback System")
        
        if st.session_state.user_role == "Admin":
            df = load_feedback()
            if not df.empty:
                st.markdown(f"### 📋 Total Feedback: {len(df)}")
                
                if st.button("🗑️ Delete All Feedback", type="secondary", key="delete_all_btn", use_container_width=True):
                    if delete_all_feedback():
                        st.success("✅ All feedback deleted!")
                        show_confetti_animation()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete feedback")
                
                st.markdown("---")
                
                for idx, row in df.sort_values("datetime", ascending=False).iterrows():
                    display_feedback_card(row, is_admin=True)
                    st.markdown("---")
            else:
                st.info("📭 No feedback yet.")
        else:
            with st.form("feedback_form", clear_on_submit=True):
                st.markdown("### 📝 Share Your Thoughts")
                
                comment = st.text_area(
                    "Your feedback:",
                    placeholder="What's on your mind? Suggestions, issues, or comments...",
                    height=150,
                    key="user_feedback"
                )
                
                if st.form_submit_button("📤 Submit", type="primary", use_container_width=True):
                    if comment.strip():
                        add_feedback(st.session_state.username, comment.strip())
                        st.success("✅ Thank you for your feedback! 🌟")
                        show_confetti_animation()
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.warning("⚠️ Please write something before submitting.")
    
    # ----- NOTIFICATIONS PAGE -----
    elif st.session_state.current_page == "notifications":
        st.subheader("🔔 Your Notifications")
        
        notifications = get_notifications(st.session_state.username)
        
        if not notifications.empty:
            if st.button("✅ Mark All as Read", type="primary", key="mark_all_read", use_container_width=True):
                if mark_all_as_read(st.session_state.username):
                    st.success("All notifications marked as read!")
                    time.sleep(0.5)
                    st.rerun()
            
            st.markdown(f"### 📩 You have {len(notifications)} notification(s)")
            
            for idx, row in notifications.sort_values("datetime", ascending=False).iterrows():
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background: rgba(255, 255, 255, 0.15);
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 15px;
                        border-left: 4px solid #3498db;
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <div style="font-weight: bold; color: white; font-size: 16px;">
                                👤 {row['replied_by'] if pd.notna(row.get('replied_by')) else row['username']} replied to your feedback
                                <span style="background: #ff4444; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px; margin-left: 10px;">NEW</span>
                            </div>
                            <div style="color: #666; font-size: 14px;">📅 {row['datetime']}</div>
                        </div>
                        
                        <div style="
                            background: rgba(0, 0, 0, 0.2);
                            padding: 15px;
                            border-radius: 8px;
                            margin: 10px 0;
                            color: white;
                            font-size: 15px;
                        ">
                            {row['comment']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_btn1, _ = st.columns([1, 5])
                    with col_btn1:
                        if st.button("✓ Mark as Read", key=f"read_{row.get('id', idx)}", use_container_width=True):
                            if mark_as_read(row.get('id', idx)):
                                st.success("Notification marked as read!")
                                time.sleep(0.5)
                                st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("📭 No new notifications.")
    
    # ----- ABOUT PAGE -----
    elif st.session_state.current_page == "about":
        st.subheader("ℹ️ About This Dashboard")
        
        with st.container():
            st.markdown("""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                padding: 25px;
                border-radius: 15px;
                border-left: 5px solid #00c6ff;
                margin-bottom: 15px;
                backdrop-filter: blur(10px);
            ">
                <h3 style="color: #00c6ff;">🎯 Mission</h3>
                <p>Streamline daily sales operations and provide real-time insights for all teams.</p>
                
                <h3 style="color: #00c6ff;">✨ Features</h3>
                <p>✅ File Management - Upload and download sales files<br>
                ✅ Feedback System - Share thoughts and suggestions<br>
                ✅ Notifications - Get alerts for replies<br>
                ✅ Admin Controls - Manage feedback and files<br>
                ✅ Team-Based Access - Different views for different teams<br>
                ✅ Mobile Responsive - Works on all devices</p>
                
                <h3 style="color: #00c6ff;">👥 Teams</h3>
                <p>• Admin - Full system control<br>
                • CHC - Healthcare Division<br>
                • CNS - Neuroscience Division<br>
                • GIT - Gastroenterology<br>
                • Primary Care - General Medicine<br>
                • CVM - Cardiology Division<br>
                • Power Team - Special Operations<br>
                • All Teams - Comprehensive access</p>
            </div>
            """, unsafe_allow_html=True)

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