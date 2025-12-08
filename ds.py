import streamlit as st
import warnings
import logging
import os
import pandas as pd
from datetime import datetime, date
import re
import base64
import time  # Added for animations

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

    /* Animation for welcome message */
    @keyframes welcomeAnimation {{
        0% {{ transform: scale(0.8); opacity: 0; }}
        70% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}

    .welcome-container {{
        animation: welcomeAnimation 1s ease-out;
    }}

    @keyframes slideIn {{
        from {{ transform: translateY(-30px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}

    .slide-in {{
        animation: slideIn 0.8s ease-out;
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
# Login + Dashboard UI Style
# ----------------------------
st.markdown("""
<style>
/* Welcome Message Special Styling */
.welcome-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    padding: 25px !important;
    border-radius: 15px !important;
    text-align: center !important;
    margin: 20px auto !important;
    color: white !important;
    font-size: 1.4rem !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    backdrop-filter: blur(10px) !important;
    max-width: 600px !important;
}

.welcome-message h2 {
    color: white !important;
    margin-bottom: 10px !important;
    font-size: 2rem !important;
}

.welcome-message p {
    color: rgba(255,255,255,0.9) !important;
    margin-top: 10px !important;
    font-size: 1.1rem !important;
}

/* INPUT BOXES */
.stTextInput > div > div > input {
    text-align: left;
    font-size: 16px;
    padding: 10px;
    color: black !important;
    border-radius: 8px;
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
    animation: slideIn 0.8s ease-out !important;
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

/* SUCCESS MESSAGE STYLING */
.stSuccess {
    background: rgba(0, 200, 83, 0.1) !important;
    border-left: 5px solid #00C853 !important;
    border-radius: 10px !important;
}

@media only screen and (max-width: 768px) {
    .login-box {
        width: 90%;
        padding: 25px;
        margin-top: 60px;
    }
    
    .welcome-message {
        padding: 20px !important;
        margin: 15px !important;
        font-size: 1.2rem !important;
    }
    
    .welcome-message h2 {
        font-size: 1.6rem !important;
    }
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

if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

# ----------------------------
# Paths
# ----------------------------
BASE_PATH = "data"
FEEDBACK_FILE = os.path.join(BASE_PATH, "feedback.csv")

# ----------------------------
# Helper Functions
# ----------------------------
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

def add_feedback(username, comment):
    """Add feedback to CSV file"""
    os.makedirs(BASE_PATH, exist_ok=True)
    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_csv(FEEDBACK_FILE)
    else:
        df = pd.DataFrame(columns=["username","comment","datetime"])
    df = pd.concat([df, pd.DataFrame([{"username": username,"comment":comment,"datetime":datetime.now()}])], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)

def load_feedback():
    """Load feedback from CSV file"""
    if os.path.exists(FEEDBACK_FILE):
        return pd.read_csv(FEEDBACK_FILE)
    else:
        return pd.DataFrame(columns=["username","comment","datetime"])

def show_welcome_animation(username):
    """Display animated welcome message"""
    # Balloon animation
    st.balloons()
    
    # Animated welcome message
    welcome_container = st.empty()
    
    # Animated progress bar
    progress_text = f"🚀 Preparing dashboard for {username} Team..."
    progress_bar = st.progress(0, text=progress_text)
    
    # Simulate loading animation
    for i in range(100):
        progress_bar.progress(i + 1, text=progress_text)
        time.sleep(0.02)  # Adjust speed
    
    # Clear progress bar
    progress_bar.empty()
    
    # Show final welcome message
    welcome_container.markdown(f"""
    <div class="welcome-container">
        <div class="welcome-message">
            <h2>🎉 Welcome {username} Team! 👋</h2>
            <p>🌟 Ready to explore today's sales data</p>
            <div style="margin-top: 15px; font-size: 2rem;">
                🚀 📊 💼
            </div>
            <p style="margin-top: 15px; font-size: 0.9rem; opacity: 0.8;">
                Dashboard loaded successfully!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hold the message for 2 seconds
    time.sleep(2)
    welcome_container.empty()
    st.session_state.welcome_shown = True

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
            return True
    return False

def logout():
    """Logout user and reset session"""
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.current_page = "dashboard"
    st.session_state.welcome_shown = False

# ----------------------------
# Navigation Buttons (Top-Right)
# ----------------------------
def top_right_buttons():
    """Display navigation buttons at top-right"""
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("💬 Feedback Inbox"):
            st.session_state.current_page = "feedback"
    with col2:
        if st.button("ℹ About Us"):
            st.session_state.current_page = "about"
    with col3:
        if st.button("🔴 Logout"):
            logout()
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
    
    # Login button with special styling
    st.markdown('<div class="login-btn">', unsafe_allow_html=True)
    if st.button("🚀 Login to Dashboard"):
        if u and p:
            if login(u, p):
                # Show welcome animation
                show_welcome_animation(u)
                st.rerun()
            else:
                st.error("❌ Wrong Username Or Password")
        else:
            st.warning("⚠ Please enter both username and password")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DASHBOARD (Logged In) ----------
else:
    # Display welcome message only once
    if not st.session_state.welcome_shown:
        st.markdown(f"""
        <div class="slide-in">
            <div class="welcome-message">
                <h2>👋 Hello {st.session_state.username} Team!</h2>
                <p>🌟 Welcome to Daily Sales Dashboard</p>
                <div style="margin-top: 10px; font-size: 1.5rem;">
                    📊 🚀 💼
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    top_right_buttons()
    
    # ----- DASHBOARD PAGE -----
    if st.session_state.current_page == "dashboard":
        st.subheader("📊 Daily Sales Dashboard")
        
        folders = get_current_month_folders()
        
        if folders:
            selected_day = folders[0]
            st.markdown(f"### 📅 Date: {selected_day}")
        else:
            st.warning("No available dates.")
            selected_day = None
        
        # ----- ADMIN DASHBOARD -----
        if st.session_state.user_role == "Admin":
            st.markdown("---")
            st.subheader("👨‍💼 Admin Dashboard")
            
            # File upload section
            uploaded_files = st.file_uploader(
                "📤 Upload Excel Files", 
                type=["xlsx","xls"], 
                accept_multiple_files=True,
                help="Upload daily sales Excel files"
            )
            
            if uploaded_files:
                today_folder = os.path.join(BASE_PATH, datetime.today().strftime("%Y-%m-%d"))
                os.makedirs(today_folder, exist_ok=True)
                
                success_count = 0
                for file in uploaded_files:
                    with open(os.path.join(today_folder, file.name), "wb") as f:
                        f.write(file.getbuffer())
                    success_count += 1
                
                st.success(f"✅ {success_count} file(s) uploaded successfully!")
                st.balloons()
            
            st.markdown("---")
            
            # File management section
            if selected_day:
                folder_path = os.path.join(BASE_PATH, selected_day)
                st.subheader("📁 File Management")
                
                if os.path.exists(folder_path):
                    files = os.listdir(folder_path)
                    if files:
                        for file in files:
                            path = os.path.join(folder_path, file)
                            c1, c2, c3 = st.columns([4,1,1])
                            
                            with c1:
                                st.write(f"📄 {file}")
                            
                            with c2:
                                if st.button("🗑️", key=f"del_{file}"):
                                    os.remove(path)
                                    st.warning(f"❌ File '{file}' deleted successfully")
                                    time.sleep(1)
                                    st.rerun()
                            
                            with c3:
                                with open(path, "rb") as f:
                                    st.download_button(
                                        "⬇️ Download",
                                        f,
                                        file_name=file,
                                        key=f"download_{file}"
                                    )
                    else:
                        st.info("📭 No files in this folder yet.")
                else:
                    st.info("📁 Folder doesn't exist yet.")
        
        # ----- USER DASHBOARD -----
        else:
            if selected_day:
                folder_path = os.path.join(BASE_PATH, selected_day)
                
                if os.path.exists(folder_path):
                    allowed_files = [
                        f for f in os.listdir(folder_path)
                        if st.session_state.user_role == "AllViewer"
                        or is_file_for_user(f, st.session_state.username)
                    ]
                    
                    if allowed_files:
                        st.markdown("### 📥 Download Your Files")
                        chosen = st.selectbox(
                            "Select a file:",
                            allowed_files,
                            format_func=lambda x: f"📄 {x}"
                        )
                        
                        if chosen:
                            path = os.path.join(folder_path, chosen)
                            with open(path, "rb") as f:
                                file_bytes = f.read()
                            
                            col1, col2 = st.columns([3,1])
                            with col1:
                                st.info(f"Selected: **{chosen}**")
                            with col2:
                                st.download_button(
                                    "🔽 Download File",
                                    data=file_bytes,
                                    file_name=chosen,
                                    key="user_download"
                                )
                    else:
                        st.warning("📭 No files available for your team yet.")
                else:
                    st.warning("📁 No data available for this date.")
    
    # ----- FEEDBACK PAGE -----
    elif st.session_state.current_page == "feedback":
        st.subheader("💬 Feedback Inbox")
        
        if st.session_state.user_role == "Admin":
            df = load_feedback()
            if not df.empty:
                st.markdown(f"### 📋 Total Feedback: {len(df)}")
                
                # Add filters for admin
                col1, col2 = st.columns(2)
                with col1:
                    users_filter = st.multiselect(
                        "Filter by user:",
                        df['username'].unique()
                    )
                
                if users_filter:
                    df = df[df['username'].isin(users_filter)]
                
                # Display feedback
                df_sorted = df.sort_values("datetime", ascending=False)
                for idx, row in df_sorted.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.1);
                                    padding: 15px;
                                    border-radius: 10px;
                                    margin-bottom: 10px;
                                    border-left: 4px solid #00c6ff;">
                            <p><strong>👤 {row['username']}</strong></p>
                            <p>{row['comment']}</p>
                            <p style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">
                                📅 {row['datetime']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("📭 No feedback yet.")
        else:
            # User feedback submission
            st.markdown("### 📝 Share Your Feedback")
            
            with st.form("feedback_form"):
                comment = st.text_area(
                    "Your message:",
                    placeholder="Type your feedback, suggestions, or issues here...",
                    height=150
                )
                
                submit = st.form_submit_button("📤 Submit Feedback")
                
                if submit:
                    if comment.strip():
                        add_feedback(st.session_state.username, comment.strip())
                        st.success("✅ Feedback submitted successfully! Thank you! 🌟")
                        time.sleep(1.5)
                        st.session_state.current_page = "dashboard"
                        st.rerun()
                    else:
                        st.warning("⚠ Please write something before submitting.")
    
    # ----- ABOUT PAGE -----
    elif st.session_state.current_page == "about":
        st.subheader("ℹ️ About Us")
        
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1);
                    padding: 25px;
                    border-radius: 15px;
                    margin-top: 20px;">
            <h3 style="color: #00c6ff;">👨‍💼 Our Team</h3>
            <p>• <strong>Ahmed</strong> – Admin</p>
            <p>• <strong>CHC Team</strong> – Sales Operations</p>
            <p>• <strong>CNS Teams</strong> – Central Nervous System Division</p>
            <p>• <strong>GIT Teams</strong> – Gastrointestinal Division</p>
            <p>• <strong>Primary Care</strong> – General Medicine</p>
            <p>• <strong>CVM</strong> – Cardiovascular Division</p>
            <p>• <strong>Power Team</strong> – Special Operations</p>
            <p>• And more dedicated professionals...</p>
            
            <h3 style="color: #00c6ff; margin-top: 30px;">🎯 Description</h3>
            <p>This dashboard is designed to manage daily sales files and feedback efficiently across all teams. 
            It provides secure access, easy file management, and a streamlined communication system.</p>
            
            <h3 style="color: #00c6ff; margin-top: 30px;">📈 Features</h3>
            <p>✅ Secure login system with role-based access</p>
            <p>✅ Daily sales file management</p>
            <p>✅ Feedback collection system</p>
            <p>✅ Admin controls for file management</p>
            <p>✅ Mobile-responsive design</p>
            
            <div style="margin-top: 30px; padding: 15px; background: rgba(0,198,255,0.1); border-radius: 10px;">
                <p style="text-align: center; margin: 0;">
                    🚀 <strong>Streamlining sales operations since 2024</strong>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Footer
# ----------------------------
if st.session_state.logged_in:
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem; padding: 20px;">
        <p>📊 Daily Sales Dashboard v1.0 | © 2024 All Rights Reserved</p>
        <p>👤 Logged in as: <strong>{username}</strong> | Role: <strong>{role}</strong></p>
    </div>
    """.format(
        username=st.session_state.username,
        role=st.session_state.user_role
    ), unsafe_allow_html=True)