"""Chabu AI — Hackathon Mission Control Dashboard."""

import html
import json
import os
import sys
import time
from datetime import datetime

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit as st

st.set_page_config(
    page_title="Chabu AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
hide_streamlit = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

st.markdown(hide_streamlit, unsafe_allow_html=True)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_handler import process_web_command
from shared.config import load_config
from shared.logger import get_log_path, get_status
from shared.memory import recall, remember
from shared.notes_tasks import (
    add_note,
    add_task,
    complete_task,
    delete_note,
    delete_task,
    get_notes,
    get_tasks,
)
from shared.stats import get_dashboard_stats

CFG = load_config()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")
WAKE_WORD = CFG.get("wake_word", "harry potter")



st_autorefresh(interval=2000, key="chabu_hackathon_sync")

QUICK_COMMANDS = [
    ("🌐 Google", "open google"),
    ("💼 LinkedIn", "open linkedin"),
    ("▶️ YouTube", "open youtube"),
    ("📝 Notes", "show notes"),
    ("✅ Tasks", "show tasks"),
    ("🖥️ System", "check system"),
    ("📅 Plan day", "plan my day"),
    ("👋 Hello", "hello"),
]

FEATURES = [
    ("🎤", "Voice-first", f"Wake with “{WAKE_WORD}”, then speak naturally"),
    ("🧠", "Gemini AI", "Multilingual Q&A, email drafts, day planning"),
    ("📋", "Productivity", "Notes, tasks, timed voice reminders"),
    ("🖼️", "System tools", "Screenshots, camera, PDF analysis"),
    ("📡", "Live sync", "CLI voice + this dashboard stay in sync"),
    ("🎭", "Personalities", "Funny, pro, teacher, or friend mode"),
]

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;600;700&display=swap');
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 1rem; max-width: 1480px; }
.stApp {
    background: #0a0c10;

    background-image:
        radial-gradient(
            ellipse 80% 50% at 50% -20%,
            rgba(0,219,231,0.12),
            transparent
        ),
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);

    background-size:
        100% 100%,
        28px 28px,
        28px 28px;

    color: #e5e2e1;
    font-family: 'Inter', sans-serif;
}
.hack-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #00fb86;
    border: 1px solid rgba(0, 251, 134, 0.4);
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
}
.metric-card {
    background: linear-gradient(
        145deg,
        rgba(20,20,30,0.95),
        rgba(10,10,18,0.95)
    );

    border: 1px solid rgba(0,219,231,0.35);

    border-radius: 14px;

    padding: 1rem;

    text-align: center;

    box-shadow:
        0 0 15px rgba(0,219,231,0.15),
        0 0 30px rgba(0,219,231,0.08);

    transition: all 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow:
        0 0 25px rgba(0,219,231,0.35),
        0 0 50px rgba(0,219,231,0.15);
        transform: translateY(-8px) scale(1.03);
}


