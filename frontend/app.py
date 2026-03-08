import streamlit as st
import pandas as pd
import requests
import time
import os
import base64
from streamlit_mic_recorder import mic_recorder

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Vox | Talk to your Data", layout="wide")

# --- 2. SESSION STATE INITIALIZATION (Must be at top level) ---
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "threat_scores" not in st.session_state:
    st.session_state.threat_scores = [0.2] * 20
if "latest_reply" not in st.session_state:
    st.session_state.latest_reply = ""
if "last_line_count" not in st.session_state:
    st.session_state.last_line_count = 0
if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None

# --- 3. STATIC CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #30363d; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    [data-testid="stHorizontalBlock"] { align-items: center !important; }
    [data-testid="stLineChart"] { margin-top: 38px; }
    .centered-title { text-align: center; width: 100%; margin: 0; padding: 0; }
    </style>
    """, unsafe_allow_html=True)

# Constants
BACKEND_URL = "http://127.0.0.1:8000"
LIVE_LOG_FILE = "live_stream.log"
LOGO_PATH = os.path.join("frontend", "vox_logo.png")

# --- 4. HEADER ---
h_col1, h_col2, h_col3 = st.columns([1, 2, 1])
with h_col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=150)
with h_col2:
    st.markdown("<h1 class='centered-title'>Vox: Talk To Your Data</h1>", unsafe_allow_html=True)
with h_col3:
    st.empty()

st.divider()

# --- 5. FRAGMENT 1: THE LIVE DASHBOARD ---
@st.fragment(run_every=1.0)
def live_dashboard():
    current_lines = []
    if os.path.exists(LIVE_LOG_FILE):
        with open(LIVE_LOG_FILE, "r") as f:
            current_lines = f.readlines()
    
    line_count = len(current_lines)
    if line_count > st.session_state.last_line_count:
        latest_line = current_lines[-1].upper() if current_lines else ""
        if "FATAL" in latest_line: score = 10.0
        elif "CRITICAL" in latest_line: score = 9.0
        elif "SECURITY" in latest_line: score = 8.5
        elif "ERROR" in latest_line: score = 5.0
        elif "WARNING" in latest_line: score = 4.0
        else: score = 0.2
        
        st.session_state.threat_scores.append(score)
        st.session_state.threat_scores = st.session_state.threat_scores[-20:]
        st.session_state.last_log_content = "".join(current_lines[-12:])
        st.session_state.last_line_count = line_count

    c_logs, c_graph = st.columns([1, 1])
    with c_logs:
        st.markdown("##### System Event Stream")
        content = st.session_state.get("last_log_content", "Waiting for pulse...")
        st.code(content, language="text")
    with c_graph:
        st.markdown("##### Activity Risk Index")
        chart_df = pd.DataFrame(st.session_state.threat_scores, columns=["Risk Level"])
        st.line_chart(chart_df, height=275, use_container_width=True)

live_dashboard()

# --- 6. FRAGMENT 2: THE CHAT INTERFACE ---
@st.fragment
def chat_interface():
    st.divider()
    st.markdown("##### Intelligence Interface")

    def autoplay_audio(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
            st.markdown(md, unsafe_allow_html=True)

    # UI Inputs
    c1, c2, c3 = st.columns([0.6, 4, 0.8])
    with c1:
        audio_input = mic_recorder(start_prompt="Record", stop_prompt="Stop", key='vox_mic')
    with c2:
        # Dynamic key based on query_count ensures text clears on success
        user_text = st.text_input(
            "Query", 
            key=f"user_query_{st.session_state.query_count}", 
            placeholder="Analyze current stream...", 
            label_visibility="collapsed"
        )
    with c3:
        send_btn = st.button("Send", use_container_width=True)

    status_area = st.empty()
    output_area = st.empty()

    # Audio change detection
    is_new_audio = False
    if audio_input is not None:
        if audio_input['id'] != st.session_state.last_audio_id:
            is_new_audio = True

    # Processing Logic
    if is_new_audio or (send_btn and user_text):
        with status_area:
            with st.spinner("Vox is analyzing..."):
                try:
                    if is_new_audio:
                        files = {"audio": ("query.wav", audio_input['bytes'], "audio/wav")}
                        res = requests.post(f"{BACKEND_URL}/ask_live_voice", files=files)
                        st.session_state.last_audio_id = audio_input['id']
                    else:
                        res = requests.post(f"{BACKEND_URL}/ask_live_text", json={"question": user_text})

                    if res.status_code == 200:
                        ans = res.json().get('answer', "No response.")
                        st.session_state.latest_reply = f"Vox Analysis: {ans}"
                        
                        if is_new_audio:
                            audio_res = requests.get(f"{BACKEND_URL}/get_audio")
                            with open("response.mp3", "wb") as f: f.write(audio_res.content)
                            autoplay_audio("response.mp3")
                        
                        # Increment to force-clear the text widget and state
                        st.session_state.query_count += 1
                        status_area.empty()
                        st.rerun(scope="fragment")
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.latest_reply:
        output_area.info(st.session_state.latest_reply)

chat_interface()