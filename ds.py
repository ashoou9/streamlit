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

    /* Medical Animations */
    @keyframes pillFloat {{
        0% {{ transform: translateY(100vh) rotate(0deg); opacity: 0; }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 1; }}
        100% {{ transform: translateY(-100px) rotate(360deg); opacity: 0; }}
    }}

    @keyframes syringeFloat {{
        0% {{ transform: translateX(-100px) rotate(-45deg); opacity: 0; }}
        20% {{ opacity: 1; }}
        80% {{ opacity: 1; }}
        100% {{ transform: translateX(100vw) rotate(45deg); opacity: 0; }}
    }}

    @keyframes heartbeat {{
        0% {{ transform: scale(1); }}
        25% {{ transform: scale(1.1); }}
        50% {{ transform: scale(1); }}
        75% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}

    @keyframes dnaSpin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

    @keyframes stethoscopeMove {{
        0% {{ transform: translateX(0) rotate(0deg); }}
        50% {{ transform: translateX(20px) rotate(10deg); }}
        100% {{ transform: translateX(0) rotate(0deg); }}
    }}

    @keyframes capsuleBounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-20px); }}
    }}

    @keyframes welcomeSlide {{
        0% {{ transform: translateX(-100%); opacity: 0; }}
        100% {{ transform: translateX(0); opacity: 1; }}
    }}

    .heartbeat {{ animation: heartbeat 1.5s infinite; }}
    .dna-spin {{ animation: dnaSpin 10s linear infinite; }}
    .stethoscope {{ animation: stethoscopeMove 2s ease-in-out infinite; }}
    .capsule {{ animation: capsuleBounce 2s ease-in-out infinite; }}
    .welcome-slide {{ animation: welcomeSlide 1s ease-out; }}

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
# Medical Animations Functions
# ----------------------------
def show_medical_welcome(username):
    """Show medical-themed welcome animation"""
    
    # Create pills floating animation
    pills_html = """
    <div id="pillsContainer" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:9998;"></div>
    <script>
    function createPill() {
        const container = document.getElementById('pillsContainer');
        const pill = document.createElement('div');
        
        // Random pill styles
        const colors = ['#FF5252', '#FF4081', '#E040FB', '#7C4DFF', '#536DFE', '#448AFF', '#40C4FF', '#18FFFF'];
        const shapes = ['pill', 'capsule', 'round'];
        const shape = shapes[Math.floor(Math.random() * shapes.length)];
        
        pill.style.position = 'absolute';
        pill.style.left = Math.random() * 100 + 'vw';
        pill.style.width = Math.random() * 30 + 20 + 'px';
        pill.style.height = Math.random() * 15 + 10 + 'px';
        pill.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        pill.style.borderRadius = shape === 'round' ? '50%' : (shape === 'capsule' ? '50px' : '10px');
        pill.style.opacity = '0.7';
        pill.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
        
        // Animation
        const duration = Math.random() * 3 + 2;
        pill.style.animation = `pillFloat ${duration}s linear forwards`;
        
        container.appendChild(pill);
        setTimeout(() => pill.remove(), duration * 1000);
    }
    
    // Create multiple pills
    for(let i = 0; i < 15; i++) {
        setTimeout(() => createPill(), i * 200);
    }
    </script>
    """
    
    # DNA Helix Animation
    dna_html = """
    <div style="position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); z-index:9997; opacity:0.1;">
        <div style="font-size: 100px;" class="dna-spin">
        🧬
        </div>
    </div>
    """
    
    # Show animations
    st.components.v1.html(pills_html, height=0)
    st.markdown(dna_html, unsafe_allow_html=True)
    
    # Success message with medical theme
    success_msg = st.empty()
    success_msg.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 20px auto;
        max-width: 500px;
        animation: welcomeSlide 1s ease-out;
    ">
        <div style="font-size: 50px; margin-bottom: 10px;">💊 🩺</div>
        <h2 style="margin: 10px 0;">Welcome {username} Team!</h2>
        <p style="opacity: 0.9;">Accessing Pharmaceutical Dashboard...</p>
        <div style="margin-top: 15px; font-size: 24px;">
            <span class="heartbeat" style="display: inline-block;">❤️</span>
            <span class="capsule" style="display: inline-block; animation-delay: 0.5s;">💊</span>
            <span class="stethoscope" style="display: inline-block; animation-delay: 1s;">🩺</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(2.5)
    success_msg.empty()

