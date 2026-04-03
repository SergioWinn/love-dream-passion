import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LOVE DREAM PASSION", layout="wide", page_icon="🔴")

# Silent refresh
st_autorefresh(interval=500, key="ldp_autorefresh")

# --- 2. UI/UX STYLING (MODERN, MINIMALIST, ADAPTIVE) ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }

.ldp-main-header { display: flex; align-items: center; justify-content: center; margin-bottom: 25px; border-bottom: 1px solid rgba(128,128,128,0.2); padding-bottom: 20px; flex-wrap: wrap; gap: 15px; text-align: center; }
.ldp-title { font-weight: 800; font-size: 2.2rem; margin: 0; line-height: 1.2; }

.live-badge-wrapper { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 13px; color: #10B981; background-color: rgba(16, 185, 129, 0.15); padding: 6px 14px; border-radius: 30px; border: 1px solid rgba(16, 185, 129, 0.3); }
.live-dot { height: 10px; width: 10px; background-color: #10B981; border-radius: 50%; display: inline-block; animation: ldp_pulse 2s infinite; }
@keyframes ldp_pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(1.1); } 100% { opacity: 1; transform: scale(1); } }

.stTabs [data-baseweb="tab-list"] { gap: 40px; justify-content: center; }
.stTabs [data-baseweb="tab"] { height: 60px; background-color: transparent; border: none; padding: 10px 0px; font-size: 17px; font-weight: 400; }
.stTabs [aria-selected="true"] { border-bottom: 4px solid #E52B38; color: #E52B38; font-weight: 700; }

.sesi-section { margin-top: 30px; margin-bottom: 50px; }
.sesi-header-wrapper { display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 25px; flex-wrap: wrap; }
.sesi-title { font-size: 1.5rem; font-weight: 700; margin: 0; }
.sesi-time-badge { font-size: 14px; font-weight: 600; opacity: 0.8; background: rgba(128,128,128,0.15); padding: 4px 12px; border-radius: 8px; }

/* GRID SYSTEM */
.cards-flex-container { display: grid; grid-template-columns: repeat(auto-fit, 185px); gap: 18px; justify-content: center; }

.ldp-card { background-color: rgba(128,128,128, 0.03); border-radius: 12px; padding: 22px; width: 100%; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid rgba(128,128,128,0.2); box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1); cursor: default; }
.ldp-card:hover { transform: translateY(-5px); border-color: rgba(128,128,128,0.4); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }

/* STATUS COLORS */
.ldp-card.avail { border-bottom: 4px solid #10B981; }
.ldp-card.warn { border-bottom: 4px solid #FBBF24; } /* Kuning Modern */
.ldp-card.sold { border-bottom: 4px solid rgba(128,128,128,0.3); background-color: rgba(128,128,128,0.08); opacity: 0.6; filter: grayscale(50%); }

.card-jalur { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.6; margin-bottom: 5px; font-weight: 600; }
.card-member { font-weight: 700; font-size: 16px; margin-bottom: 18px; line-height: 1.3; height: 2.6em; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }

.card-badge { align-self: center; font-size: 10px; font-weight: 800; padding: 6px 12px; border-radius: 20px; letter-spacing: 0.5px; width: 100%; text-align: center; text-transform: uppercase;}
.ldp-card.avail .card-badge { background-color: rgba(16, 185, 129, 0.15); color: #10B981; }
.ldp-card.warn .card-badge { background-color: rgba(251, 191, 36, 0.15); color: #D97706; }
.ldp-card.sold .card-badge { background-color: rgba(128,128,128,0.2); color: inherit; opacity: 0.8; }

.stTextInput input { border-radius: 10px; border: 1px solid rgba(128,128,128,0.3); padding: 12px; background: transparent; }
</style>
"""
st.markdown(css.replace('\n', '').replace('\r', ''), unsafe_allow_html=True)

# --- 3. RENDER HEADER ---
st.markdown('<div class="ldp-main-header"><h1 class="ldp-title">Meet & Greet - 23 May</h1><div class="live-badge-wrapper"><span class="live-dot"></span> LIVE</div></div>', unsafe_allow_html=True)

# --- 4. DATA FETCHING ---
URL_2SHOT = "https://jkt48.com/api/v1/exclusives/EX579E/bonus?lang=id"
URL_MNG = "https://jkt48.com/api/v1/exclusives/EXE588/bonus?lang=id"

@st.cache_data(ttl=5)
def fetch_jkt48_data(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except:
        return None

# --- 5. LOGIKA STATUS (3 INDIKATOR) ---
def get_status_logic(quota, event_type):
    if quota <= 0:
        return "sold", "HABIS"
    
    # Threshold berbeda sesuai request
    threshold = 5 if event_type == "2shot" else 20
    
    if quota < threshold:
        return "warn", f"HAMPIR HABIS ({quota})"
    
    return "avail", f"TERSEDIA ({quota})"

# --- 6. RENDER UI CARDS ---
def render_modern_ldp_cards(data, search_query="", event_type=""):
    if not data or data.get('status') is not True:
        st.info("Sinkronisasi data server...")
        return
    
    try:
        items = data.get('data', []) 
        found_any = False

        for sesi in items:
            nama_sesi = sesi.get('label', 'Sesi')
            waktu = f"{sesi.get('start_time', '')[:5]} - {sesi.get('end_time', '')[:5]}"
            members = sesi.get('session_members', [])
            
            if search_query:
                members = [m for m in members if search_query.lower() in m.get('member_name', '').lower()]
            
            if not members: continue 
            found_any = True

            full_html = f'<div class="sesi-section"><div class="sesi-header-wrapper"><div class="sesi-title">{nama_sesi}</div><div class="sesi-time-badge">🕒 {waktu}</div></div><div class="cards-flex-container">'
            
            for m in members:
                quota = m.get('quota', 0)
                status_class, status_label = get_status_logic(quota, event_type)
                m_name = m.get('member_name', '')
                jalur = m.get('label', '')
                
                full_html += f'<div class="ldp-card {status_class}"><div style="text-align: center;"><div class="card-jalur">{jalur}</div><div class="card-member">{m_name}</div></div><div class="card-badge">{status_label}</div></div>'
            
            full_html += "</div></div>"
            st.markdown(full_html.replace('\n', '').replace('\r', ''), unsafe_allow_html=True)

        if not found_any and search_query:
            st.markdown(f"<div style='text-align: center; padding: 50px 20px; font-size: 15px; border-radius: 12px; background-color: rgba(128,128,128,0.05); border: 1px solid rgba(128,128,128,0.1); margin-top: 20px;'>🔍 Oshi '<b>{search_query}</b>' tidak ditemukan di jadwal ini.</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"UI Render Error: {e}")

# --- 7. TABS ---
tab1, tab2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])

with tab1:
    s1 = st.text_input("Cari member 2-Shot...", key="s1", placeholder="Ketik nama...")
    render_modern_ldp_cards(fetch_jkt48_data(URL_2SHOT), s1, "2shot")

with tab2:
    s2 = st.text_input("Cari member Meet & Greet...", key="s2", placeholder="Ketik nama...")
    render_modern_ldp_cards(fetch_jkt48_data(URL_MNG), s2, "mng")
