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
    @keyframes pillFall {{
        0% {{ transform: translateY(-100px) rotate(0deg); opacity: 0; }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 1; }}
        100% {{ transform: translateY(100vh) rotate(360deg); opacity: 0; }}
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

    @keyframes capsuleBounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-20px); }}
    }}

    @keyframes welcomeSlide {{
        0% {{ transform: translateX(-100%); opacity: 0; }}
        100% {{ transform: translateX(0); opacity: 1; }}
    }}

    @keyframes medicalFloat {{
        0% {{ transform: translateY(0) rotate(0deg); }}
        25% {{ transform: translateY(-20px) rotate(90deg); }}
        50% {{ transform: translateY(-40px) rotate(180deg); }}
        75% {{ transform: translateY(-20px) rotate(270deg); }}
        100% {{ transform: translateY(0) rotate(360deg); }}
    }}

    .heartbeat {{ animation: heartbeat 1.5s infinite; }}
    .dna-spin {{ animation: dnaSpin 10s linear infinite; }}
    .capsule {{ animation: capsuleBounce 2s ease-in-out infinite; }}
    .welcome-slide {{ animation: welcomeSlide 1s ease-out; }}
    .medical-float {{ animation: medicalFloat 4s ease-in-out infinite; }}

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
def show_medicine_fall_animation():
    """Show medicine falling animation from top to bottom"""
    medicine_html = """
    <div id="medicineContainer" style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:9998;"></div>
    <script>
    function createMedicine() {
        const container = document.getElementById('medicineContainer');
        const medicine = document.createElement('div');
        
        // أنواع الأدوية والبرشام
        const medicines = [
            {emoji: '💊', color: '#FF5252', size: 25},  // حبة حمراء
            {emoji: '💊', color: '#448AFF', size: 30},  // حبة زرقاء
            {emoji: '💊', color: '#00C853', size: 20},  // حبة خضراء
            {emoji: '💉', color: '#FF4081', size: 35},  // حقنة
            {emoji: '🧪', color: '#E040FB', size: 40},  // أنبوبة اختبار
            {emoji: '🩺', color: '#536DFE', size: 45},  // سماعة طبية
            {emoji: '🌡️', color: '#FF9800', size: 30},  // ترمومتر
            {emoji: '💊', color: '#009688', size: 25},  // حبة فيروزي
            {emoji: '💊', color: '#FFD600', size: 28},  // حبة صفراء
            {emoji: '💊', color: '#9C27B0', size: 32}   // حبة بنفسجية
        ];
        
        const med = medicines[Math.floor(Math.random() * medicines.length)];
        
        medicine.innerHTML = med.emoji;
        medicine.style.position = 'absolute';
        medicine.style.left = Math.random() * 100 + 'vw';
        medicine.style.fontSize = med.size + 'px';
        medicine.style.color = med.color;
        medicine.style.opacity = '0.9';
        medicine.style.textShadow = '0 2px 10px rgba(0,0,0,0.3)';
        medicine.style.zIndex = '9999';
        
        // سرعة سقوط مختلفة لكل دواء
        const duration = Math.random() * 3 + 2;
        const delay = Math.random() * 2;
        
        medicine.style.animation = `
            pillFall ${duration}s ease-in ${delay}s forwards,
            medicalFloat ${duration * 0.5}s ease-in-out ${delay}s infinite
        `;
        
        container.appendChild(medicine);
        setTimeout(() => medicine.remove(), (duration + delay) * 1000);
    }
    
    // إنشاء كمية كبيرة من الأدوية
    for(let i = 0; i < 50; i++) {
        setTimeout(() => createMedicine(), i * 100);
    }
    
    // CSS للـ animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pillFall {
            0% { 
                transform: translateY(-100px) rotate(0deg); 
                opacity: 0; 
            }
            10% { 
                opacity: 1; 
            }
            90% { 
                opacity: 1; 
            }
            100% { 
                transform: translateY(100vh) rotate(360deg); 
                opacity: 0; 
            }
        }
        
        @keyframes medicalFloat {
            0%, 100% { transform: translateX(0); }
            50% { transform: translateX(20px); }
        }
    `;
    document.head.appendChild(style);
    </script>
    """
    st.components.v1.html(medicine_html, height=0)