def show_prescription_animation():
    """Show prescription writing animation"""
    prescription_html = """
    <div style="
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: writePrescription 3s ease-in-out forwards;
        max-width: 400px;
    ">
        <div style="text-align: center;">
            <div style="font-size: 40px; margin-bottom: 15px;">📝</div>
            <h3 style="color: #333; margin: 0;">Prescription Ready!</h3>
            <p style="color: #666; margin-top: 10px;">Data loaded successfully</p>
        </div>
    </div>
    <style>
    @keyframes writePrescription {
        0% { 
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.5);
        }
        30% { 
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.05);
        }
        70% { 
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
        100% { 
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.5);
        }
    }
    </style>
    """
    st.components.v1.html(prescription_html, height=0)

def show_medicine_drop():
    """Show medicine drop animation"""
    drop_html = """
    <div id="dropsContainer" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:9998;"></div>
    <script>
    function createMedicineDrop() {
        const container = document.getElementById('dropsContainer');
        const drop = document.createElement('div');
        
        // Random drop styles
        const medicines = ['💊', '💉', '🧪', '🧫', '🩹', '🩺', '🌡️', '💊', '💊'];
        const medicine = medicines[Math.floor(Math.random() * medicines.length)];
        
        drop.innerHTML = medicine;
        drop.style.position = 'absolute';
        drop.style.left = Math.random() * 100 + 'vw';
        drop.style.fontSize = Math.random() * 20 + 20 + 'px';
        drop.style.opacity = '0';
        
        // Animation
        const duration = Math.random() * 2 + 1;
        drop.style.animation = `
            dropFall ${duration}s ease-in forwards,
            fadeInOut ${duration}s ease-in-out forwards
        `;
        
        container.appendChild(drop);
        setTimeout(() => drop.remove(), duration * 1000);
    }
    
    // Create multiple drops
    for(let i = 0; i < 20; i++) {
        setTimeout(() => createMedicineDrop(), i * 100);
    }
    
    // CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes dropFall {
            0% { transform: translateY(-100px) rotate(0deg); }
            100% { transform: translateY(100vh) rotate(360deg); }
        }
        @keyframes fadeInOut {
            0%, 100% { opacity: 0; }
            50% { opacity: 0.8; }
        }
    `;
    document.head.appendChild(style);
    </script>
    """
    st.components.v1.html(drop_html, height=0)

def show_heartbeat_loader(text="Loading Health Data..."):
    """Show heartbeat loading animation"""
    heartbeat_html = f"""
    <div style="text-align: center; padding: 30px;">
        <div style="
            display: inline-block;
            animation: heartbeat 1.5s infinite;
            font-size: 60px;
            margin-bottom: 20px;
        ">
            ❤️
        </div>
        <p style="color: white; font-weight: bold; font-size: 18px;">{text}</p>
        <div style="
            width: 200px;
            height: 4px;
            background: rgba(255,255,255,0.2);
            border-radius: 2px;
            margin: 20px auto;
            overflow: hidden;
        ">
            <div style="
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, #FF5252, #FF4081);
                animation: loadingBar 2s ease-in-out infinite;
            "></div>
        </div>
        <style>
        @keyframes loadingBar {{
            0%, 100% {{ transform: translateX(-100%); }}
            50% {{ transform: translateX(100%); }}
        }}
        </style>
    </div>
    """
    return st.markdown(heartbeat_html, unsafe_allow_html=True)

