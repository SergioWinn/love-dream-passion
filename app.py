import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LOVE DREAM PASSION", layout="wide", page_icon="🔴")

# REKOMENDASI: Ubah ke 2000 (2 detik) kalau masih kerasa berat di HP
st_autorefresh(interval=1000, key="ldp_fast_refresh")

# --- 2. OPTIMIZED CSS (Lebih ramping) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1rem; max-width: 1400px; }
.ldp-header { text-align: center; margin-bottom: 20px; }
.live-badge { display: inline-flex; align-items: center; gap: 5px; font-weight: 700; font-size: 11px; color: #10B981; background: rgba(16,185,129,0.1); padding: 3px 10px; border-radius: 15px; }
.live-dot { height: 7px; width: 7px; background: #10B981; border-radius: 50%; animation: p 1s infinite; }
@keyframes p { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; justify-content: center; }
.ldp-card { background: rgba(128,128,128,0.05); border-radius: 10px; padding: 15px; border: 1px solid rgba(128,128,128,0.15); display: flex; flex-direction: column; text-align: center; }
.ldp-card.avail { border-bottom: 4px solid #10B981; }
.ldp-card.warn { border-bottom: 4px solid #FBBF24; }
.ldp-card.sold { border-bottom: 4px solid #EF4444; opacity: 0.7; }
.c-member { font-weight: 700; font-size: 14px; margin-bottom: 10px; height: 2.5em; overflow: hidden; }
.c-badge { font-size: 9px; font-weight: 800; padding: 4px; border-radius: 10px; text-transform: uppercase; }
.ldp-card.avail .c-badge { background: rgba(16,185,129,0.2); color: #10B981; }
.ldp-card.warn .c-badge { background: rgba(251,191,36,0.2); color: #D97706; }
.ldp-card.sold .c-badge { background: #EF4444; color: #fff; }
@media (max-width: 500px) { .cards-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; } }
</style>
""".replace('\n', ''), unsafe_allow_html=True)

st.markdown('<div class="ldp-header"><h2>Meet & Greet - 23 May</h2><div class="live-badge"><span class="live-dot"></span> LIVE 1s</div></div>', unsafe_allow_html=True)

# --- 3. DATA ENGINE (Optimized Timeout) ---
@st.cache_data(ttl=1)
def get_data(url):
    try:
        # Timeout diperketat ke 2 detik biar skrip nggak 'ngagantung'
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=2)
        return r.json() if r.status_code == 200 else None
    except: return None

def draw_ui(url, key_prefix, ev_type):
    search_key = f"s_{key_prefix}"
    st.text_input("Cari Oshi...", key=search_key)
    query = st.session_state.get(search_key, "").lower().strip()
    
    data = get_data(url)
    if not data: return st.info("Reconnecting...")

    for sesi in data.get('data', []):
        members = sesi.get('session_members', [])
        if query:
            members = [m for m in members if query in m.get('member_name', '').lower()]
        if not members: continue

        st.caption(f"**{sesi['label']}** | {sesi['start_time'][:5]}-{sesi['end_time'][:5]}")
        
        html = '<div class="cards-grid">'
        for m in members:
            q = m.get('quota', 0)
            # Logika Warna
            limit = 5 if ev_type == "2shot" else 20
            if q <= 0: cls, lbl = "sold", "HABIS"
            elif q < limit: cls, lbl = "warn", f"SISA {q}"
            else: cls, lbl = "avail", f"SISA {q}"
            
            html += f'<div class="ldp-card {cls}"><div class="c-member">{m["member_name"]}</div><div class="c-badge">{lbl}</div></div>'
        
        st.markdown(html + '</div>', unsafe_allow_html=True)

# --- 4. TABS ---
t1, t2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])
with t1: draw_ui("https://jkt48.com/api/v1/exclusives/EX579E/bonus?lang=id", "2s", "2shot")
with t2: draw_ui("https://jkt48.com/api/v1/exclusives/EXE588/bonus?lang=id", "mng", "mng")