def show_prescription_animation():
    """Show prescription writing animation"""
    prescription_html = """
    <div style="
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #ffffff, #f5f5f5);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: writePrescription 3s ease-in-out forwards;
        max-width: 400px;
        border: 3px solid #26d0ce;
    ">
        <div style="text-align: center;">
            <div style="font-size: 50px; margin-bottom: 15px; color: #26d0ce;">📝</div>
            <h3 style="color: #1a2980; margin: 0; font-family: 'Arial', sans-serif;">Medical Access Granted!</h3>
            <div style="
                width: 80px;
                height: 4px;
                background: linear-gradient(90deg, #1a2980, #26d0ce);
                margin: 15px auto;
                border-radius: 2px;
            "></div>
            <p style="color: #666; margin-top: 10px; font-size: 14px;">
                Pharmaceutical Dashboard Ready
            </p>
            <div style="margin-top: 20px; font-size: 24px;">
                <span style="color: #FF5252;">💊</span>
                <span style="color: #448AFF; margin: 0 10px;">🩺</span>
                <span style="color: #00C853;">🌡️</span>
            </div>
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

def show_heartbeat_loader(text="Accessing Medical Database..."):
    """Show heartbeat loading animation"""
    heartbeat_html = f"""
    <div style="text-align: center; padding: 40px;">
        <div style="
            display: inline-block;
            animation: heartbeat 1.5s infinite;
            font-size: 70px;
            margin-bottom: 20px;
            color: #FF5252;
        ">
            ❤️
        </div>
        <p style="color: white; font-weight: bold; font-size: 20px; margin-bottom: 20px;">{text}</p>
        <div style="
            width: 300px;
            height: 6px;
            background: rgba(255,255,255,0.2);
            border-radius: 3px;
            margin: 0 auto;
            overflow: hidden;
        ">
            <div style="
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, #FF5252, #FF4081, #E040FB);
                animation: loadingBar 2s ease-in-out infinite;
                border-radius: 3px;
            "></div>
        </div>
        <div style="margin-top: 20px; font-size: 24px; opacity: 0.8;">
            <span style="animation-delay: 0s;">💊</span>
            <span style="animation-delay: 0.2s; margin: 0 10px;">💉</span>
            <span style="animation-delay: 0.4s;">🧪</span>
        </div>
        <style>
        @keyframes loadingBar {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        </style>
    </div>
    """
    return heartbeat_html

# ----------------------------
# Login + Dashboard UI Style
# ----------------------------
st.markdown("""
<style>
/* Medical Theme Welcome Message */
.welcome-medical {
    background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%) !important;
    padding: 25px !important;
    border-radius: 20px !important;
    text-align: center !important;
    margin: 0 auto 30px auto !important;
    color: white !important;
    font-size: 1.4rem !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.3) !important;
    border: 3px solid rgba(255,255,255,0.4) !important;
    backdrop-filter: blur(15px) !important;
    max-width: 650px !important;
    position: relative;
    overflow: hidden;
    z-index: 100;
}

.welcome-medical::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 20px 20px;
    animation: backgroundMove 20s linear infinite;
    z-index: -1;
}

@keyframes backgroundMove {
    0% { transform: translate(0, 0) rotate(0deg); }
    100% { transform: translate(100px, 100px) rotate(360deg); }
}

.welcome-medical h3 {
    color: white !important;
    margin-bottom: 10px !important;
    font-size: 2rem !important;
    position: relative;
    z-index: 2;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.welcome-medical p {
    color: rgba(255,255,255,0.95) !important;
    margin-top: 10px !important;
    font-size: 1.1rem !important;
    position: relative;
    z-index: 2;
}

/* Medical Cards */
.medical-card {
    background: rgba(255, 255, 255, 0.15) !important;
    padding: 25px !important;
    border-radius: 20px !important;
    border-left: 8px solid #26d0ce !important;
    margin-bottom: 20px !important;
    backdrop-filter: blur(15px) !important;
    transition: all 0.4s ease !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2) !important;
}

.medical-card:hover {
    transform: translateY(-8px) scale(1.02) !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3) !important;
    border-left: 8px solid #FF5252 !important;
}

/* Medical Buttons */
.stButton > button {
    width: 100%;
    border-radius: 15px !important;
    height: 55px;
    font-size: 18px !important;
    background: linear-gradient(90deg, #1a2980, #26d0ce) !important;
    color: white !important;
    border: none !important;
    transition: all 0.3s ease !important;
    font-weight: bold !important;
    box-shadow: 0 5px 15px rgba(26, 41, 128, 0.4) !important;
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #0d1a66, #1cb5b3) !important;
    transform: scale(1.05) translateY(-3px) !important;
    box-shadow: 0 10px 25px rgba(26, 41, 128, 0.6) !important;
}

.stButton > button::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        to right,
        rgba(255,255,255,0) 0%,
        rgba(255,255,255,0.3) 50%,
        rgba(255,255,255,0) 100%
    );
    transform: rotate(30deg);
    transition: all 0.6s ease;
}

.stButton > button:hover::after {
    left: 100%;
}

