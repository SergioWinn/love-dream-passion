import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LOVE DREAM PASSION", layout="wide", page_icon="🔴")

# Auto-refresh 1 detik
st_autorefresh(interval=1000, key="ldp_refresh_global")

# --- 2. UI/UX STYLING (MODERN, ADAPTIVE, NO-SORT) ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }

/* Header Center */
.ldp-header { text-align: center; margin-bottom: 30px; border-bottom: 1px solid rgba(128,128,128,0.2); padding-bottom: 20px; }
.ldp-title { font-weight: 800; font-size: 2.2rem; margin: 0; margin-bottom: 10px; }
.live-badge { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; font-size: 12px; color: #10B981; background: rgba(16,185,129,0.1); padding: 5px 12px; border-radius: 20px; }
.live-dot { height: 8px; width: 8px; background: #10B981; border-radius: 50%; animation: pulse_dot 2s infinite; }
@keyframes pulse_dot { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

/* Grid System */
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 15px; justify-content: center; }

/* Modern Card */
.ldp-card { background: rgba(128,128,128,0.05); border-radius: 12px; padding: 20px; border: 1px solid rgba(128,128,128,0.2); display: flex; flex-direction: column; justify-content: space-between; transition: 0.3s; height: 100%; text-align: center; }
.ldp-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }

/* Status Colors */
.ldp-card.avail { border-bottom: 4px solid #10B981; }
.ldp-card.warn { border-bottom: 4px solid #FBBF24; animation: card_pulse 2s infinite; }
.ldp-card.sold { border-bottom: 4px solid #EF4444; opacity: 0.6; filter: grayscale(100%); }

@keyframes card_pulse { 0% { box-shadow: 0 0 0 0 rgba(251,191,36,0.4); } 70% { box-shadow: 0 0 0 10px rgba(251,191,36,0); } 100% { box-shadow: 0 0 0 0 rgba(251,191,36,0); } }

.c-jalur { font-size: 10px; opacity: 0.6; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; }
.c-member { font-weight: 700; font-size: 15px; line-height: 1.2; margin-bottom: 15px; height: 2.4em; overflow: hidden; }

.c-badge { font-size: 9px; font-weight: 800; padding: 5px; border-radius: 15px; text-transform: uppercase; width: 100%; display: block; }
.ldp-card.avail .c-badge { background: rgba(16,185,129,0.15); color: #10B981; }
.ldp-card.warn .c-badge { background: rgba(251,191,36,0.2); color: #D97706; }
.ldp-card.sold .c-badge { background: rgba(239,68,68,0.15); color: #EF4444; }

@media (max-width: 500px) { .cards-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; } .ldp-card { padding: 15px 10px; } }
</style>
"""
st.markdown(css.replace('\n', ''), unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown('<div class="ldp-header"><h1 class="ldp-title">Meet & Greet - 23 May</h1><div class="live-badge"><span class="live-dot"></span> LIVE MONITORING</div></div>', unsafe_allow_html=True)

# --- 4. LOGIKA DATA ---
URL_2SHOT = "https://jkt48.com/api/v1/exclusives/EX579E/bonus?lang=id"
URL_MNG = "https://jkt48.com/api/v1/exclusives/EXE588/bonus?lang=id"

@st.cache_data(ttl=4)
def get_data(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

def get_status(quota, ev_type):
    if quota <= 0: return "sold", "HABIS"
    limit = 5 if ev_type == "2shot" else 20
    if quota < limit: return "warn", f"HAMPIR HABIS ({quota})"
    return "avail", f"SISA {quota}"

# --- 5. RENDER ENGINE ---
def draw_ui(url, key_prefix, ev_type):
    query = st.text_input("Cari Oshi...", key=f"search_{key_prefix}", placeholder="Ketik nama member...").lower().strip()
    
    data = get_data(url)
    if not data:
        st.info("Menghubungkan ke server JKT48...")
        return

    for sesi in data.get('data', []):
        members = sesi.get('session_members', [])
        
        if query:
            members = [m for m in members if query in m.get('member_name', '').lower()]
        
        if not members: continue

        # --- SORTING DIHAPUS ---
        # Data akan tampil sesuai urutan asli dari API JKT48

        st.markdown(f"#### {sesi['label']} <small style='opacity:0.5'>| {sesi['start_time'][:5]}-{sesi['end_time'][:5]}</small>", unsafe_allow_html=True)
        
        html = '<div class="cards-grid">'
        for m in members:
            q = m.get('quota', 0)
            cls, lbl = get_status(q, ev_type)
            html += f'<div class="ldp-card {cls}"><div class="c-jalur">{m["label"]}</div><div class="c-member">{m["member_name"]}</div><div class="c-badge">{lbl}</div></div>'
        html += '</div>'
        st.markdown(html.replace('\n', ''), unsafe_allow_html=True)
        st.write("")

# --- 6. TABS ---
t1, t2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])
with t1: draw_ui(URL_2SHOT, "2s", "2shot")
with t2: draw_ui(URL_MNG, "mng", "mng")