.metric-val {
   font-size: 2.2rem;
    font-weight: 800;
    color: #00eaff;

    text-shadow:
        0 0 10px #00eaff,
        0 0 20px rgba(0,234,255,0.6);
}
.metric-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #849495;
    margin-top: 0.35rem;
}
.glass {
    
       background: rgba(26,28,36,0.75);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 3px solid #00dbe7;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.75rem;
}
.panel-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #00dbe7;
    margin-bottom: 0.5rem;
}
.feat-card {
    padding: 0.75rem;
    border-radius: 8px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 0.5rem;
}
.feat-card h4 { margin: 0 0 0.25rem 0; color: #e1fdff; font-size: 0.9rem; }
.feat-card p { margin: 0; font-size: 0.78rem; color: #849495; }
.status-on { color: #00fb86; font-weight: 600; }
.status-off { color: #ff6b8a; font-weight: 600; }
div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,219,231,0.15) !important;
    border-radius: 10px !important;
}


.stButton > button {
    background: linear-gradient(
        135deg,
        rgba(0,234,255,0.15),
        rgba(0,120,255,0.10)
    );

    color: white !important;
    border: 1px solid rgba(0,234,255,0.4);
    border-radius: 12px;
    height: 55px;
    font-weight: 700;

    box-shadow:
        0 0 10px rgba(0,234,255,0.15);

    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);

    border: 1px solid #00eaff;

    box-shadow:
        0 0 20px rgba(0,234,255,0.4),
        0 0 40px rgba(0,234,255,0.2);
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 12px;
    color: white;
}

.stTabs [aria-selected="true"] {
    background: rgba(0,234,255,0.15) !important;
    border: 1px solid rgba(0,234,255,0.4);
    box-shadow: 0 0 15px rgba(0,234,255,0.3);
}


.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
}
</style>
""",
    unsafe_allow_html=True,
)


def load_chat_history(limit=30):
    log_path = get_log_path()
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            return json.load(f)[-limit:]
    except (json.JSONDecodeError, OSError):
        return []


def format_time(ts):
    if not ts or "T" not in str(ts):
        return ""
    try:
        return datetime.fromisoformat(ts).strftime("%H:%M")
    except ValueError:
        return ""


def run_command(cmd):
    if cmd:
        with st.spinner("Executing…"):
            process_web_command(cmd)
        time.sleep(0.35)
        st.rerun()


if "pending_command" not in st.session_state:
    st.session_state.pending_command = None

stats = get_dashboard_stats()
status_data = get_status()
is_awake = status_data.get("is_awake", False)
status_color = "#00ff88" if is_awake else "#ff5555"
status_text = "ONLINE" if is_awake else "STANDBY"

st.markdown(f"""
<div style="
text-align:center;
margin-bottom:15px;
">
<span style="
background:{status_color};
padding:8px 18px;
border-radius:20px;
font-weight:bold;
color:black;
">
● {status_text}
</span>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar (hackathon pitch + settings) ───
with st.sidebar:
    
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=180)
    st.markdown(f'<span class="hack-badge">Hackathon build · {html.escape(CFG.get("version", "1.0"))}</span>', unsafe_allow_html=True)
    st.markdown("""
        <h1 style="
        color:#00eaff;
        font-size:38px;
        font-weight:800;
        text-shadow:
        0 0 10px #00eaff,
        0 0 20px #00eaff;
        ">
        🤖 CHABU AI
        </h1>
      """, unsafe_allow_html=True)
    st.markdown("""
       <div style="
       color:#9aa6b2;
       font-size:16px;
        margin-top:-10px;
        margin-bottom:20px;
        ">
       Your Voice • Your Control
      </div>
      """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🖥 SYSTEM STATUS")

    st.success("🟢 Voice Engine Online")
    st.success("🟢 Gemini AI Connected")
    st.success("🟢 Memory Core Active")
    st.success("🟢 Desktop Control Ready")
    

    

    st.markdown("**⚙️ Operator profile**")
    new_name = st.text_input("Display name", value=recall("username") or "", placeholder="Chabu")
    personality = st.selectbox(
        "AI personality",
        ["professional", "funny", "teacher", "friend"],
        index=["professional", "funny", "teacher", "friend"].index(
            (recall("personality") or "professional").lower()
        )
        if (recall("personality") or "professional").lower() in ["professional", "funny", "teacher", "friend"]
        else 0,
    )
    if st.button("Save profile", use_container_width=True):
        if new_name.strip():
            remember("username", new_name.strip().title())
        remember("personality", personality)
        st.success("Profile saved!")
        time.sleep(0.3)
        st.rerun()

    st.markdown("---")
    st.markdown("**🎬 Demo script (judges)**")
    for i, cmd in enumerate(CFG.get("demo_commands", []), 1):
        st.caption(f"{i}. “{cmd}”")
    if st.button("▶ Run demo: hello", use_container_width=True):
        st.session_state.pending_command = "hello"


   
# HEADER

st.markdown(f"""
       <div style="
       text-align:center;
        font-size:28px;
        font-weight:800;
       color:#00eaff;
        padding:10px;
        border:1px solid rgba(0,234,255,0.4);
        border-radius:10px;
        text-shadow:
        0 0 10px #00eaff,
        0 0 20px #00eaff;
        ">
        🛰️ MISSION CONTROL • WAKE WORD: {WAKE_WORD.upper()}
       </div>
      """, unsafe_allow_html=True) 
st.markdown(f"""
<div style="
background: linear-gradient(
135deg,
rgba(0,234,255,0.20),
rgba(0,100,255,0.12)
);
padding:35px;
border-radius:22px;
border:1px solid rgba(0,234,255,0.35);
box-shadow:
0 0 30px rgba(0,234,255,0.20),
0 0 60px rgba(0,234,255,0.10);
text-align:center;
margin-bottom:25px;
">

<div style="
font-size:14px;
letter-spacing:4px;
color:#00eaff;
margin-bottom:10px;
">
NEXT GEN AI DESKTOP ASSISTANT
</div>

<h1 style="
font-size:52px;
font-weight:900;
color:white;
margin:0;
text-shadow:
0 0 15px #00eaff,
0 0 30px rgba(0,234,255,0.7);
">
🤖 CHABU AI
</h1>

<h3 style="
color:#d8e7ff;
margin-top:12px;
">
Your Voice • Your Control • Your Assistant
</h3>

<p style="
color:#9aa6b2;
font-size:18px;
margin-top:15px;
">
Voice Control • Gemini AI • Memory • Notes • Tasks • Automation
</p>

</div>
""", unsafe_allow_html=True)
    
m1, m2, m3, m4, m5 = st.columns(5)
metrics = [
    (str(stats["commands_today"]), "Commands today"),
    (str(stats["notes_count"]), "Smart notes"),
    (f'{stats["tasks_done"]}/{stats["tasks_total"]}', "Tasks done"),
    (f'{stats["tasks_pct"]}%', "Completion"),
    ("ONLINE" if is_awake else "STANDBY", "Voice core"),
]
for col, (val, lbl) in zip([m1, m2, m3, m4, m5], metrics):
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-val">{html.escape(val)}</div>'
            f'<div class="metric-lbl">{html.escape(lbl)}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("")

tab_mission, tab_prod, tab_chat = st.tabs(["🛰️ MISSION CONTROL", "📋 PRODUCTIVITY", "💬 NEURAL TERMINAL"])

with tab_mission:
    c_left, c_right = st.columns([1.2, 1])
    with c_left:
        st.markdown('<div class="panel-tag">Quick launch</div>', unsafe_allow_html=True)
        for i in range(0, len(QUICK_COMMANDS), 4):
            row = QUICK_COMMANDS[i : i + 4]
            cols = st.columns(len(row))
            for col, (label, cmd) in zip(cols, row):
                with col:
                    if st.button(label, key=f"q_{cmd}", use_container_width=True):
                        st.session_state.pending_command = cmd

        status_cls = "status-on" if is_awake else "status-off"
        status_lbl = "AWAKE & LISTENING" if is_awake else "STANDBY"
        st.markdown(f"""
         <div class="glass">

        <h3 style="color:#00eaff;">
        🧠 AI CORE STATUS
        </h3>

        <hr>

        <p>🎤 Voice Engine : <span class="{status_cls}">{status_lbl}</span></p>

        <p>⚡ Current Action :
         <b>{html.escape(status_data.get("status", "Idle"))}</b></p>

        <p>🔑 Wake Word :
       <b>{WAKE_WORD}</b></p>

        <p>👤 Operator :
      <b>{html.escape((recall("username") or "Guest").title())}</b></p>

      <p>🎭 Personality :
       <b>{html.escape((recall("personality") or "Professional").title())}</b></p>

      </div>
      """, unsafe_allow_html=True)

    with c_right:
        st.markdown('<div class="panel-tag">Why Chabu wins</div>', unsafe_allow_html=True)
        for icon, title, desc in FEATURES:
            st.markdown(
                f'<div class="feat-card"><h4>{icon} {html.escape(title)}</h4><p>{html.escape(desc)}</p></div>',
                unsafe_allow_html=True,
            )

with tab_prod:
    p_notes, p_tasks = st.columns(2)

    with p_notes:
        st.markdown('<div class="panel-tag">Smart notes</div>', unsafe_allow_html=True)
        note_text = st.text_area("New note", height=80, placeholder="Meeting ideas, reminders…", label_visibility="collapsed")
        if st.button("➕ Save note", key="add_note_btn", use_container_width=True):
            if note_text.strip():
                add_note(note_text.strip())
                st.success("Note saved!")
                st.rerun()
            else:
                st.warning("Type something first.")

        notes = get_notes()
        if notes:
            for i, n in enumerate(notes):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"**#{i+1}** {n}")
                with col_b:
                    if st.button("🗑", key=f"dn_{i}"):
                        delete_note(i)
                        st.rerun()
        else:
            st.caption("No notes yet.")

    with p_tasks:
        st.markdown('<div class="panel-tag">System tasks</div>', unsafe_allow_html=True)
        task_text = st.text_input("New task", placeholder="Finish hackathon slide deck…", label_visibility="collapsed")
        if st.button("➕ Add task", key="add_task_btn", use_container_width=True):
            if task_text.strip():
                add_task(task_text.strip())
                st.success("Task added!")
                st.rerun()

        tasks = get_tasks()
        if tasks:
            for i, t in enumerate(tasks):
                done = t.get("completed", False)
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    prefix = "~~" if done else ""
                    suffix = "~~" if done else ""
                    st.markdown(f"{prefix}{'✅' if done else '⏳'} {t['task']}{suffix}")
                with col_b:
                    if not done and st.button("Done", key=f"ct_{i}"):
                        complete_task(i)
                        st.rerun()
                with col_c:
                    if st.button("🗑", key=f"dt_{i}"):
                        delete_task(i)
                        st.rerun()
            st.progress(stats["tasks_pct"] / 100, text=f"{stats['tasks_pct']}% complete")
        else:
            st.caption("No tasks yet.")

with tab_chat:
    history = load_chat_history()
    with st.container(height=480):
        if history:
            for entry in history:
                ts = format_time(entry.get("time", ""))
                if entry.get("user"):
                    with st.chat_message("user", avatar="🧑"):
                        if ts:
                            st.caption(ts)
                        st.markdown(entry["user"])
                if entry.get("assistant"):
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(entry["assistant"])
        else:
            st.markdown(
                """
                <div style="text-align:center;padding:3rem;color:#849495;">
                <p style="color:#00dbe7;font-family:monospace;">[ NEURAL LINK STANDBY ]</p>
                <p>Say <strong style="color:#e1fdff;">harry potter</strong> in the CLI, or type below.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

user_input = st.chat_input(f"Command Chabu… (wake word: {WAKE_WORD})")
command = user_input or st.session_state.pending_command
if command:
    st.session_state.pending_command = None
    run_command(command)
st.markdown("""
<hr>
<center>

<h4 style='color:#00eaff'>
🚀 CHABU AI
</h4>

<p style='color:#7f8c9d'>
Built with Streamlit • Gemini AI • Voice Recognition
</p>

</center>
""", unsafe_allow_html=True)    
