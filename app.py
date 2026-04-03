import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LOVE DREAM PASSION", layout="wide", page_icon="🔴")

# --- 2. SILENT AUTO REFRESH (1 Detik) ---
st_autorefresh(interval=1000, key="ldp_autorefresh")

# --- 3. UI/UX MODERN STYLING (CSS DIPADATKAN AGAR TIDAK BOCOR) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #1f2937; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }
    .ldp-main-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 25px; border-bottom: 1px solid rgba(0,0,0,0.05); padding-bottom: 20px; flex-wrap: wrap; gap: 10px; }
    .ldp-title { font-weight: 800; font-size: 2.5rem; color: #111827; margin: 0; line-height: 1.2; }
    .live-badge-wrapper { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 13px; color: #10B981; background-color: rgba(16, 185, 129, 0.1); padding: 6px 14px; border-radius: 30px; border: 1px solid rgba(16, 185, 129, 0.2); }
    .live-dot { height: 10px; width: 10px; background-color: #10B981; border-radius: 50%; display: inline-block; animation: ldp_pulse 2s infinite; }
    @keyframes ldp_pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(1.1); } 100% { opacity: 1; transform: scale(1); } }
    .stTabs [data-baseweb="tab-list"] { gap: 40px; }
    .stTabs [data-baseweb="tab"] {
