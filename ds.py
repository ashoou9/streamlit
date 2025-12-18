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
st.set_page_config(
    page_title="Mash Premiere",
    page_icon="💊"
    
)
# ----------------------------
# أولاً: إنشاء المجلدات والملفات المطلوبة للويندوز الجديد
# هذه الزيادة الوحيدة اللي هنضيفها في الأول
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
# Hide Warnings and Logs
# ----------------------------
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)
os.environ["PYTHONWARNINGS"] = "ignore"

# ----------------------------
# JavaScript لإصلاح مشكلة الـ Zoom
# ----------------------------
st.markdown("""
<script>
// منع الـ Zoom الغير مرغوب فيه
document.addEventListener('DOMContentLoaded', function() {
    // منع zoom بالـ keyboard (Ctrl + +, Ctrl + -)
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey === true || e.metaKey === true) && 
            (e.keyCode === 61 || e.keyCode === 107 || e.keyCode === 173 || 
             e.keyCode === 109 || e.keyCode === 187 || e.keyCode === 189)) {
            e.preventDefault();
        }
    });
    
    // منع zoom بالـ mouse wheel + Ctrl
    document.addEventListener('wheel', function(e) {
        if(e.ctrlKey) {
            e.preventDefault();
        }
    }, { passive: false });
    
    // إجبار viewport scale على 1
    const metaViewport = document.querySelector('meta[name="viewport"]');
    if (metaViewport) {
        metaViewport.content = "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no";
    }
});
</script>

<style>
/* إصلاح عام للـ Zoom */
* {
    -webkit-text-size-adjust: 100% !important;
    -moz-text-size-adjust: 100% !important;
    -ms-text-size-adjust: 100% !important;
    text-size-adjust: 100% !important;
}

/* ============================================= */
/* REDUCED WIDTH LAYOUT - تقليل عرض الصفحة */
/* ============================================= */

/* زيادة الـ padding من الجوانب لتقليل العرض */
.block-container {
    padding-top: 1rem !important;
    padding-left: 6rem !important;      /* زود من 2rem لـ 6rem */
    padding-right: 6rem !important;     /* زود من 2rem لـ 6rem */
    padding-bottom: 100px !important;
    max-width: 100% !important;
    width: 100% !important;
    overflow-x: hidden !important;
}

/* تحسين الـ Responsive للعناصر */
@media (max-width: 1400px) {
    .block-container {
        padding-left: 5rem !important;    /* زود من 2 لـ 5 */
        padding-right: 5rem !important;   /* زود من 2 لـ 5 */
    }
}

@media (max-width: 1200px) {
    .block-container {
        padding-left: 4rem !important;    /* زود من 2 لـ 4 */
        padding-right: 4rem !important;   /* زود من 2 لـ 4 */
    }
}

@media (max-width: 992px) {
    .block-container {
        padding-left: 3rem !important;    /* زود من 1.5 لـ 3 */
        padding-right: 3rem !important;   /* زود من 1.5 لـ 3 */
    }
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 2rem !important;    /* زود من 1 لـ 2 */
        padding-right: 2rem !important;   /* زود من 1 لـ 2 */
    }
}

@media (max-width: 576px) {
    .block-container {
        padding-left: 1.5rem !important;  /* زود من 0.5 لـ 1.5 */
        padding-right: 1.5rem !important; /* زود من 0.5 لـ 1.5 */
    }
}

/* تحسين الأزرار للـ Zoom */
.stButton > button {
    min-width: 0px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

/* تحسين الـ Welcome Message للـ Zoom */
.welcome-fixed {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}

/* تحسين النصوص للـ Zoom */
h1, h2, h3, h4, h5, h6, p, span, div {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Page Background - مع تعديل بسيط للتعامل مع الويندوز الجديد
# ----------------------------
def set_bg_local(image_file, login_page=True):
    try:
        with open(image_file, "rb") as f:
            img_bytes = f.read()
        b64 = base64.b64encode(img_bytes).decode()
    except FileNotFoundError:
        # إذا الصورة مش موجودة، استخدم خلفية لونية بدون ما تكسر التصميم
        b64 = ""
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        return

    # تخفيض الـ padding-top لرفع المحتوى لأعلى
    padding_top = "20px" if login_page else "60px"  # قللت من 105 و 180

    page_bg_img = f"""
    <style>
    html, body {{
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }}

    /* ثبات تام للخلفية */
    .stApp {{
        background: url("data:image/png;base64,{b64}") no-repeat center top !important;
        background-size: cover !important;
        background-attachment: fixed !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        min-height: 100vh !important;
    }}

    /* تأمين الخلفية من التحرك */
    [data-testid="stAppViewContainer"] {{
        padding-top: {padding_top} !important;
        margin: 0 !important;
        overflow-x: hidden !important;
        background: transparent !important;
        position: relative !important;
    }}

    .block-container {{
        padding-top: 1rem !important;
        padding-left: 6rem !important;      /* زود من 2rem لـ 6rem */
        padding-right: 6rem !important;     /* زود من 2rem لـ 6rem */
        padding-bottom: 100px !important;
        max-width: 100% !important;
        width: 100% !important;
        overflow-x: hidden !important;
        background: transparent !important;
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

    @media only screen and (max-width: 768px) {{
        [data-testid="stAppViewContainer"] {{
            padding-top: 120px !important;  /* قللت من 140px */
        }}
        .block-container {{
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }}
    }}
    
    /* توسيع الأعمدة والصفوف */
    .stColumn {{
        padding: 0 5px !important;
    }}
    
    [data-testid="column"] {{
        padding: 0 5px !important;
    }}
    
    .row-widget {{
        width: 100% !important;
    }}
    
    /* توسيع العناصر الداخلية */
    div[data-testid="stHorizontalBlock"] {{
        width: 100% !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }}
    
    /* توسيع الـ Cards */
    .custom-card {{
        width: 100% !important;
        margin: 0 0 15px 0 !important;
    }}
    
    /* تقليل Welcome Message */
    .welcome-fixed {{
        width: 80% !important;               /* قل من 100% لـ 80% */
        max-width: 80% !important;           /* قل من 100% لـ 80% */
        margin: 0 auto 25px auto !important; /* مركز */
    }}
    
    /* توسيع الـ Forms */
    .stForm {{
        width: 100% !important;
    }}
    
    /* رفع حاوية الأزرار للأعلى */
    .nav-buttons-container {{
        margin-top: -10px !important;        /* رفع الأزرار لأعلى */
        margin-bottom: 20px !important;
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
# Login + Dashboard UI Style - FIXED مع تقليل العرض
# ----------------------------
st.markdown("""
<style>
/* Welcome Message - Fixed in Dashboard - REDUCED */
.welcome-fixed {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    padding: 18px !important;               /* قل من 20px لـ 18px */
    border-radius: 15px !important;
    text-align: center !important;
    margin: 0 auto 25px auto !important;    /* مركز */
    color: white !important;
    font-size: 1.2rem !important;           /* قل من 1.3rem لـ 1.2rem */
    box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    backdrop-filter: blur(10px) !important;
    max-width: 80% !important;              /* قل من 100% لـ 80% */
    width: 80% !important;                  /* قل من 100% لـ 80% */
    box-sizing: border-box !important;
}

.welcome-fixed h3 {
    color: white !important;
    margin-bottom: 8px !important;
    font-size: 1.6rem !important;           /* قل من 1.8rem لـ 1.6rem */
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}

.welcome-fixed p {
    color: rgba(255,255,255,0.9) !important;
    margin-top: 8px !important;
    font-size: 0.95rem !important;          /* قل من 1rem لـ 0.95rem */
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}

/* Success Message with Animation */
.success-animated {
    background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important;
    padding: 15px !important;
    border-radius: 10px !important;
    border: none !important;
    animation: pulse 2s infinite !important;
}

/* Notification Card - FIXED - REDUCED */
.notification-card {
    background: rgba(255,255,255,0.15) !important;
    padding: 18px !important;               /* قل من 20px لـ 18px */
    border-radius: 15px !important;
    margin-bottom: 15px !important;
    border-left: 5px solid #FF9800 !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.notification-card:hover {
    background: rgba(255,255,255,0.2) !important;
    transform: translateY(-2px) !important;
}

.notification-card.read {
    border-left: 5px solid #4CAF50 !important;
    opacity: 0.8;
}

/* Comment Display Box - FIXED - REDUCED */
.comment-box {
    background: rgba(0, 0, 0, 0.25) !important;
    padding: 14px !important;               /* قل من 15px لـ 14px */
    border-radius: 10px !important;
    margin: 10px 0 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    line-height: 1.6 !important;
    font-size: 0.9rem !important;           /* قل من 0.95rem لـ 0.9rem */
    max-height: 300px !important;
    overflow-y: auto !important;
    color: rgba(255, 255, 255, 0.95) !important;
    width: 100% !important;
}

.comment-box p {
    margin: 0 !important;
    color: rgba(255, 255, 255, 0.95) !important;
}

/* INPUT BOXES - REDUCED */
.stTextInput > div > div > input {
    text-align: left;
    font-size: 15px !important;             /* قل من 16px لـ 15px */
    padding: 9px !important;                /* قل من 10px لـ 9px */
    color: black !important;
    border-radius: 8px;
    background: rgba(255,255,255,0.9) !important;
    box-sizing: border-box !important;
    width: 100% !important;
}

/* ALL LABELS */
label[data-baseweb="label"],
.stSelectbox label,
.stFileUploader label,
.stTextInput label,
.stDateInput label {
    color: white !important;
    font-weight: bold !important;
    font-size: 0.95rem !important;          /* قل شوية */
}

/* SUBHEADERS & TEXT - REDUCED */
h1, h2, h3, h4, h5, h6,
.stSubheader,
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stText"] {
    color: white !important;
    font-weight: bold !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    width: 100% !important;
}

/* PLACEHOLDER */
input::placeholder {
    color: rgba(0,0,0,0.6) !important;
}

/* ----- LOGIN BOX أصغر بالكامل ----- */
.login-box {
    background: rgba(255, 255, 255, 0.1) !important;
    width: 75% !important;                  /* قلل من 90% لـ 75% */
    max-width: 350px !important;            /* قلل من 450px لـ 350px */
    padding: 20px !important;               /* قلل من 30px لـ 20px */
    border-radius: 12px !important;         /* قلل الزوايا شوية */
    text-align: center;
    margin: 20px auto 0 auto !important;    /* رفع لأعلى أكثر */
    backdrop-filter: blur(8px) !important;  /* قلل blur */
    border: 1px solid rgba(255,255,255,0.2) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
    animation: fadeInUp 0.8s ease-out !important;
    box-sizing: border-box !important;
}

/* العنوان داخل الـ box */
.login-box h2 {
    color: white !important;
    margin-bottom: 5px !important;
    font-size: 1.4rem !important;           /* أصغر */
}

.login-box p {
    color: rgba(255,255,255,0.8) !important;
    margin-bottom: 15px !important;
    font-size: 0.85rem !important;          /* أصغر */
}

/* الحقول نفسها - أصغر */
.stApp .login-box .stTextInput > div > div > input {
    font-size: 14px !important;
    padding: 7px 10px !important;           /* أصغر padding */
    height: 38px !important;                /* ارتفاع أقل */
    border-radius: 6px !important;          /* زوايا أقل */
    margin: 0 auto 10px auto !important;    /* مسافة بين الحقول أقل */
    width: 90% !important;                  /* عرض أقل داخل الـ box */
    max-width: 280px !important;
    display: block !important;
}

/* زر الـ Login - أصغر */
.stApp .login-box .stButton > button {
    width: 90% !important;                  /* عرض أقل */
    max-width: 280px !important;
    height: 36px !important;                /* ارتفاع أقل */
    font-size: 13px !important;             /* خط أصغر */
    border-radius: 6px !important;          /* زوايا أقل */
    margin: 5px auto 0 auto !important;
    background: linear-gradient(90deg, #0072ff, #00c6ff) !important;
    transition: all 0.2s ease !important;
    display: block !important;
}

.stApp .login-box .stButton > button:hover {
    transform: scale(1.02) !important;
}

/* للموبايل - تكييف أكثر */
@media (max-width: 768px) {
    .login-box {
        width: 85% !important;
        max-width: 300px !important;
        padding: 18px !important;
        margin: 15px auto 0 auto !important;
    }
    
    .login-box h2 {
        font-size: 1.3rem !important;
    }
    
    .stApp .login-box .stTextInput > div > div > input {
        font-size: 13px !important;
        padding: 6px 8px !important;
        height: 36px !important;
    }
    
    .stApp .login-box .stButton > button {
        height: 34px !important;
        font-size: 12px !important;
    }
}

/* ============================================= */
/* NAVIGATION BUTTONS - أزرار التنقل المعدلة */
/* ============================================= */

/* حاوية الأزرار الرئيسية - مرفوعة لأعلى */
.nav-buttons-container {
    display: flex !important;
    gap: 10px !important;
    margin: 5px 0 20px 0 !important;        /* رفع الأزرار لأعلى */
    width: 100% !important;
    justify-content: space-between !important;
    flex-wrap: nowrap !important;
    padding-top: 0 !important;
}

/* الأزرار نفسها */
.nav-button {
    flex: 1 !important;
    min-width: 0 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

/* تنسيق الأزرار داخل الـ columns */
.nav-buttons-container .stButton > button {
    width: 100% !important;
    border-radius: 10px !important;
    height: 42px !important;                /* قل من 45px لـ 42px */
    font-size: 1px !important;             /* قل من 14px لـ 13px */
    background: linear-gradient(90deg, #0072ff, #00c6ff) !important;
    color: white !important;
    border: none !important;
    transition: all 0.3s ease !important;
    box-sizing: border-box !important;
    margin: 0 !important;
    padding: 0 8px !important;              /* قل من 10px لـ 8px */
}

.nav-buttons-container .stButton > button:hover {
    background: linear-gradient(90deg, #0051cc, #0099cc) !important;
    transform: scale(1.02) !important;
    box-shadow: 0 5px 15px rgba(0,114,255,0.4) !important;
}

/* زر الـ Logout بلون مختلف */
.nav-buttons-container .stButton > button[kind="secondary"] {
    background: linear-gradient(90deg, #ff416c, #ff4b2b) !important;
}

.nav-buttons-container .stButton > button[kind="secondary"]:hover {
    background: linear-gradient(90deg, #e03e5a, #e63c1f) !important;
}

/* زر Notifications مع badge */
.notification-button {
    position: relative !important;
}

/* BUTTONS - REDUCED */
.stButton > button {
    width: 100% !important;
    border-radius: 10px;
    height: 42px !important;                /* قل من 45px لـ 42px */
    font-size: 15px !important;             /* قل من 16px لـ 15px */
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white;
    border: none;
    transition: all 0.3s ease !important;
    box-sizing: border-box !important;
    min-width: 0 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
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

/* DOWNLOAD BUTTON - REDUCED */
.stDownloadButton button {
    color: white !important;
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    border-radius: 10px;
    height: 42px !important;                /* قل من 45px لـ 42px */
    font-size: 15px !important;             /* قل من 16px لـ 15px */
    transition: all 0.3s ease !important;
    min-width: 0 !important;
    width: 100% !important;
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

/* CARD STYLING - REDUCED */
.custom-card {
    background: rgba(255, 255, 255, 0.1) !important;
    padding: 18px !important;               /* قل من 20px لـ 18px */
    border-radius: 15px !important;
    border-left: 5px solid #00c6ff !important;
    margin-bottom: 15px !important;
    backdrop-filter: blur(10px) !important;
    box-sizing: border-box !important;
    word-wrap: break-word !important;
    width: 100% !important;
    height: 110px !important;               /* قل من 120px لـ 110px */
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

.custom-card h4 {
    color: #00c6ff !important;
    margin: 0 0 8px 0 !important;           /* قل من 10px لـ 8px */
    font-size: 1rem !important;             /* قل من 1.1rem لـ 1rem */
}

.custom-card p {
    font-size: 1.4rem !important;           /* قل من 1.5rem لـ 1.4rem */
    margin: 0 !important;
    color: white !important;
    font-weight: bold !important;
}

/* REPLY CARD - REDUCED */
.reply-card {
    background: rgba(0, 198, 255, 0.1) !important;
    padding: 14px !important;               /* قل من 15px لـ 14px */
    border-radius: 10px !important;
    margin: 10px 0 15px 20px !important;
    border-left: 3px solid #00c6ff !important;
    width: 100% !important;
}

/* ABOUT PAGE STYLING - REDUCED */
.about-section {
    margin-bottom: 25px !important;
    width: 100% !important;
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

/* FIX for logout button */
.stButton > button[kind="secondary"] {
    min-width: 110px !important;            /* قل من 120px لـ 110px */
    width: auto !important;
    padding: 0 18px !important;             /* قل من 20px لـ 18px */
}

/* Feedback actions container */
.feedback-actions {
    display: flex;
    gap: 10px;
    margin-top: 10px;
    width: 100% !important;
}

/* Admin actions - REDUCED */
.admin-actions {
    display: flex !important;
    gap: 10px !important;
    margin-top: 15px !important;
    width: 100% !important;
}

/* NOTIFICATIONS STYLING - REDUCED */
.notification-item {
    background: white;
    border-radius: 10px;
    padding: 18px !important;               /* قل من 20px لـ 18px */
    margin: 10px 0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    box-sizing: border-box !important;
    width: 100% !important;
}

.notification-item.unread {
    border-left: 4px solid #3498db;
    background: #f0f8ff;
}

.notification-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    width: 100% !important;
}

.notification-title {
    font-weight: bold;
    color: #333;
    font-size: 15px !important;             /* قل من 16px لـ 15px */
    word-wrap: break-word !important;
}

.notification-time {
    color: #666;
    font-size: 13px !important;             /* قل من 14px لـ 13px */
}

.new-badge {
    background: #ff4444;
    color: white;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}

.notification-content-box {
    background: #f5f5f5;
    padding: 14px !important;               /* قل من 15px لـ 14px */
    border-radius: 8px;
    margin: 10px 0;
    color: #333;
    font-size: 14px !important;             /* قل من 15px لـ 14px */
    word-wrap: break-word !important;
    width: 100% !important;
}

/* ============================================= */
/* FULL WIDTH RESPONSIVE ADJUSTMENTS */
/* ============================================= */

/* توسيع الـ columns */
.stColumn, [data-testid="column"] {
    padding: 0 5px !important;
}

/* توسيع الـ horizontal blocks */
div[data-testid="stHorizontalBlock"] {
    width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    padding: 0 !important;
}

/* توسيع الـ select boxes */
.stSelectbox > div > div {
    width: 100% !important;
}

/* توسيع الـ file uploader */
.stFileUploader {
    width: 100% !important;
}

/* توسيع الـ text areas */
.stTextArea > div > div > textarea {
    width: 100% !important;
}

/* توسيع الـ forms */
.stForm {
    width: 100% !important;
}

/* ============================================= */
/* RESPONSIVE ADJUSTMENTS للعرض المخفّض */
/* ============================================= */

@media only screen and (max-width: 1400px) {
    .block-container {
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }
    
    .welcome-fixed {
        width: 85% !important;              /* قل من 100% لـ 85% */
        max-width: 85% !important;
    }
    
    .custom-card {
        height: 105px !important;           /* قل من 110px لـ 105px */
    }
    
    .nav-buttons-container .stButton > button {
        font-size: 12px !important;         /* قل من 13px لـ 12px */
        padding: 0 7px !important;          /* قل من 8px لـ 7px */
    }
}

@media only screen and (max-width: 1200px) {
    .block-container {
        padding-left: 4rem !important;
        padding-right: 4rem !important;
    }
    
    .welcome-fixed h3 {
        font-size: 1.5rem !important;       /* قل من 1.6rem لـ 1.5rem */
    }
    
    .custom-card {
        height: 95px !important;            /* قل من 100px لـ 95px */
        padding: 16px !important;           /* قل من 15px لـ 16px */
    }
    
    .custom-card p {
        font-size: 1.3rem !important;       /* قل من 1.4rem لـ 1.3rem */
    }
    
    .nav-buttons-container .stButton > button {
        font-size: 11px !important;         /* قل من 12px لـ 11px */
        height: 38px !important;            /* قل من 40px لـ 38px */
    }
}

@media only screen and (max-width: 992px) {
    .block-container {
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }
    
    .welcome-fixed {
        padding: 16px !important;           /* قل من 15px لـ 16px */
        font-size: 1.1rem !important;
    }
    
    .welcome-fixed h3 {
        font-size: 1.4rem !important;
    }
    
    .stButton > button {
        font-size: 14px !important;
        height: 38px !important;            /* قل من 40px لـ 38px */
    }
    
    .custom-card {
        height: 85px !important;            /* قل من 90px لـ 85px */
        padding: 14px !important;           /* قل من 12px لـ 14px */
    }
    
    .custom-card p {
        font-size: 1.2rem !important;       /* قل من 1.3rem لـ 1.2rem */
    }
    
    .nav-buttons-container {
        gap: 7px !important;                /* قل من 8px لـ 7px */
    }
    
    .nav-buttons-container .stButton > button {
        font-size: 10px !important;         /* قل من 11px لـ 10px */
        height: 36px !important;            /* قل من 38px لـ 36px */
        padding: 0 5px !important;          /* قل من 6px لـ 5px */
    }
}

@media only screen and (max-width: 768px) {
    .login-box {
        width: 90% !important;
        padding: 25px !important;
        margin-top: 40px !important;        /* رفع الـ login box */
    }
    
    .welcome-fixed {
        padding: 14px !important;           /* قل من 15px لـ 14px */
        margin: 0 auto 20px auto !important;
        font-size: 1.1rem !important;
    }
    
    .welcome-fixed h3 {
        font-size: 1.4rem !important;
    }
    
    .comment-box {
        padding: 12px !important;
        font-size: 0.85rem !important;      /* قل من 0.9rem لـ 0.85rem */
    }
    
    .admin-actions {
        flex-direction: column !important;
    }
    
    .stButton > button[kind="secondary"] {
        min-width: 100px !important;
        padding: 0 15px !important;
    }
    
    .stButton > button {
        font-size: 13px !important;
        height: 36px !important;            /* قل من 38px لـ 36px */
        padding: 0 8px !important;          /* قل من 10px لـ 8px */
    }
    
    .custom-card {
        height: 80px !important;            /* قل من 85px لـ 80px */
        margin-bottom: 10px !important;
    }
    
    .custom-card p {
        font-size: 1.1rem !important;       /* قل من 1.2rem لـ 1.1rem */
    }
    
    .nav-buttons-container {
        gap: 5px !important;                /* قل من 6px لـ 5px */
        margin: 3px 0 15px 0 !important;    /* رفع أكثر للشاشات الصغيرة */
    }
    
    .nav-buttons-container .stButton > button {
        font-size: 9px !important;          /* قل من 10px لـ 9px */
        height: 32px !important;            /* قل من 35px لـ 32px */
        padding: 0 3px !important;          /* قل من 4px لـ 3px */
    }
}

@media only screen and (max-width: 576px) {
    .block-container {
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    
    .welcome-fixed {
        font-size: 1rem !important;
        padding: 12px !important;
        width: 90% !important;              /* قل من 95% لـ 90% */
        max-width: 90% !important;
    }
    
    .welcome-fixed h3 {
        font-size: 1.2rem !important;
    }
    
    .stButton > button {
        font-size: 12px !important;
        height: 32px !important;            /* قل من 35px لـ 32px */
        padding: 0 6px !important;          /* قل من 8px لـ 6px */
    }
    
    .login-box {
        padding: 20px !important;
        margin-top: 30px !important;        /* رفع أكثر */
        width: 95% !important;
    }
    
    .custom-card {
        height: 75px !important;            /* قل من 80px لـ 75px */
        padding: 10px !important;
    }
    
    .custom-card h4 {
        font-size: 0.95rem !important;      /* قل من 1rem لـ 0.95rem */
    }
    
    .custom-card p {
        font-size: 1rem !important;         /* قل من 1.1rem لـ 1rem */
    }
    
    .nav-buttons-container {
        flex-wrap: wrap !important;
        gap: 4px !important;                /* قل من 5px لـ 4px */
        margin: 2px 0 12px 0 !important;    /* رفع أكثر */
    }
    
    .nav-buttons-container .stButton > button {
        font-size: 8px !important;          /* قل من 9px لـ 8px */
        height: 28px !important;            /* قل من 32px لـ 28px */
        padding: 0 2px !important;          /* قل من 3px لـ 2px */
        min-width: 55px !important;         /* قل من 60px لـ 55px */
    }
}

@media only screen and (max-width: 480px) {
    .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    
    .welcome-fixed {
        font-size: 0.9rem !important;
        width: 95% !important;              /* قل من 100% لـ 95% */
        max-width: 95% !important;
    }
    
    .welcome-fixed h3 {
        font-size: 1.1rem !important;
    }
    
    .stButton > button {
        font-size: 11px !important;
        height: 30px !important;            /* قل من 32px لـ 30px */
    }
    
    .custom-card {
        height: 70px !important;            /* قل من 75px لـ 70px */
    }
    
    .custom-card p {
        font-size: 0.95rem !important;      /* قل من 1rem لـ 0.95rem */
    }
    
    .nav-buttons-container {
        gap: 3px !important;                /* قل من 4px لـ 3px */
        margin: 1px 0 10px 0 !important;    /* رفع نهائي */
    }
    
    .nav-buttons-container .stButton > button {
        font-size: 7px !important;          /* قل من 8px لـ 7px */
        height: 26px !important;            /* قل من 30px لـ 26px */
        padding: 0 1px !important;          /* قل من 2px لـ 1px */
        min-width: 45px !important;         /* قل من 50px لـ 45px */
    }
}

/* ============================================= */
/* ADDITIONAL REDUCTIONS */
/* ============================================= */

/* تقليل الـ selectbox للتاريخ */
div[data-testid="stSelectbox"] {
    width: 100% !important;
}

/* تقليل الـ expander */
.streamlit-expanderHeader {
    width: 100% !important;
    padding: 12px !important;               /* قل شوية */
}

.streamlit-expanderContent {
    width: 100% !important;
    padding: 15px !important;               /* قل شوية */
}

/* تقليل الـ containers */
.stContainer {
    width: 100% !important;
}

/* تقليل الـ markdown containers */
div[data-testid="stMarkdownContainer"] {
    width: 100% !important;
}

/* تقليل الجداول */
.stDataFrame {
    width: 100% !important;
}

/* تقليل الـ alerts */
.stAlert {
    width: 100% !important;
    padding: 12px !important;               /* قل من 15px لـ 12px */
}

/* تقليل الفواصل */
hr {
    margin: 20px 0 !important;              /* قل من 25px لـ 20px */
}

/* تقليل الـ subheaders */
.stSubheader {
    margin-bottom: 15px !important;         /* قل من 20px لـ 15px */
}

/* رفع الـ subheaders للأعلى */
h1, h2, h3, h4, h5, h6 {
    margin-top: 5px !important;             /* رفع العناوين */
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

if "replying_to" not in st.session_state:
    st.session_state.replying_to = None

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

def show_login_animation(username):
    """Show animation during login"""
    loading_placeholder = st.empty()
    loading_placeholder.markdown(show_loading_animation(f"Welcome {username} Team! 🚀"), unsafe_allow_html=True)
    
    time.sleep(1.5)
    loading_placeholder.empty()
    
    st.success(f"✅ Login successful! Welcome {username} Team! 👋")
    
    st.session_state.animation_shown = True
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
    st.session_state.replying_to = None

# ----------------------------
# Navigation Buttons (Top-Right) - رجوع للأزرار مع تحسينات
# ----------------------------
def top_right_buttons():
    """Display navigation buttons at top-right - المعدلة لتقليل العرض"""
    unread_count = 0
    if st.session_state.logged_in and st.session_state.current_page != "notifications":
        unread_count = get_unread_count(st.session_state.username)
    
    # حاوية CSS للأزرار
    st.markdown('<div class="nav-buttons-container">', unsafe_allow_html=True)
    
    # استخدام 5 أعمدة موزعة بالتساوي
    cols = st.columns(5)
    
    with cols[0]:
        if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    with cols[1]:
        if st.button("💬 Feedback", key="nav_feedback", use_container_width=True):
            st.session_state.current_page = "feedback"
            st.rerun()
    
    with cols[2]:
        button_label = "🔔 Notifications"
        if unread_count > 0:
            button_label = f"🔔 ({unread_count})"
        
        if st.button(button_label, key="nav_notifications", use_container_width=True):
            st.session_state.current_page = "notifications"
            st.rerun()
    
    with cols[3]:
        if st.button("ℹ️ About", key="nav_about", use_container_width=True):
            st.session_state.current_page = "about"
            st.rerun()
    
    with cols[4]:
        # زر Logout بلون مختلف
        if st.button("🚪 Logout", key="nav_logout", type="secondary", use_container_width=True):
            logout()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
        

# ----------------------------
# Welcome Message Component
# ----------------------------
def show_welcome_message():
    """Display welcome message that stays in dashboard"""
    if st.session_state.show_welcome and st.session_state.logged_in:
        team_messages = {
            "Admin": "🎯 Admin Dashboard ",
            "CHC": " CHC Team",
            "CNS": " CNS Team ", 
            "GIT": " GIT Team ",
            "Primary Care": " Primary Care ",
            "CVM": " CVM Team ",
            "Power Team": " Power Team ",
            "DGU": " DGU Team ",
            "DNU": " DNU Team ",
            "Sildava": " Sildava Team",
            "Ortho": " Ortho Team ",
            "All": " All Viewer ",
            "managers": " Managemers View",
            "khalid": " Developer View"
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
# Display Feedback Card - FIXED
# ----------------------------
def display_feedback_card(row, is_admin=False):
    """Display a single feedback card"""
    has_reply = pd.notna(row.get('replied_by')) and str(row.get('replied_by')).strip() != ''
    
    # تحديد لون البطاقة - FIXED
    border_color = "#FF9800" if has_reply else "#00c6ff"
    
    with st.container():
        # استخدام Streamlit components مباشرة
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**👤 {row['username']}**")
        with col2:
            st.caption(f"📅 {row['datetime']}")
        
        # عرض التعليق في مربع نص - FIXED
        st.markdown(
            f'<div class="comment-box">{row["comment"]}</div>',
            unsafe_allow_html=True
        )
        
        # إذا كان هناك رد
        if has_reply:
            st.info(f"↩️ Replied by: {row['replied_by']}")
        
        # أزرار الإجراءات للمسؤول
        if is_admin:
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🗑️ Delete", key=f"delete_{row['id']}", type="secondary", use_container_width=True):
                    if delete_feedback(row['id']):
                        st.success("✅ Feedback deleted!")
                        time.sleep(1)
                        st.rerun()
            
            with col_btn2:
                if st.button("📤 Reply", key=f"reply_{row['id']}", type="primary", use_container_width=True):
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
                    elif submit_reply:
                        st.warning("Please write a reply first.")

# ----------------------------
# Main Application UI
# ----------------------------
# استخدام صورة بديلة إذا الصورة الأصلية مش موجودة
bg_image_path = "data/Untitled.png"
if not os.path.exists(bg_image_path):
    # إنشاء صورة بديلة بسيطة
    from PIL import Image
    img = Image.new('RGB', (1920, 1080), color=(25, 25, 112))
    os.makedirs("data", exist_ok=True)
    img.save(bg_image_path)

if not st.session_state.logged_in:
    set_bg_local(bg_image_path, True)
else:
    set_bg_local(bg_image_path, False)

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
    
    st.markdown('<div class="login-btn">', unsafe_allow_html=True)
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DASHBOARD (Logged In) ----------
else:
    # Show navigation buttons (رجوع للأزرار)
    top_right_buttons()
    
    # Show welcome message
    show_welcome_message()
    
    # ----- DASHBOARD PAGE -----
    if st.session_state.current_page == "dashboard":
        st.subheader("📊 Daily Sales Dashboard")
        
        # استخدام كامل العرض للـ columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="custom-card">
                <h4 style="color: #00c6ff; margin: 0 0 8px 0;">📅 Today</h4>
                <p style="font-size: 1.4rem; margin: 0; color: white; font-weight: bold;">{date.today().strftime('%d %b')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="custom-card">
                <h4 style="color: #00c6ff; margin: 0 0 8px 0;">👤 Role</h4>
                <p style="font-size: 1.4rem; margin: 0; color: white; font-weight: bold;">{st.session_state.user_role}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            unread_count = get_unread_count(st.session_state.username)
            notification_text = f"{unread_count} unread" if unread_count > 0 else "All read"
            badge_color = "#FF5252" if unread_count > 0 else "#4CAF50"
            
            st.markdown(f"""
            <div class="custom-card">
                <h4 style="color: #00c6ff; margin: 0 0 8px 0;">🔔 Notifications</h4>
                <p style="font-size: 1.4rem; margin: 0; color: {badge_color}; font-weight: bold;">{notification_text}</p>
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
                        
                        if uploaded_files and st.button("🚀 Upload Files", type="primary", key="upload_button", use_container_width=True):
                            today_folder = os.path.join(BASE_PATH, selected_day)
                            os.makedirs(today_folder, exist_ok=True)
                            
                            success_count = 0
                            for file in uploaded_files:
                                with open(os.path.join(today_folder, file.name), "wb") as f:
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
                                    c1, c2, c3 = st.columns([6, 1, 2])
                                    
                                    with c1:
                                        st.write(f"📄 **{file}**")
                                    
                                    with c2:
                                        if st.button("🗑️", key=f"del_{file}", use_container_width=True):
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
                                                key=f"dl_{file}",
                                                use_container_width=True
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
                            
                            # استخدام 2 columns للملفات
                            cols = st.columns(2)
                            for idx, file in enumerate(allowed_files):
                                with cols[idx % 2]:
                                    with st.container():
                                        st.markdown(f"""
                                        <div style="
                                            background: rgba(255,255,255,0.1);
                                            padding: 14px;
                                            border-radius: 10px;
                                            margin-bottom: 10px;
                                            width: 100% !important;
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
    
    # ----- FEEDBACK PAGE -----
    elif st.session_state.current_page == "feedback":
        st.subheader("💬 Feedback System")
        
        if st.session_state.user_role == "Admin":
            df = load_feedback()
            if not df.empty:
                st.markdown(f"### 📋 Total Feedback: {len(df)}")
                
                # Delete all button
                if st.button("🗑️ Delete All Feedback", type="secondary", key="delete_all_btn", use_container_width=True):
                    if delete_all_feedback():
                        st.success("✅ All feedback deleted!")
                        show_confetti_animation()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete feedback")
                
                st.markdown("---")
                
                # Display feedback using the fixed function
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
                    height=140,  # قل من 150 لـ 140
                    key="user_feedback"
                )
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    submit = st.form_submit_button("📤 Submit", type="primary", use_container_width=True)
                
                if submit and comment.strip():
                    add_feedback(st.session_state.username, comment.strip())
                    st.success("✅ Thank you for your feedback! 🌟")
                    show_confetti_animation()
                    time.sleep(1.5)
                    st.rerun()
                elif submit:
                    st.warning("⚠️ Please write something before submitting.")
    
    # ----- NOTIFICATIONS PAGE - SIMPLIFIED AND FIXED -----
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
                    is_new = not row.get('is_read', False)
                    replied_by = row.get('replied_by', '')
                    
                    # استخدام تصميم مبسط وواضح
                    st.markdown(f"""
                    <div class="notification-item {'unread' if is_new else ''}">
                        <div class="notification-header">
                            <div class="notification-title">
                                👤 {replied_by if replied_by else row['username']} replied to your feedback
                                {'<span class="new-badge">NEW</span>' if is_new else ''}
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
                    
                    if is_new:
                        col_btn1, col_btn2 = st.columns([1, 5])
                        with col_btn1:
                            if st.button("✓ Mark as Read", key=f"read_{row.get('id', idx)}", use_container_width=True):
                                if mark_as_read(row.get('id', idx)):
                                    st.success("Notification marked as read!")
                                    time.sleep(0.5)
                                    st.rerun()
                        with col_btn2:
                            st.write("")  # مسافة فارغة
                    
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
                        <div class="notification-item read">
                            <div class="notification-header">
                                <div class="notification-title">
                                    👤 {row['username']}
                                    {f"<span style='color: #FF9800; font-size: 0.9rem; margin-left: 10px;'>↩️ {row['replied_by']}</span>" if is_reply else ""}
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
                        
                        st.markdown("---")
        
        st.markdown("---")
        if st.button("← Back to Dashboard", key="back_to_dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    # ----- ABOUT PAGE -----
    elif st.session_state.current_page == "about":
        st.subheader("ℹ️ About This Dashboard")
        
        with st.container():
            st.markdown("""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                padding: 22px;
                border-radius: 15px;
                border-left: 5px solid #00c6ff;
                margin-bottom: 15px;
                backdrop-filter: blur(10px);
                width: 100% !important;
            ">
            """, unsafe_allow_html=True)
            
            st.markdown("#### 🎯 Mission")
            st.markdown("Streamline daily sales operations and provide real-time insights for all teams.")
            
            st.markdown("---")

            st.markdown("---")
            
            st.markdown("####Commercial Excellence  Team")
            st.markdown("""
            • **Commercial Excellnece Director** Dr- Khaled Gamal   
            • **CHC** - Healthcare Division  
            • **CNS** - Neuroscience Division  
            • **GIT** - Gastroenterology  
            • **Primary Care** - General Medicine  
            • **CVM** - Cardiology Division  
            • **Power Team** - Special Operations  
            • **All Teams** - Comprehensive access
            """)
            
            st.markdown("#### ✨ Features")
            st.markdown("""
            ✅ **File Management** - Upload and download sales files  
            ✅ **Feedback System** - Share thoughts and suggestions  
            ✅ **Notifications** - Get alerts for replies  
            ✅ **Admin Controls** - Manage feedback and files  
            ✅ **Team-Based Access** - Different views for different teams  
            ✅ **Mobile Responsive** - Works on all devices
            """)
            

            
            st.markdown("---")
            
            st.markdown("""
            <div style="text-align: center; padding: 14px; background: rgba(0,198,255,0.1); border-radius: 10px; margin-top: 20px; width: 100% !important;">
                <p style="margin: 0; font-size: 1.1rem; color: white;">
                    🚀 <strong>Sales Dashboard | Secure & Efficient</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
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
    <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.85rem; padding: 12px; width: 100% !important;">
        <p>📊 Daily Sales Dashboard | © 2026 | 🔒 Secure Access {notification_text}</p>
    </div>
    """, unsafe_allow_html=True)