/* LOGIN BOX - Medical Theme */
.login-medical-box {
    background: rgba(255, 255, 255, 0.15) !important;
    width: 450px;
    max-width: 90%;
    padding: 50px 40px;
    border-radius: 25px;
    text-align: center;
    margin: 80px auto 0 auto;
    backdrop-filter: blur(20px) !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    box-shadow: 0 25px 50px rgba(0,0,0,0.3) !important;
    animation: welcomeSlide 1s ease-out !important;
    position: relative;
    overflow: hidden;
}

.login-medical-box::before {
    content: "💊 🩺 💉";
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 50px;
    opacity: 0.2;
    z-index: 0;
}

.login-medical-box::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #FF5252, #FF4081, #E040FB, #7C4DFF);
    animation: gradientMove 3s ease infinite;
    background-size: 400% 100%;
}

@keyframes gradientMove {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* INPUT FIELDS */
.stTextInput > div > div > input {
    text-align: left;
    font-size: 18px !important;
    padding: 15px !important;
    color: #1a2980 !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.95) !important;
    border: 2px solid #26d0ce !important;
    transition: all 0.3s ease !important;
    margin-bottom: 20px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #FF5252 !important;
    box-shadow: 0 0 0 3px rgba(255, 82, 82, 0.2) !important;
    transform: scale(1.02) !important;
}

/* LABELS */
.stTextInput > label,
.stTextInput > div > label {
    color: white !important;
    font-weight: bold !important;
    font-size: 16px !important;
    margin-bottom: 8px !important;
    display: block !important;
}

/* HEADERS */
.medical-header {
    background: linear-gradient(90deg, #FF5252, #FF4081, #E040FB) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    padding: 15px 0 !important;
    border-bottom: 3px solid #26d0ce !important;
    display: inline-block !important;
    margin-bottom: 25px !important;
    font-size: 2rem !important;
    font-weight: bold !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
}

/* DOWNLOAD BUTTON */
.stDownloadButton > button {
    background: linear-gradient(90deg, #00C853, #64DD17) !important;
    color: white !important;
    border-radius: 12px !important;
    height: 50px;
    font-size: 16px !important;
    border: none !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 5px 15px rgba(0, 200, 83, 0.4) !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #00B248, #4CAF50) !important;
    transform: scale(1.05) !important;
    box-shadow: 0 10px 25px rgba(0, 200, 83, 0.6) !important;
}

/* SUCCESS MESSAGES */
.stSuccess {
    background: linear-gradient(135deg, #00b09b, #96c93d) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
    animation: heartbeat 2s infinite !important;
    border-left: 5px solid white !important;
    box-shadow: 0 10px 20px rgba(0, 176, 155, 0.3) !important;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #1a2980, #26d0ce);
    border-radius: 10px;
    border: 3px solid rgba(255,255,255,0.1);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #0d1a66, #1cb5b3);
}

@media only screen and (max-width: 768px) {
    .login-medical-box {
        width: 90%;
        padding: 30px 20px;
        margin-top: 60px;
    }
    
    .welcome-medical {
        padding: 20px !important;
        margin: 0 15px 25px 15px !important;
        font-size: 1.2rem !important;
    }
    
    .welcome-medical h3 {
        font-size: 1.6rem !important;
    }
    
    .medical-header {
        font-size: 1.5rem !important;
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

if "medicine_animation_shown" not in st.session_state:
    st.session_state.medicine_animation_shown = False

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
    st.session_state.medicine_animation_shown = False

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
            "Primary": {"emoji": "👨‍⚕️", "message": "General Medicine"},
            "CVM": {"emoji": "❤️", "message": "Cardiology Division"},
            "Power": {"emoji": "⚡", "message": "Special Operations"},
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
                <div style="margin-top: 20px; font-size: 30px; opacity: 0.9;">
                    <span class="heartbeat">❤️</span>
                    <span class="capsule" style="margin: 0 15px; animation-delay: 0.3s;">💊</span>
                    <span class="heartbeat" style="animation-delay: 0.6s;">🩺</span>
                </div>
                <div style="margin-top: 15px; font-size: 0.9rem; opacity: 0.8;">
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
            <div style="font-size: 40px; color: #26d0ce; margin-bottom: 15px; text-align: center;">💊</div>
            <h4 style="margin: 0; color: white; text-align: center;">Today's Reports</h4>
            <p style="font-size: 2rem; margin: 15px 0; color: #26d0ce; text-align: center;">{date.today().strftime('%d %b')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="medical-card">
            <div style="font-size: 40px; color: #FF5252; margin-bottom: 15px; text-align: center;">🩺</div>
            <h4 style="margin: 0; color: white; text-align: center;">Department</h4>
            <p style="font-size: 1.8rem; margin: 15px 0; color: #FF5252; text-align: center;">{st.session_state.username}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status_emoji = "✅" if st.session_state.logged_in else "❌"
        st.markdown(f"""
        <div class="medical-card">
            <div style="font-size: 40px; color: #00C853; margin-bottom: 15px; text-align: center;">🌡️</div>
            <h4 style="margin: 0; color: white; text-align: center;">System Status</h4>
            <p style="font-size: 2rem; margin: 15px 0; color: #00C853; text-align: center;">Active {status_emoji}</p>
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
    <div style="text-align: center; margin-bottom: 40px;">
        <div style="font-size: 60px; margin-bottom: 15px;">💊 🩺 💉</div>
        <h2 style="color: white; margin-bottom: 10px; font-size: 2.2rem;">Pharmaceutical Access</h2>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">Medical Dashboard Login</p>
        <div style="
            width: 100px;
            height: 4px;
            background: linear-gradient(90deg, #FF5252, #26d0ce);
            margin: 20px auto;
            border-radius: 2px;
        "></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input fields with medical icons
    u = st.text_input("", placeholder="👤 Medical ID / Username", key="username_input")
    p = st.text_input("", type="password", placeholder="🔒 Secure Password", key="password_input")
    
    # Medical-themed login button
    if st.button("💉 Access Medical Dashboard", use_container_width=True):
        if u and p:
            if login(u, p):
                # Show medicine falling animation
                show_medicine_fall_animation()
                
                # Show loading animation
                loading_placeholder = st.empty()
                loading_placeholder.markdown(show_heartbeat_loader(f"Welcome {u} Medical Team!"), unsafe_allow_html=True)
                
                time.sleep(2)
                
                # Show prescription animation
                show_prescription_animation()
                
                # Clear loading
                loading_placeholder.empty()
                
                # Mark animation as shown
                st.session_state.medicine_animation_shown = True
                
                # Small delay before redirect
                time.sleep(1.5)
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
                                
                                # Show medicine animation on successful upload
                                show_medicine_fall_animation()
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
                                            <div style="display: flex; align-items: center;">
                                                <span style="font-size: 30px; margin-right: 15px; color: #26d0ce;">📄</span>
                                                <div>
                                                    <strong style="color: white; font-size: 1.2rem;">{file}</strong>
                                                    <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 0.9rem;">
                                                        Medical Report • {selected_day}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    col1, col2 = st.columns([1, 1])
                                    with col1:
                                        with open(path, "rb") as f:
                                            if st.download_button(
                                                "📥 Download Report",
                                                f,
                                                file_name=file,
                                                use_container_width=True,
                                                key=f"download_{file}"
                                            ):
                                                show_medicine_fall_animation()
                                    with col2:
                                        if st.button("🗑️ Delete", key=f"del_{file}", use_container_width=True):
                                            os.remove(path)
                                            st.warning(f"Deleted: {file}")
                                            show_medicine_fall_animation()
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
                                        <div style="display: flex; align-items: center; margin-bottom: 20px;">
                                            <span style="font-size: 40px; margin-right: 20px; color: #FF5252;">💊</span>
                                            <div style="flex: 1;">
                                                <h4 style="margin: 0; color: white;">{file}</h4>
                                                <p style="margin: 10px 0 0 0; opacity: 0.8; font-size: 0.9rem;">
                                                    📅 {selected_day} | 👤 {st.session_state.username}
                                                </p>
                                            </div>
                                        </div>
                                        <div style="
                                            width: 100%;
                                            height: 3px;
                                            background: linear-gradient(90deg, #FF5252, #26d0ce);
                                            margin: 15px 0;
                                            border-radius: 2px;
                                        "></div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    if st.download_button(
                                        "📥 Download Medical Report",
                                        data=file_bytes,
                                        file_name=file,
                                        use_container_width=True,
                                        key=f"user_dl_{file}"
                                    ):
                                        # Show animation when downloading
                                        show_medicine_fall_animation()
                                        time.sleep(0.5)
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
                                <span style="font-size: 30px; margin-right: 20px; color: #26d0ce;">👤</span>
                                <div style="flex: 1;">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <strong style="color: white; font-size: 1.2rem;">{row['username']}</strong>
                                        <small style="opacity: 0.7; background: rgba(255,255,255,0.1); padding: 5px 10px; border-radius: 5px;">
                                            {row['datetime']}
                                        </small>
                                    </div>
                                    <div style="
                                        background: rgba(255,255,255,0.05); 
                                        padding: 15px; 
                                        border-radius: 10px;
                                        margin-top: 15px;
                                        border-left: 4px solid #FF5252;
                                    ">
                                        <p style="margin: 0; color: rgba(255,255,255,0.9);">{row['comment']}</p>
                                    </div>
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
                        show_medicine_fall_animation()
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