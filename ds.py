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
import html

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

    /* Animation for welcome message */
    @keyframes welcomeAnimation {{
        0% {{ transform: translateY(-20px); opacity: 0; }}
        100% {{ transform: translateY(0); opacity: 1; }}
    }}

    .welcome-container {{
        animation: welcomeAnimation 1s ease-out;
    }}

    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}

    .pulse-animation {{
        animation: pulse 2s infinite;
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}

    .float-animation {{
        animation: float 3s ease-in-out infinite;
    }}

    @keyframes shimmer {{
        0% {{ background-position: -200% center; }}
        100% {{ background-position: 200% center; }}
    }}

    .shimmer-effect {{
        background: linear-gradient(90deg, 
            rgba(255,255,255,0) 0%, 
            rgba(255,255,255,0.2) 50%, 
            rgba(255,255,255,0) 100%);
        background-size: 200% auto;
        animation: shimmer 3s infinite linear;
    }}

    @keyframes fadeInUp {{
        from {{ 
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{ 
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .fadeInUp {{
        animation: fadeInUp 0.8s ease-out;
    }}

    /* Notification badge */
    .notification-badge {{
        position: absolute;
        top: -5px;
        right: -5px;
        background: #FF5252;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }}

    /* Safe text display */
    .safe-text {{
        white-space: pre-wrap;
        word-break: break-word;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.5;
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
# Custom Animations Functions
# ----------------------------
def show_confetti_animation():
    """Show confetti animation effect"""
    confetti_html = """
    <style>
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background-color: #f00;
        top: 0;
        opacity: 0;
    }
    @keyframes confetti-fall {
        0% {
            top: -100px;
            opacity: 1;
            transform: rotate(0deg);
        }
        100% {
            top: 100vh;
            opacity: 0;
            transform: rotate(360deg);
        }
    }
    </style>
    <script>
    function createConfetti() {
        const colors = ['#FF5252', '#FF4081', '#E040FB', '#7C4DFF', '#536DFE', '#448AFF', '#40C4FF', '#18FFFF', '#64FFDA', '#69F0AE'];
        for(let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.width = Math.random() * 10 + 5 + 'px';
            confetti.style.height = Math.random() * 10 + 5 + 'px';
            confetti.style.animation = `confetti-fall ${Math.random() * 3 + 2}s linear forwards`;
            document.body.appendChild(confetti);
            setTimeout(() => confetti.remove(), 5000);
        }
    }
    setTimeout(createConfetti, 100);
    </script>
    """
    st.components.v1.html(confetti_html, height=0)

def show_fireworks_animation():
    """Show fireworks animation"""
    fireworks_html = """
    <canvas id="fireworksCanvas" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:9999;"></canvas>
    <script>
    const canvas = document.getElementById('fireworksCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const particles = [];
    const colors = ['#FF5252', '#FF4081', '#E040FB', '#7C4DFF', '#536DFE', '#448AFF', '#40C4FF'];
    
    class Particle {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            this.size = Math.random() * 3 + 1;
            this.speedX = Math.random() * 6 - 3;
            this.speedY = Math.random() * 6 - 3;
            this.color = colors[Math.floor(Math.random() * colors.length)];
            this.life = 100;
        }
        
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            this.life--;
            this.size *= 0.97;
        }
        
        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    function createFirework(x, y) {
        for(let i = 0; i < 50; i++) {
            particles.push(new Particle(x, y));
        }
    }
    
    // Create multiple fireworks
    setTimeout(() => createFirework(canvas.width/4, canvas.height/3), 100);
    setTimeout(() => createFirework(canvas.width/2, canvas.height/3), 300);
    setTimeout(() => createFirework(canvas.width*3/4, canvas.height/3), 500);
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        
        for(let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
            
            if(particles[i].life <= 0 || particles[i].size <= 0.5) {
                particles.splice(i, 1);
                i--;
            }
        }
        
        if(particles.length > 0) {
            requestAnimationFrame(animate);
        } else {
            canvas.remove();
        }
    }
    
    animate();
    </script>
    """
    st.components.v1.html(fireworks_html, height=0)

def show_loading_animation(text="Loading..."):
    """Show custom loading animation"""
    loading_html = f"""
    <div style="text-align: center; padding: 20px;">
        <div style="
            width: 50px;
            height: 50px;
            margin: 0 auto 15px;
            border: 5px solid rgba(0, 198, 255, 0.3);
            border-top: 5px solid #00c6ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        "></div>
        <p style="color: white; font-weight: bold;">{text}</p>
        <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        </style>
    </div>
    """
    return st.markdown(loading_html, unsafe_allow_html=True)

# ----------------------------
# Login + Dashboard UI Style
# ----------------------------
st.markdown("""
<style>
/* Welcome Message - Fixed in Dashboard */
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

.welcome-fixed h3 {
    color: white !important;
    margin-bottom: 8px !important;
    font-size: 1.8rem !important;
}

.welcome-fixed p {
    color: rgba(255,255,255,0.9) !important;
    margin-top: 8px !important;
    font-size: 1rem !important;
}

/* Success Message with Animation */
.success-animated {
    background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important;
    padding: 15px !important;
    border-radius: 10px !important;
    border: none !important;
    animation: pulse 2s infinite !important;
}

/* Notification Card */
.notification-card {
    background: rgba(255,255,255,0.15) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    margin-bottom: 15px !important;
    border-left: 5px solid #FF9800 !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.3s ease !important;
}

.notification-card:hover {
    background: rgba(255,255,255,0.2) !important;
    transform: translateY(-2px) !important;
}

.notification-card.read {
    border-left: 5px solid #4CAF50 !important;
    opacity: 0.8;
}

/* Comment Display Box */
.comment-box {
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
    max-height: 300px !important;
    overflow-y: auto !important;
}

.comment-box p {
    margin: 0 !important;
    color: rgba(255, 255, 255, 0.95) !important;
}

/* INPUT BOXES */
.stTextInput > div > div > input {
    text-align: left;
    font-size: 16px;
    padding: 10px;
    color: black !important;
    border-radius: 8px;
    background: rgba(255,255,255,0.9) !important;
}

/* ALL LABELS */
label[data-baseweb="label"],
.stSelectbox label,
.stFileUploader label,
.stTextInput label,
.stDateInput label {
    color: white !important;
    font-weight: bold !important;
}

/* SUBHEADERS & TEXT */
h1, h2, h3, h4, h5, h6,
.stSubheader,
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stText"] {
    color: white !important;
    font-weight: bold !important;
}

/* PLACEHOLDER */
input::placeholder {
    color: rgba(0,0,0,0.6) !important;
}

/* LOGIN BOX */
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
    animation: fadeInUp 0.8s ease-out !important;
}

/* BUTTONS */
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

/* BUTTON WITH NOTIFICATION BADGE */
.notification-btn {
    position: relative !important;
}

/* LOGIN BUTTON SPECIAL */
.login-btn {
    background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    margin-top: 20px !important;
}

/* DOWNLOAD BUTTON */
.stDownloadButton button {
    color: white !important;
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    transition: all 0.3s ease !important;
}

.stDownloadButton button:hover {
    background: linear-gradient(90deg, #0051cc, #0099cc);
    transform: scale(1.02) !important;
    color: white !important;
}

/* PROGRESS BAR STYLING */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
}

/* CARD STYLING */
.custom-card {
    background: rgba(255, 255, 255, 0.1) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    border-left: 5px solid #00c6ff !important;
    margin-bottom: 15px !important;
    backdrop-filter: blur(10px) !important;
}

/* REPLY CARD */
.reply-card {
    background: rgba(0, 198, 255, 0.1) !important;
    padding: 15px !important;
    border-radius: 10px !important;
    margin: 10px 0 15px 20px !important;
    border-left: 3px solid #00c6ff !important;
}

/* ABOUT PAGE STYLING */
.about-section {
    margin-bottom: 25px !important;
}

.about-section h4 {
    color: #00c6ff !important;
    margin-bottom: 15px !important;
    border-bottom: 2px solid rgba(0, 198, 255, 0.3) !important;
    padding-bottom: 8px !important;
}

.about-feature-list {
    margin-left: 20px !important;
    margin-bottom: 15px !important;
}

.about-feature-list li {
    margin-bottom: 8px !important;
    color: rgba(255, 255, 255, 0.9) !important;
}

@media only screen and (max-width: 768px) {
    .login-box {
        width: 90%;
        padding: 25px;
        margin-top: 60px;
    }
    
    .welcome-fixed {
        padding: 15px !important;
        margin: 0 10px 20px 10px !important;
        font-size: 1.1rem !important;
    }
    
    .welcome-fixed h3 {
        font-size: 1.4rem !important;
    }
    
    .comment-box {
        padding: 12px !important;
        font-size: 0.9rem !important;
    }
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

if "animation_shown" not in st.session_state:
    st.session_state.animation_shown = False

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
    لحل مشكلة ظهور الكود كـ HTML في الإشعارات
    """
    if not isinstance(text, str):
        return str(text)
    
    # تحويل HTML entities إلى نص عادي
    text = html.unescape(text)
    
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
    
    # تنظيف النص قبل الحفظ
    cleaned_comment = clean_text(comment) if comment else ""
    
    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_csv(FEEDBACK_FILE)
        # تأكد من وجود الأعمدة المطلوبة
        for col in ["id", "replied_to", "replied_by", "is_read"]:
            if col not in df.columns:
                df[col] = None
    else:
        df = pd.DataFrame(columns=["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"])
    
    # Generate unique ID
    feedback_id = str(uuid.uuid4())[:8]
    
    new_feedback = {
        "id": feedback_id,
        "username": username,
        "comment": cleaned_comment,
        "datetime": datetime.now(),
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
            # تنظيف التعليقات القديمة
            if 'comment' in df.columns:
                df['comment'] = df['comment'].apply(lambda x: clean_text(x) if isinstance(x, str) else x)
            
            # تأكد من وجود جميع الأعمدة
            required_columns = ["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"]
            for col in required_columns:
                if col not in df.columns:
                    df[col] = None
            
            # Generate IDs for old records if missing
            if df['id'].isna().any():
                df['id'] = df.apply(lambda x: str(uuid.uuid4())[:8] if pd.isna(x['id']) else x['id'], axis=1)
            
            # Set default values
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
    
    # الحصول على الردود الموجهة لهذا المستخدم وغير المقروءة
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
        # تحديث الردود الموجهة له
        mask = (df['replied_to'] == username) & (df['is_read'] == False)
        df.loc[mask, 'is_read'] = True
        df.to_csv(FEEDBACK_FILE, index=False)
        return True
    return False

def show_login_animation(username):
    """Show animation during login"""
    # Show loading animation first
    loading_placeholder = st.empty()
    loading_placeholder.markdown(show_loading_animation(f"Welcome {username} Team! 🚀"), unsafe_allow_html=True)
    
    time.sleep(1.5)
    
    # Clear loading
    loading_placeholder.empty()
    
    # Show success message
    st.success(f"✅ Login successful! Welcome {username} Team! 👋")
    
    # Mark animation as shown
    st.session_state.animation_shown = True
    
    # Small delay before redirect
    time.sleep(1)

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
    st.session_state.animation_shown = False

# ----------------------------
# Navigation Buttons (Top-Right)
# ----------------------------
def top_right_buttons():
    """Display navigation buttons at top-right"""
    # حساب عدد الإشعارات غير المقروءة
    unread_count = 0
    if st.session_state.logged_in and st.session_state.current_page != "notifications":
        unread_count = get_unread_count(st.session_state.username)
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 0.5])
    
    with col1:
        if st.button("💬 Feedback"):
            st.session_state.current_page = "feedback"
    
    with col2:
        # زر الإشعارات مع العداد
        button_label = "🔔 Notifications"
        if unread_count > 0:
            button_label = f"🔔 ({unread_count}) Notifications"
        
        if st.button(button_label, key="notifications_btn"):
            st.session_state.current_page = "notifications"
    
    with col3:
        if st.button("ℹ️ About"):
            st.session_state.current_page = "about"
    
    with col4:
        if st.button("🚪"):
            logout()
            st.rerun()

# ----------------------------
# Welcome Message Component
# ----------------------------
def show_welcome_message():
    """Display welcome message that stays in dashboard"""
    if st.session_state.show_welcome and st.session_state.logged_in:
        # Different messages based on team
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
        
        # Get appropriate message
        username = st.session_state.username
        message = team_messages.get(username.split()[0] if ' ' in username else username, 
                                   f"👋 Welcome {username.capitalize()} Team!")
        
        # Emojis based on team
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
        
        # عرض عدد الإشعارات غير المقروءة
        unread_count = get_unread_count(username)
        notification_badge = ""
        if unread_count > 0 and st.session_state.current_page != "notifications":
            notification_badge = f'<span style="background: #FF5252; color: white; padding: 2px 8px; border-radius: 10px; margin-left: 10px; font-size: 0.9rem;">{unread_count} new</span>'
        
        # Display welcome message
        st.markdown(f"""
        <div class="welcome-container">
            <div class="welcome-fixed">
                <h3>{emoji} Hello {username.capitalize()} Team! {notification_badge}</h3>
                <p>{message}</p>
                <div style="margin-top: 10px; font-size: 1.2rem;">
                    📅 {date.today().strftime('%B %d, %Y')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
    
    # Login Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: white; margin-bottom: 5px;">🔐 Login</h2>
        <p style="color: rgba(255,255,255,0.8);">Enter your credentials</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input fields
    u = st.text_input("", placeholder="👤 Username")
    p = st.text_input("", type="password", placeholder="🔒 Password")
    
    # Login button
    st.markdown('<div class="login-btn">', unsafe_allow_html=True)
    if st.button("🚀 Login to Dashboard"):
        if u and p:
            if login(u, p):
                # Show animation during login
                show_login_animation(u)
                st.rerun()
            else:
                st.error("❌ Wrong Username Or Password")
        else:
            st.warning("⚠️ Please enter both username and password")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DASHBOARD (Logged In) ----------
else:
    # Show navigation buttons
    top_right_buttons()
    
    # Show welcome message (ALWAYS VISIBLE in dashboard)
    show_welcome_message()
    
    # ----- DASHBOARD PAGE -----
    if st.session_state.current_page == "dashboard":
        st.subheader("📊 Daily Sales Dashboard")
        
        # Stats Card
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
            # عرض عدد الإشعارات غير المقروءة
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
        
        # Get available data
        folders = get_current_month_folders()
        
        if folders:
            selected_day = st.selectbox(
                "📅 Select Date:",
                folders,
                format_func=lambda x: f"📅 {x}",
                index=0
            )
            
            if selected_day:
                folder_path = os.path.join(BASE_PATH, selected_day)
                
                # ----- ADMIN DASHBOARD -----
                if st.session_state.user_role == "Admin":
                    st.markdown("---")
                    st.subheader("👨‍💼 Admin Controls")
                    
                    # File upload section
                    with st.expander("📤 Upload Files", expanded=True):
                        uploaded_files = st.file_uploader(
                            "Choose Excel files", 
                            type=["xlsx","xls"], 
                            accept_multiple_files=True,
                            key="admin_uploader"
                        )
                        
                        if uploaded_files and st.button("🚀 Upload Files", type="primary"):
                            today_folder = os.path.join(BASE_PATH, selected_day)
                            os.makedirs(today_folder, exist_ok=True)
                            
                            success_count = 0
                            for file in uploaded_files:
                                with open(os.path.join(today_folder, file.name), "wb") as f:
                                    f.write(file.getbuffer())
                                success_count += 1
                            
                            st.success(f"✅ {success_count} file(s) uploaded successfully!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                    
                    # File management section
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
                
                # ----- USER DASHBOARD -----
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
                            
                            # Display files in a nice grid
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
    
        # ----- FEEDBACK PAGE (المصحح) -----
    elif st.session_state.current_page == "feedback":
        st.subheader("💬 Feedback System")
        
        if st.session_state.user_role == "Admin":
            df = load_feedback()
            if not df.empty:
                st.markdown(f"### 📋 Total Feedback: {len(df)}")
                
                # Display feedback cards with reply option
                for idx, row in df.sort_values("datetime", ascending=False).iterrows():
                    with st.container():
                        # Determine card style based on reply status
                        has_reply = pd.notna(row.get('replied_by')) and str(row.get('replied_by')).strip() != ''
                        card_class = "notification-card" if has_reply else "custom-card"
                        border_color = "#FF9800" if has_reply else "#00c6ff"
                        
                        # Prepare reply HTML
                        reply_html = ""
                        if has_reply:
                            reply_by = str(row['replied_by']).strip()
                            reply_html = f'<span style="font-size: 0.9rem; color: #FF9800; margin-left: 10px;">↩️ Replied by {reply_by}</span>'
                        
                        # Prepare unread HTML
                        is_unread = not row.get('is_read', True)
                        unread_html = " | 🔔 Unread" if is_unread else ""
                        
                        st.markdown(f"""
                        <div class="fadeInUp">
                            <div class="{card_class}" style="border-left: 5px solid {border_color} !important;">
                                <div style="display: flex; justify-content: space-between; align-items: start;">
                                    <div>
                                        <p style="margin: 0; font-size: 1.1rem;">
                                            <strong>👤 {row['username']}</strong>
                                            {reply_html}
                                        </p>
                                        <p style="margin: 5px 0 10px 0; font-size: 0.9rem; color: rgba(255,255,255,0.8);">
                                            📅 {row['datetime']}
                                            {unread_html}
                                        </p>
                                    </div>
                                </div>
                                <div class="comment-box safe-text">
                                    {html.escape(str(row['comment']))}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)



                        
                        # Reply section for Admin only
                        with st.expander(f"💬 Reply to {row['username']}", expanded=False):
                            reply_text = st.text_area(
                                "Your reply:",
                                placeholder=f"Type your reply to {row['username']}...",
                                key=f"reply_{row.get('id', idx)}",
                                height=100
                            )
                            
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                if st.button("📤 Send Reply", key=f"send_{row.get('id', idx)}", type="primary"):
                                    if reply_text.strip():
                                        # Add reply as new feedback
                                        add_feedback(
                                            username=st.session_state.username,
                                            comment=reply_text,
                                            replied_to=row['username'],
                                            replied_by=st.session_state.username
                                        )
                                        st.success(f"✅ Reply sent to {row['username']}!")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.warning("Please write a reply first.")
            else:
                st.info("📭 No feedback yet.")
        else:
            # User feedback form
            with st.form("feedback_form", clear_on_submit=True):
                st.markdown("### 📝 Share Your Thoughts")
                
                comment = st.text_area(
                    "Your feedback:",
                    placeholder="What's on your mind? Suggestions, issues, or comments...",
                    height=150
                )
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    submit = st.form_submit_button("📤 Submit", type="primary")
                
                if submit and comment.strip():
                    add_feedback(st.session_state.username, comment.strip())
                    st.success("✅ Thank you for your feedback! 🌟")
                    time.sleep(1.5)
                    st.session_state.current_page = "dashboard"
                    st.rerun()
                elif submit:
                    st.warning("⚠️ Please write something before submitting.")
    
    # ----- NOTIFICATIONS PAGE -----
    elif st.session_state.current_page == "notifications":
        st.subheader("🔔 Your Notifications")
        
        notifications = get_notifications(st.session_state.username)
        
        if not notifications.empty:
            # زر Mark All as Read
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("✅ Mark All as Read", type="primary"):
                    if mark_all_as_read(st.session_state.username):
                        st.success("All notifications marked as read!")
                        time.sleep(0.5)
                        st.rerun()
            
            st.markdown(f"### 📩 You have {len(notifications)} notification(s)")
            
            for idx, row in notifications.sort_values("datetime", ascending=False).iterrows():
                with st.container():
                    # تحديد إذا كان الرد جديداً
                    is_new = not row.get('is_read', False)
                    replied_by = row.get('replied_by', '')
                    
                    st.markdown(f"""
                    <div class="fadeInUp">
                        <div class="{'notification-card' if is_new else 'notification-card read'}">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div>
                                    <p style="margin: 0; font-size: 1.1rem;">
                                        <strong>👤 {replied_by if replied_by else row['username']}</strong>
                                        {' replied to your feedback' if replied_by else ' posted new feedback'}
                                    </p>
                                    <p style="margin: 5px 0 10px 0; font-size: 0.9rem; color: rgba(255,255,255,0.8);">
                                        📅 {row['datetime']}
                                        {' | 🔔 NEW' if is_new else ' | ✅ Read'}
                                    </p>
                                </div>
                                {'' if not is_new else '<span style="background: #FF9800; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;">NEW</span>'}
                            </div>
                            
                            <div class="comment-box">
                                {str(row['comment'])}
                            </div>
                            
                            {f'<div style="margin-top: 10px; font-size: 0.9rem; color: #00c6ff;">↪️ In response to your feedback</div>' if replied_by else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # زر Mark as Read
                    if is_new:
                        col_btn1, col_btn2 = st.columns([1, 5])
                        with col_btn1:
                            if st.button("✓ Mark as Read", key=f"read_{row.get('id', idx)}"):
                                if mark_as_read(row.get('id', idx)):
                                    st.success("Notification marked as read!")
                                    time.sleep(0.5)
                                    st.rerun()
        else:
            st.info("📭 No new notifications.")
            
            # عرض كل الإشعارات السابقة
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
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div>
                                    <p style="margin: 0;"><strong>👤 {row['username']}</strong>
                                    {f"<span style='color: #FF9800; font-size: 0.9rem; margin-left: 10px;'>↩️ {row['replied_by']}</span>" if is_reply else ""}
                                    </p>
                                    <p style="margin: 5px 0; font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                                        📅 {row['datetime']}
                                    </p>
                                </div>
                            </div>
                            <div class="comment-box">
                                {str(row['comment'])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # زر العودة
        st.markdown("---")
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    # ----- ABOUT PAGE -----
    elif st.session_state.current_page == "about":
        st.subheader("ℹ️ About This Dashboard")
        
        # استخدام container للتحكم في التنسيق
        with st.container():
            st.markdown('<div class="custom-card fadeInUp">', unsafe_allow_html=True)
            
            # Mission Section
            st.markdown('<div class="about-section">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Mission")
            st.markdown("Streamline daily sales operations and provide real-time insights for all teams.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # New Features Section
            st.markdown('<div class="about-section">', unsafe_allow_html=True)
            st.markdown("#### ✨ New Features (v2.1)")
            st.markdown("""
            ✅ **Notification System** - Get alerts for feedback replies  
            ✅ **Reply to Feedback** - Admins can respond to user comments  
            ✅ **Real-time Badges** - See unread notifications count  
            ✅ **Mark as Read** - Manage your notifications  
            ✅ **HTML Safe Display** - No more code display issues
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Teams Section
            st.markdown('<div class="about-section">', unsafe_allow_html=True)
            st.markdown("#### 👥 Teams")
            st.markdown("""
            • **Admin** - Full system control + Reply to feedback  
            • **CHC** - Healthcare Division  
            • **CNS** - Neuroscience Division  
            • **GIT** - Gastroenterology  
            • **Primary Care** - General Medicine  
            • **CVM** - Cardiology Division  
            • **Power Team** - Special Operations  
            • **All Teams** - Comprehensive access
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # How Notifications Work
            st.markdown('<div class="about-section">', unsafe_allow_html=True)
            st.markdown("#### 🔔 How Notifications Work")
            st.markdown("""
            1. 📝 User submits feedback  
            2. 💬 Admin replies to the feedback  
            3. 🔔 User gets notification  
            4. 👁️ User can view and mark as read
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Footer
            st.markdown("""
            <div style="text-align: center; padding: 15px; background: rgba(0,198,255,0.1); border-radius: 10px; margin-top: 20px;">
                <p style="margin: 0; font-size: 1.1rem; color: white;">
                    🚀 <strong>Sales Dashboard v2.1 | Notification System Enabled</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Footer
# ----------------------------
if st.session_state.logged_in:
    st.markdown("---")
    # عرض حالة الإشعارات في الفوتر
    if st.session_state.logged_in and st.session_state.current_page != "notifications":
        unread_count = get_unread_count(st.session_state.username)
        notification_text = f" | 🔔 {unread_count} unread notification(s)" if unread_count > 0 else ""
    else:
        notification_text = ""
    
    st.markdown(f"""
    <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem; padding: 15px;">
        <p>📊 Sales Dashboard v2.1 | © 2024 | 🔒 Secure Access {notification_text}</p>
    </div>
    """, unsafe_allow_html=True)