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
# إخفاء التحذيرات
# ----------------------------
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)
os.environ["PYTHONWARNINGS"] = "ignore"

# ----------------------------
# خلفية الصفحة
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
        padding-bottom: 100px !important;
        max-width: 100% !important;
    }}

    header, footer {{
        visibility: hidden !important;
        height: 0px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# ----------------------------
# CSS مبسط
# ----------------------------
st.markdown("""
<style>
/* ألوان النصوص */
h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}

/* زر تسجيل الدخول */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white;
    border: none;
}

/* كارت الإشعارات */
.notification-card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}

.notification-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.notification-title {
    font-weight: bold;
    color: #333;
    font-size: 16px;
}

.notification-time {
    color: #666;
    font-size: 14px;
}

.notification-content-box {
    background: #f5f5f5;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    color: #333;
    font-size: 15px;
}

.new-badge {
    background: #ff4444;
    color: white;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}

/* أزرار التنقل */
.nav-button {
    background: rgba(255,255,255,0.2);
    color: white;
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 8px;
    padding: 10px 15px;
    margin: 5px;
    cursor: pointer;
    transition: all 0.3s;
}

.nav-button:hover {
    background: rgba(255,255,255,0.3);
}

/* رسالة الترحيب */
.welcome-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin: 20px auto;
    color: white;
    max-width: 600px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# قاعدة بيانات المستخدمين
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
# حالة الجلسة
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.current_page = "dashboard"

# ----------------------------
# المسارات
# ----------------------------
BASE_PATH = "data"
FEEDBACK_FILE = os.path.join(BASE_PATH, "feedback.csv")

# ----------------------------
# دوال المساعدة
# ----------------------------
def clean_text(text):
    """تنظيف النص"""
    if not isinstance(text, str):
        return str(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip()
    return text

def add_feedback(username, comment, replied_to=None, replied_by=None):
    """إضافة تعليق جديد"""
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
    """تحميل جميع التعليقات"""
    if os.path.exists(FEEDBACK_FILE):
        try:
            df = pd.read_csv(FEEDBACK_FILE)
            return df
        except:
            return pd.DataFrame(columns=["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"])
    else:
        return pd.DataFrame(columns=["id", "username", "comment", "datetime", "replied_to", "replied_by", "is_read"])

def get_notifications(username):
    """الحصول على إشعارات المستخدم"""
    df = load_feedback()
    
    if df.empty:
        return pd.DataFrame()
    
    user_notifications = df[
        (df['replied_to'] == username) & 
        (df['is_read'] == False)
    ].copy()
    
    return user_notifications

def get_unread_count(username):
    """عدد الإشعارات غير المقروءة"""
    notifications = get_notifications(username)
    return len(notifications)

def mark_as_read(feedback_id):
    """تحديد الإشعار كمقروء"""
    df = load_feedback()
    
    if not df.empty and 'id' in df.columns:
        df.loc[df['id'] == feedback_id, 'is_read'] = True
        df.to_csv(FEEDBACK_FILE, index=False)
        return True
    return False

def mark_all_as_read(username):
    """تحديد جميع الإشعارات كمقروءة"""
    df = load_feedback()
    
    if not df.empty:
        mask = (df['replied_to'] == username) & (df['is_read'] == False)
        df.loc[mask, 'is_read'] = True
        df.to_csv(FEEDBACK_FILE, index=False)
        return True
    return False

# ----------------------------
# تسجيل الدخول والخروج
# ----------------------------
def login(username, password):
    """تسجيل الدخول"""
    for key, data in users.items():
        if username.lower() == key.lower() and password == data["password"]:
            st.session_state.logged_in = True
            st.session_state.user_role = data["role"]
            st.session_state.username = key
            return True
    return False

def logout():
    """تسجيل الخروج"""
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.current_page = "dashboard"

# ----------------------------
# أزرار التنقل
# ----------------------------
def show_navigation():
    """عرض أزرار التنقل"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("💬 Feedback", use_container_width=True):
            st.session_state.current_page = "feedback"
            st.rerun()
    
    with col3:
        unread_count = 0
        if st.session_state.logged_in:
            unread_count = get_unread_count(st.session_state.username)
        
        label = "🔔 Notifications"
        if unread_count > 0:
            label = f"🔔 ({unread_count})"
        
        if st.button(label, use_container_width=True):
            st.session_state.current_page = "notifications"
            st.rerun()
    
    with col4:
        if st.button("ℹ️ About", use_container_width=True):
            st.session_state.current_page = "about"
            st.rerun()
    
    with col5:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout()
            st.rerun()

# ----------------------------
# صفحة الإشعارات - تصميم مبسط
# ----------------------------
def show_notifications_page():
    """عرض صفحة الإشعارات بشكل مبسط"""
    st.title("🔔 Your Notifications")
    
    notifications = get_notifications(st.session_state.username)
    unread_count = len(notifications)
    
    # زر Mark All as Read
    if unread_count > 0:
        if st.button("✅ Mark All as Read", type="primary", use_container_width=True):
            if mark_all_as_read(st.session_state.username):
                st.success("All notifications marked as read!")
                time.sleep(1)
                st.rerun()
    
    st.markdown(f"**You have {unread_count} notification(s)**")
    st.markdown("---")
    
    if not notifications.empty:
        for idx, row in notifications.sort_values("datetime", ascending=False).iterrows():
            # كارت الإشعار
            with st.container():
                st.markdown(f"""
                <div class="notification-card">
                    <div class="notification-header">
                        <div class="notification-title">
                            👤 {row.get('replied_by', 'admin')} replied to your feedback
                            <span class="new-badge">NEW</span>
                        </div>
                        <div class="notification-time">
                            📅 {row['datetime']}
                        </div>
                    </div>
                    
                    <div class="notification-content-box">
                        {row['comment']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # زر Mark as Read
                if st.button("✔ Mark as Read", key=f"read_{row['id']}", use_container_width=True):
                    if mark_as_read(row['id']):
                        st.success("Notification marked as read!")
                        time.sleep(1)
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("📭 No new notifications.")
    
    # زر العودة
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.current_page = "dashboard"
        st.rerun()

# ----------------------------
# صفحة Dashboard
# ----------------------------
def show_dashboard():
    """عرض صفحة Dashboard"""
    st.title("📊 Sales Dashboard")
    
    # رسالة الترحيب
    st.markdown(f"""
    <div class="welcome-box">
        <h3>👋 Welcome {st.session_state.username}!</h3>
        <p>Today is {date.today().strftime('%B %d, %Y')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # معلومات سريعة
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📅 Today", date.today().strftime('%d %b'))
    
    with col2:
        st.metric("👤 Role", st.session_state.user_role)
    
    with col3:
        unread_count = get_unread_count(st.session_state.username)
        st.metric("🔔 Notifications", f"{unread_count} unread" if unread_count > 0 else "All read")
    
    st.markdown("---")
    
    # محتوى Dashboard
    if st.session_state.user_role == "Admin":
        st.subheader("👨‍💼 Admin Panel")
        st.write("Upload and manage files here.")
        
        # مثال بسيط لرفع الملفات
        uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
        if uploaded_file is not None:
            st.success(f"File {uploaded_file.name} uploaded successfully!")
    
    else:
        st.subheader("📁 Your Files")
        st.info("Your files will appear here.")

# ----------------------------
# صفحة Feedback
# ----------------------------
def show_feedback_page():
    """عرض صفحة Feedback"""
    st.title("💬 Feedback System")
    
    if st.session_state.user_role == "Admin":
        # عرض جميع التعليقات للمسؤول
        df = load_feedback()
        
        if not df.empty:
            st.subheader(f"Total Feedback: {len(df)}")
            
            for idx, row in df.sort_values("datetime", ascending=False).iterrows():
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**👤 {row['username']}**")
                    with col2:
                        st.caption(f"📅 {row['datetime']}")
                    
                    st.markdown(f"""
                    <div style="
                        background: rgba(255,255,255,0.1);
                        padding: 15px;
                        border-radius: 10px;
                        margin: 10px 0;
                        color: white;
                    ">
                        {row['comment']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if pd.notna(row.get('replied_by')):
                        st.info(f"↩️ Replied by: {row['replied_by']}")
                    
                    # أزرار للمسؤول
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button("🗑️ Delete", key=f"delete_{row['id']}"):
                            # كود الحذف هنا
                            st.success("Feedback deleted!")
                            time.sleep(1)
                            st.rerun()
                    
                    with col_btn2:
                        if st.button("📤 Reply", key=f"reply_{row['id']}"):
                            st.session_state.replying_to = row['id']
                            st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No feedback yet.")
    
    else:
        # نموذج إرسال تعليق للمستخدمين العاديين
        with st.form("feedback_form"):
            st.subheader("📝 Share Your Feedback")
            
            comment = st.text_area("Your message:", height=150)
            
            if st.form_submit_button("📤 Submit", use_container_width=True):
                if comment.strip():
                    add_feedback(st.session_state.username, comment.strip())
                    st.success("✅ Thank you for your feedback!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Please write something first.")

# ----------------------------
# صفحة About
# ----------------------------
def show_about_page():
    """عرض صفحة About"""
    st.title("ℹ️ About This Dashboard")
    
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    ">
        <h3>🎯 Mission</h3>
        <p>Streamline daily sales operations and provide real-time insights for all teams.</p>
        
        <h3>✨ Features</h3>
        <p>✅ File Management<br>
           ✅ Feedback System<br>
           ✅ Notifications<br>
           ✅ Admin Controls<br>
           ✅ Team-Based Access</p>
        
        <h3>👥 Teams</h3>
        <p>• Admin - Full system control<br>
           • CHC - Healthcare Division<br>
           • CNS - Neuroscience Division<br>
           • GIT - Gastroenterology<br>
           • Primary Care - General Medicine</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# التطبيق الرئيسي
# ----------------------------
def main():
    # تعيين الخلفية
    if not st.session_state.logged_in:
        set_bg_local("data/Untitled.png", True)
    else:
        set_bg_local("data/Untitled.png", False)
    
    # صفحة تسجيل الدخول
    if not st.session_state.logged_in:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.1);
            width: 400px;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin: 100px auto;
            backdrop-filter: blur(10px);
        ">
            <h2 style="color: white; margin-bottom: 30px;">🔐 Login</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("", placeholder="👤 Username", key="login_username")
            password = st.text_input("", type="password", placeholder="🔒 Password", key="login_password")
            
            if st.button("🚀 Login", use_container_width=True, type="primary"):
                if username and password:
                    if login(username, password):
                        st.success(f"Welcome {username}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Wrong username or password")
                else:
                    st.warning("Please enter both username and password")
    
    # الصفحات بعد تسجيل الدخول
    else:
        # أزرار التنقل
        show_navigation()
        
        # عرض الصفحة المحددة
        if st.session_state.current_page == "dashboard":
            show_dashboard()
        
        elif st.session_state.current_page == "feedback":
            show_feedback_page()
        
        elif st.session_state.current_page == "notifications":
            show_notifications_page()
        
        elif st.session_state.current_page == "about":
            show_about_page()
        
        # الفوتر
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.6); padding: 20px;">
            <p>📊 Sales Dashboard | © 2024</p>
        </div>
        """, unsafe_allow_html=True)

# تشغيل التطبيق
if __name__ == "__main__":
    main()