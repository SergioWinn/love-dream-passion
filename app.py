import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LOVE DREAM PASSION", layout="wide", page_icon="🔴")

# --- 2. SUPER FAST REFRESH (3 Detik) ---
st_autorefresh(interval=3000, key="ldp_hyper_refresh")

# --- 3. UI/UX STYLING (CLEAN VERSION) ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }
.ldp-header { text-align: center; margin-bottom: 30px; border-bottom: 1px solid rgba(128,128,128,0.2); padding-bottom: 20px; }
.ldp-title { font-weight: 800; font-size: 2.2rem; margin: 0; margin-bottom: 10px; }
.live-badge { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; font-size: 12px; color: #10B981; background: rgba(16,185,129,0.1); padding: 5px 12px; border-radius: 20px; }
.live-dot { height: 8px; width: 8px; background: #10B981; border-radius: 50%; display: inline-block; animation: pulse_dot 1s infinite; }
@keyframes pulse_dot { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 15px; justify-content: center; }
.ldp-card { background: rgba(128,128,128,0.05); border-radius: 12px; padding: 20px; border: 1px solid rgba(128,128,128,0.2); display: flex; flex-direction: column; justify-content: space-between; height: 100%; text-align: center; }
.ldp-card.avail { border-bottom: 5px solid #10B981; }
.ldp-card.warn { border-bottom: 5px solid #FBBF24; animation: card_pulse 1.5s infinite; }
.ldp-card.sold { border-bottom: 5px solid #EF4444; background: rgba(239, 68, 68, 0.05); }
@keyframes card_pulse { 0% { box-shadow: 0 0 0 0 rgba(251,191,36,0.4); } 70% { box-shadow: 0 0 0 10px rgba(251,191,36,0); } 100% { box-shadow: 0 0 0 0 rgba(251,191,36,0); } }
.c-jalur { font-size: 10px; opacity: 0.6; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; }
.c-member { font-weight: 700; font-size: 15px; line-height: 1.2; margin-bottom: 15px; height: 2.4em; overflow: hidden; }
.c-badge { font-size: 10px; font-weight: 800; padding: 6px; border-radius: 15px; text-transform: uppercase; width: 100%; display: block; }
.ldp-card.avail .c-badge { background: rgba(16,185,129,0.2); color: #10B981; }
.ldp-card.warn .c-badge { background: rgba(251,191,36,0.25); color: #D97706; }
.ldp-card.sold .c-badge { background: #EF4444; color: #FFFFFF; }
@media (max-width: 500px) { .cards-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; } .ldp-card { padding: 15px 10px; } }
</style>
"""
st.markdown(css.replace('\n', '').replace('\r', ''), unsafe_allow_html=True)

# --- 4. HEADER ---
st.markdown('<div class="ldp-header"><h1 class="ldp-title">Meet & Greet - 23 May</h1><div class="live-badge"><span class="live-dot"></span> LIVE</div></div>', unsafe_allow_html=True)

# --- 5. LOGIKA DATA & STATUS ---
URL_2SHOT = "https://jkt48.com/api/v1/exclusives/EX579E/bonus?lang=id"
URL_MNG = "https://jkt48.com/api/v1/exclusives/EXE588/bonus?lang=id"

@st.cache_data(ttl=1)
def get_data(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def get_status_info(quota, ev_type):
    if quota <= 0:
        return "sold", "HABIS"
    limit = 5 if ev_type == "2shot" else 20
    if quota < limit:
        return "warn", f"SISA {quota}"
    return "avail", f"SISA {quota}"

# --- 6. RENDER ENGINE ---
def draw_ui(url, key_prefix, ev_type):
    search_key = f"search_input_{key_prefix}"
    st.text_input("Cari Oshi...", key=search_key, placeholder="Ketik nama...")
    
    # Real-time search dari session state
    query = st.session_state.get(search_key, "").lower().strip()
    
    data = get_data(url)
    if not data:
        st.info("Menghubungkan ke API...")
        return

    for sesi in data.get('data', []):
        members = sesi.get('session_members', [])
        if query:
            members = [m for m in members if query in m.get('member_name', '').lower()]
        
        if not members: continue

        st.markdown(f"#### {sesi['label']} <small style='opacity:0.5'>| {sesi['start_time'][:5]}-{sesi['end_time'][:5]}</small>", unsafe_allow_html=True)
        
        html = '<div class="cards-grid">'
        for m in members:
            q = m.get('quota', 0)
            cls, lbl = get_status_info(q, ev_type)
            html += f'<div class="ldp-card {cls}"><div class="c-jalur">{m["label"]}</div><div class="c-member">{m["member_name"]}</div><div class="c-badge">{lbl}</div></div>'
        html += '</div>'
        st.markdown(html.replace('\n', ''), unsafe_allow_html=True)
        st.write("")

# --- 7. TABS ---
t1, t2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])
with t1: draw_ui(URL_2SHOT, "2s", "2shot")
with t2: draw_ui(URL_MNG, "mng", "mng")