# ----------------------------
# Login + Dashboard UI Style
# ----------------------------
st.markdown("""
<style>
/* Medical Theme Welcome Message */
.welcome-medical {
    background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%) !important;
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
    position: relative;
    overflow: hidden;
}

.welcome-medical::before {
    content: "💊 🩺 🌡️";
    position: absolute;
    top: -20px;
    right: -20px;
    font-size: 60px;
    opacity: 0.1;
    transform: rotate(15deg);
}

.welcome-medical h3 {
    color: white !important;
    margin-bottom: 8px !important;
    font-size: 1.8rem !important;
    position: relative;
    z-index: 2;
}

.welcome-medical p {
    color: rgba(255,255,255,0.9) !important;
    margin-top: 8px !important;
    font-size: 1rem !important;
    position: relative;
    z-index: 2;
}

/* Medical Cards */
.medical-card {
    background: rgba(255, 255, 255, 0.1) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    border-left: 5px solid #26d0ce !important;
    margin-bottom: 15px !important;
    backdrop-filter: blur(10px) !important;
    transition: transform 0.3s ease !important;
}

.medical-card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
}

/* Medical Buttons */
.medical-btn {
    background: linear-gradient(90deg, #1a2980, #26d0ce) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
}

.medical-btn:hover {
    background: linear-gradient(90deg, #0d1a66, #1cb5b3) !important;
    transform: scale(1.05) !important;
}

/* Medical Icons */
.medical-icon {
    font-size: 24px !important;
    margin-right: 10px !important;
    vertical-align: middle !important;
}

/* INPUT BOXES */
.stTextInput > div > div > input {
    text-align: left;
    font-size: 16px;
    padding: 12px;
    color: black !important;
    border-radius: 10px;
    background: rgba(255,255,255,0.95) !important;
    border: 2px solid #26d0ce !important;
}

/* LOGIN BOX - Medical Theme */
.login-medical-box {
    background: rgba(255, 255, 255, 0.15) !important;
    width: 420px;
    max-width: 90%;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    margin: 60px auto 0 auto;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2) !important;
    animation: welcomeSlide 1s ease-out !important;
}

.login-medical-box::before {
    content: "💊 🩺";
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 40px;
    opacity: 0.2;
}

/* MEDICAL SUCCESS MESSAGE */
.medical-success {
    background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important;
    padding: 15px 25px !important;
    border-radius: 12px !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
    animation: heartbeat 2s infinite !important;
    border-left: 5px solid white !important;
}

/* MEDICAL HEADERS */
.medical-header {
    background: linear-gradient(90deg, #1a2980, #26d0ce) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    padding: 10px 0 !important;
    border-bottom: 3px solid #26d0ce !important;
    display: inline-block !important;
    margin-bottom: 20px !important;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #1a2980, #26d0ce);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #0d1a66, #1cb5b3);
}

@media only screen and (max-width: 768px) {
    .login-medical-box {
        width: 90%;
        padding: 25px;
        margin-top: 60px;
    }
    
    .welcome-medical {
        padding: 15px !important;
        margin: 0 10px 20px 10px !important;
        font-size: 1.1rem !important;
    }
    
    .welcome-medical h3 {
        font-size: 1.4rem !important;
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

if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

if "medical_animation_shown" not in st.session_state:
    st.session_state.medical_animation_shown = False

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
    st.session_state.medical_animation_shown = False

# ----------------------------
# Navigation Buttons (Top-Right)
# ----------------------------
def top_right_buttons():
    """Display navigation buttons at top-right"""
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("💊 Feedback"):
            st.session_state.current_page = "feedback"
    with col2:
        if st.button("🩺 About"):
            st.session_state.current_page = "about"
    with col3:
        if st.button("🚪 Logout"):
            logout()
            st.rerun()

# ----------------------------
# Medical Welcome Message Component
# ----------------------------
def show_medical_welcome_message():
    """Display medical-themed welcome message"""
    if st.session_state.show_welcome and st.session_state.logged_in:
        # Medical department emojis and messages
        department_info = {
            "CHC": {"emoji": "🏥", "message": "Healthcare Division"},
            "CNS": {"emoji": "🧠", "message": "Neuroscience Division"}, 
            "GIT": {"emoji": "🩺", "message": "Gastroenterology"},
            "Primary Care": {"emoji": "👨‍⚕️", "message": "General Medicine"},
            "CVM": {"emoji": "❤️", "message": "Cardiology Division"},
            "Power Team": {"emoji": "⚡", "message": "Special Operations"},
            "DGU": {"emoji": "🔧", "message": "Technical Division"},
            "DNU": {"emoji": "📊", "message": "Data Analysis"},
            "Sildava": {"emoji": "🌟", "message": "Sildava Team"},
            "Ortho": {"emoji": "🦴", "message": "Orthopedics"},
            "Admin": {"emoji": "👑", "message": "Pharmaceutical Admin"},
            "All": {"emoji": "👁️", "message": "Full Access"},
            "managers": {"emoji": "👨‍💼", "message": "Management View"}
        }
        
        username = st.session_state.username
        dept_key = username.split()[0] if ' ' in username else username
        info = department_info.get(dept_key, {"emoji": "💊", "message": "Medical Team"})
        
        # Display medical welcome message
        st.markdown(f"""
        <div class="welcome-slide">
            <div class="welcome-medical">
                <h3>{info['emoji']} Welcome {username}!</h3>
                <p>{info['message']} • Pharmaceutical Dashboard</p>
                <div style="margin-top: 15px; font-size: 24px; opacity: 0.8;">
                    <span class="heartbeat">❤️</span>
                    <span class="capsule" style="animation-delay: 0.3s;">💊</span>
                    <span class="stethoscope" style="animation-delay: 0.6s;">🩺</span>
                </div>
                <div style="margin-top: 10px; font-size: 0.9rem; opacity: 0.7;">
                    📅 {date.today().strftime('%B %d, %Y')} | 👤 {st.session_state.user_role}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Medical Stats Cards
# ----------------------------
def show_medical_stats():
    """Display medical statistics cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="medical-card">
            <div style="font-size: 30px; color: #26d0ce; margin-bottom: 10px;">💊</div>
            <h4 style="margin: 0; color: white;">Today's Data</h4>
            <p style="font-size: 1.8rem; margin: 10px 0; color: #26d0ce;">{date.today().strftime('%d %b')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="medical-card">
            <div style="font-size: 30px; color: #FF5252; margin-bottom: 10px;">🩺</div>
            <h4 style="margin: 0; color: white;">Department</h4>
            <p style="font-size: 1.5rem; margin: 10px 0; color: #FF5252;">{st.session_state.username}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status_emoji = "✅" if st.session_state.logged_in else "❌"
        st.markdown(f"""
        <div class="medical-card">
            <div style="font-size: 30px; color: #00C853; margin-bottom: 10px;">🌡️</div>
            <h4 style="margin: 0; color: white;">System Status</h4>
            <p style="font-size: 1.5rem; margin: 10px 0; color: #00C853;">Active {status_emoji}</p>
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
    st.markdown('<div class="login-medical-box">', unsafe_allow_html=True)
    
    # Medical Login Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 50px; margin-bottom: 10px;">💊 🩺</div>
        <h2 style="color: white; margin-bottom: 5px;">Pharmaceutical Access</h2>
        <p style="color: rgba(255,255,255,0.8);">Medical Dashboard Login</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input fields with medical icons
    u = st.text_input("", placeholder="👤 Medical ID / Username")
    p = st.text_input("", type="password", placeholder="🔒 Secure Password")
    
    # Medical-themed login button
    if st.button("💉 Access Dashboard", use_container_width=True):
        if u and p:
            if login(u, p):
                # Show medical animations
                show_medical_welcome(u)
                st.session_state.medical_animation_shown = True
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ Invalid Medical Credentials")
        else:
            st.warning("⚠️ Please enter both credentials")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DASHBOARD (Logged In) ----------
else:
    # Show medical navigation buttons
    top_right_buttons()
    
    # Show medical welcome message
    show_medical_welcome_message()
    
    # ----- DASHBOARD PAGE -----
    if st.session_state.current_page == "dashboard":
        # Medical stats cards
        show_medical_stats()
        
        st.markdown('<h3 class="medical-header">📊 Pharmaceutical Sales Dashboard</h3>', unsafe_allow_html=True)
        
        # Get available data
        folders = get_current_month_folders()
        
        if folders:
            selected_day = st.selectbox(
                "📅 Select Medical Report Date:",
                folders,
                format_func=lambda x: f"📅 {x}",
                index=0
            )
            
            if selected_day:
                folder_path = os.path.join(BASE_PATH, selected_day)
                
                # ----- ADMIN DASHBOARD -----
                if st.session_state.user_role == "Admin":
                    st.markdown("---")
                    st.markdown('<h3 class="medical-header">👨‍⚕️ Admin Controls</h3>', unsafe_allow_html=True)
                    
                    # File upload section with medical theme
                    with st.expander("💾 Upload Medical Reports", expanded=True):
                        uploaded_files = st.file_uploader(
                            "Select medical report files", 
                            type=["xlsx","xls"], 
                            accept_multiple_files=True,
                            key="medical_uploader"
                        )
                        
                        if uploaded_files:
                            if st.button("💊 Upload Medical Reports", type="primary", use_container_width=True):
                                today_folder = os.path.join(BASE_PATH, selected_day)
                                os.makedirs(today_folder, exist_ok=True)
                                
                                success_count = 0
                                for file in uploaded_files:
                                    with open(os.path.join(today_folder, file.name), "wb") as f:
                                        f.write(file.getbuffer())
                                    success_count += 1
                                
                                # Show prescription animation on successful upload
                                show_prescription_animation()
                                st.success(f"✅ {success_count} medical report(s) uploaded!")
                                time.sleep(2)
                                st.rerun()
                    
                    # File management section
                    st.markdown("---")
                    st.markdown('<h3 class="medical-header">📁 Medical Report Management</h3>', unsafe_allow_html=True)
                    
                    if os.path.exists(folder_path):
                        files = os.listdir(folder_path)
                        if files:
                            for file in files:
                                path = os.path.join(folder_path, file)
                                with st.container():
                                    st.markdown(f"""
                                    <div class="medical-card">
                                        <div style="display: flex; justify-content: space-between; align-items: center;">
                                            <div>
                                                <span style="font-size: 20px;">📄</span>
                                                <strong style="margin-left: 10px;">{file}</strong>
                                            </div>
                                            <div>
                                                <button onclick="showMedicineDrop()" style="
                                                    background: #26d0ce;
                                                    color: white;
                                                    border: none;
                                                    padding: 5px 10px;
                                                    border-radius: 5px;
                                                    margin-right: 10px;
                                                    cursor: pointer;
                                                ">Preview</button>
                                            </div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    col1, col2 = st.columns([1, 1])
                                    with col1:
                                        with open(path, "rb") as f:
                                            st.download_button(
                                                "📥 Download Report",
                                                f,
                                                file_name=file,
                                                use_container_width=True
                                            )
                                    with col2:
                                        if st.button("🗑️ Delete", key=f"del_{file}", use_container_width=True):
                                            os.remove(path)
                                            st.warning(f"Deleted: {file}")
                                            show_medicine_drop()
                                            time.sleep(1)
                                            st.rerun()
                        else:
                            st.info("📭 No medical reports available for this date.")
                    else:
                        st.info("📁 No reports folder found for this date.")
                
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
                            st.markdown('<h3 class="medical-header">📋 Your Medical Reports</h3>', unsafe_allow_html=True)
                            
                            # Display files in medical cards
                            for file in allowed_files:
                                with st.container():
                                    path = os.path.join(folder_path, file)
                                    with open(path, "rb") as f:
                                        file_bytes = f.read()
                                    
                                    st.markdown(f"""
                                    <div class="medical-card">
                                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                            <span style="font-size: 24px; margin-right: 15px;">💊</span>
                                            <div>
                                                <h4 style="margin: 0; color: white;">{file}</h4>
                                                <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 0.9rem;">
                                                    📅 {selected_day} | 👤 {st.session_state.username}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    if st.download_button(
                                        "📥 Download Medical Report",
                                        data=file_bytes,
                                        file_name=file,
                                        use_container_width=True,
                                        key=f"dl_{file}"
                                    ):
                                        # Show animation when downloading
                                        show_medicine_drop()
                        else:
                            st.warning("📭 No medical reports available for your department.")
                    else:
                        st.warning("📁 No medical data available for this date.")
        else:
            st.info("📅 No medical reports available for current month.")
    
    # ----- FEEDBACK PAGE -----
    elif st.session_state.current_page == "feedback":
        st.markdown('<h3 class="medical-header">💬 Pharmaceutical Feedback</h3>', unsafe_allow_html=True)
        
        if st.session_state.user_role == "Admin":
            df = load_feedback()
            if not df.empty:
                st.markdown(f"### 📋 Total Feedback Records: {len(df)}")
                
                # Display feedback in medical cards
                for idx, row in df.sort_values("datetime", ascending=False).iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class="medical-card">
                            <div style="display: flex; align-items: start;">
                                <span style="font-size: 24px; margin-right: 15px;">👤</span>
                                <div style="flex: 1;">
                                    <div style="display: flex; justify-content: space-between;">
                                        <strong style="color: #26d0ce;">{row['username']}</strong>
                                        <small style="opacity: 0.7;">{row['datetime']}</small>
                                    </div>
                                    <p style="margin-top: 10px; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px;">
                                        {row['comment']}
                                    </p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("📭 No feedback records yet.")
        else:
            # Medical feedback form
            with st.form("medical_feedback", clear_on_submit=True):
                st.markdown("### 📝 Medical Feedback Form")
                
                feedback_type = st.selectbox(
                    "Type of Feedback:",
                    ["Medication Report", "System Issue", "Data Accuracy", "Feature Request", "Other"]
                )
                
                comment = st.text_area(
                    "Details:",
                    placeholder="Describe your feedback regarding pharmaceutical data...",
                    height=150
                )
                
                if st.form_submit_button("💊 Submit Medical Feedback", use_container_width=True):
                    if comment.strip():
                        full_comment = f"[{feedback_type}] {comment}"
                        add_feedback(st.session_state.username, full_comment)
                        st.success("✅ Thank you for your medical feedback! 🩺")
                        show_prescription_animation()
                        time.sleep(2)
                        st.session_state.current_page = "dashboard"
                        st.rerun()
                    else:
                        st.warning("⚠️ Please provide feedback details.")
    
    # ----- ABOUT PAGE -----
    elif st.session_state.current_page == "about":
    st.markdown('<h3 class="medical-header">🩺 Pharmaceutical Dashboard</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #1a2980; font-size: 2.5rem; margin-bottom: 10px;">KANDAA</h1>
        <h2 style="color: #26d0ce; font-size: 1.8rem; margin-bottom: 20px;">Pharmaceutical Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="medical-card">
        <h4 style="color: #26d0ce; margin-bottom: 15px;">🩺 About This System</h4>
        <p>Advanced pharmaceutical sales management system designed for medical teams to streamline operations and improve patient care.</p>
        
        <h5 style="color: #26d0ce; margin-top: 20px;">🏥 Medical Departments</h5>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 15px 0;">
            <div><span style="color: #FF5252;">•</span> CNS - Neuroscience</div>
            <div><span style="color: #FF5252;">•</span> GIT - Gastroenterology</div>
            <div><span style="color: #FF5252;">•</span> CVM - Cardiology</div>
            <div><span style="color: #FF5252;">•</span> Orthopedics</div>
            <div><span style="color: #FF5252;">•</span> Primary Care</div>
            <div><span style="color: #FF5252;">•</span> Special Teams</div>
        </div>
        
        <h5 style="color: #26d0ce; margin-top: 20px;">✨ Medical Features</h5>
        <p>✅ Secure pharmaceutical data access</p>
        <p>✅ Medical report management</p>
        <p>✅ Department-specific views</p>
        <p>✅ HIPAA-compliant design</p>
        <p>✅ Medical feedback system</p>
        
        <div style="margin-top: 25px; padding: 15px; background: rgba(38, 208, 206, 0.1); border-radius: 10px;">
            <div style="text-align: center;">
                <h5 style="color: #1a2980; margin-bottom: 10px;">Commercial Excellence Team</h5>
                <div style="font-size: 40px; margin-bottom: 10px;">💊 🩺 🌡️</div>
                <p style="margin: 0; font-size: 1.1rem;">
                    <strong>Improving Healthcare Through Data Excellence</strong>
                </p>
                <p style="margin: 5px 0 0 0; opacity: 0.8;">Version 2.0 • Medical Edition</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# Medical Footer
# ----------------------------
if st.session_state.logged_in:
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem; padding: 15px;">
        <p>💊 Pharmaceutical Dashboard v2.0 • Medical Data System • © 2024</p>
        <p style="font-size: 0.8rem; opacity: 0.5; margin-top: 5px;">
            🩺 Secure • Compliant • Reliable
        </p>
    </div>
    """, unsafe_allow_html=True)