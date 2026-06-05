import streamlit as st
import os
import sys
import time
from datetime import datetime
import base64

# Add parent directory to path to find shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.memory import recall, remember
from shared.logger import get_recent_history, get_status

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Jarvis - Your Voice Your Control",
    page_icon="🤖",
    layout="wide"
)

# --- AUTO REFRESH ---
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=1500, key="datarefresh")

# --- ASSETS ---
def get_base64_of_bin_file(bin_file):
    if not os.path.exists(bin_file): return ""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png"))
logo_base64 = get_base64_of_bin_file(logo_path)

# --- HYPER-DIGITAL JARVIS STYLING ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@400;700&display=swap');

    /* Background: Tech Grid */
    .stApp {{
        background-color: #0b0e11;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }}

    /* Main Portal Branding */
    .portal-container {{
        text-align: center;
        padding-top: 20px;
    }}
    .main-logo {{
        width: 140px;
        border: 1px solid #00ff41;
        padding: 5px;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.4);
        margin-bottom: 15px;
    }}
    .jarvis-title {{
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 50px;
        color: #00ff41;
        letter-spacing: 5px;
        text-transform: uppercase;
        text-shadow: 0 0 15px rgba(0, 255, 65, 0.6);
        margin-bottom: 5px;
    }}

    /* Status Orb */
    .status-orb {{
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
    }}
    .orb-standby {{ background-color: #444; box-shadow: 0 0 5px #444; }}
    .orb-active {{ background-color: #00ff41; box-shadow: 0 0 15px #00ff41; animation: pulse 1s infinite; }}
    .orb-listening {{ background-color: #00d1ff; box-shadow: 0 0 15px #00d1ff; animation: pulse 1s infinite; }}

    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.3); opacity: 0.7; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}

    /* Chat Messages - Extra Clear Text */
    .stChatMessage {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 255, 65, 0.1) !important;
        margin-bottom: 12px !important;
    }}
    .chat-text {{
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 500 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    }}
    .chat-label {{
        font-family: 'Orbitron', sans-serif;
        font-size: 11px;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }}

    /* Sidebar Logo */
    .side-logo {{
        width: 100px;
        border: 1px solid #00ff41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
        margin-bottom: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if logo_base64:
        st.markdown(f'<div style="text-align:center"><img src="data:image/png;base64,{logo_base64}" class="side-logo"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; font-family:Orbitron; color:#00ff41; font-size:18px;'>JARVIS</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.write(f"USER: **{recall('username') or 'OPERATOR'}**")
    st.write(f"MODE: **{recall('personality') or 'FUNNY'}**")
    st.markdown("---")
    if st.button("RESET VIEW"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN UI ---
st.markdown('<div class="portal-container">', unsafe_allow_html=True)
if logo_base64:
    st.markdown(f'<img src="data:image/png;base64,{logo_base64}" class="main-logo">', unsafe_allow_html=True)
st.markdown('<div class="jarvis-title">JARVIS</div>', unsafe_allow_html=True)

status_info = get_status()
history = get_recent_history(20)
history.reverse()

status = status_info.get("status", "Standing By")
is_awake = status_info.get("is_awake", False)

orb_class = "orb-standby"
if status == "Listening...": orb_class = "orb-listening"
elif is_awake: orb_class = "orb-active"

st.markdown(f"""
<div style="margin-top:10px; margin-bottom:20px;">
    <span class="status-orb {orb_class}"></span>
    <span style="font-family:Orbitron; font-size:14px; color:#00ff41; letter-spacing:2px; text-shadow:0 0 5px rgba(0,255,65,0.5);">{status.upper()}</span>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main Feed
for role, content in history:
    with st.chat_message(role):
        label = "JARVIS" if role == "assistant" else (recall('username') or "OPERATOR")
        color = "#00ff41" if role == "assistant" else "#00d1ff"
        st.markdown(f'<div class="chat-label" style="color:{color}">[{label}]</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-text">{content}</div>', unsafe_allow_html=True)
