import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LOVE DREAM PASSION", layout="wide", page_icon="🔴")

# --- 2. SILENT AUTO REFRESH (5 Detik) ---
st_autorefresh(interval=5000, key="ldp_autorefresh")

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
    .stTabs [data-baseweb="tab"] { height: 60px; background-color: transparent; border: none; padding: 10px 0px; font-size: 17px; color: #6b7280; font-weight: 400; }
    .stTabs [aria-selected="true"] { border-bottom: 4px solid #E52B38; color: #E52B38; font-weight: 700; }
    .sesi-section { margin-top: 30px; margin-bottom: 50px; }
    .sesi-header-wrapper { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
    .sesi-title { font-size: 1.5rem; font-weight: 700; color: #374151; margin: 0; }
    .sesi-time-badge { font-size: 14px; font-weight: 400; color: #6b7280; background: #f3f4f6; padding: 4px 10px; border-radius: 8px; }
    .cards-flex-container { display: flex; flex-wrap: wrap; gap: 18px; justify-content: flex-start; }
    .ldp-card { background-color: #ffffff; border-radius: 12px; padding: 22px; width: 185px; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid rgba(0,0,0,0.04); box-shadow: 0 2px 5px rgba(0,0,0,0.02); transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1); cursor: default; }
    .ldp-card:hover { box-shadow: 0 10px 20px rgba(0,0,0,0.06); transform: translateY(-5px); border-color: rgba(0,0,0,0.1); }
    .ldp-card.avail { border-bottom: 4px solid #10B981; }
    .ldp-card.sold { border-bottom: 4px solid #e5e7eb; background-color: #f9fafb; opacity: 0.7; }
    .card-jalur { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #9ca3af; margin-bottom: 5px; font-weight: 600; }
    .card-member { font-weight: 700; font-size: 16px; margin-bottom: 18px; line-height: 1.3; color: #111827; height: 2.6em; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
    .card-badge { align-self: flex-start; font-size: 11px; font-weight: 700; padding: 6px 12px; border-radius: 20px; letter-spacing: 0.3px; }
    .ldp-card.avail .card-badge { background-color: #ecfdf5; color: #059669; }
    .ldp-card.sold .card-badge { background-color: #f3f4f6; color: #9ca3af; }
    .stTextInput input { border-radius: 10px; border: 1px solid rgba(0,0,0,0.1); padding: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. RENDER HEADER ---
st.markdown("""
    <div class="ldp-main-header">
        <h1 class="ldp-title">Meet & Greet - 23 May</h1>
        <div class="live-badge-wrapper"><span class="live-dot"></span> LIVE</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. URL ENDPOINT & AMBIL DATA ---
URL_2SHOT = "https://jkt48.com/api/v1/exclusives/EX579E/bonus?lang=id"
URL_MNG = "https://jkt48.com/api/v1/exclusives/EXE588/bonus?lang=id"

@st.cache_data(ttl=5)
def fetch_jkt48_data(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) LDP Modern Monitor v1.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

# --- 6. FUNGSI RENDER UI MODERN CARDS ---
def render_modern_ldp_cards(data, search_query=""):
    if not data or data.get('status') is not True:
        st.info("Memperbarui data terbaru dari server JKT48...")
        return
    
    try:
        items = data.get('data', []) 
        ada_member_ditemukan = False

        for sesi in items:
            nama_sesi = sesi.get('label', 'Sesi')
            waktu = f"{sesi.get('start_time', '')[:5]} - {sesi.get('end_time', '')[:5]}"
            members = sesi.get('session_members', [])
            
            if search_query:
                query = search_query.lower().strip()
                members = [m for m in members if query in m.get('member_name', '').lower()]
            
            if not members: continue 
            ada_member_ditemukan = True

            st.markdown(f"""
                <div class="sesi-section">
                    <div class="sesi-header-wrapper">
                        <div class="sesi-title">{nama_sesi}</div>
                        <div class="sesi-time-badge">🕒 {waktu}</div>
                    </div>
                    <div class="cards-flex-container">
            """, unsafe_allow_html=True)
            
            html_cards_all = ""
            for m in members:
                c_class = "avail" if m.get('quota', 0) > 0 else "sold"
                s_text = f"SISA {m.get('quota', 0)}" if c_class == "avail" else "HABIS"
                m_name = m.get('member_name', '')
                jalur = m.get('label', '')
                
                html_cards_all += f'<div class="ldp-card {c_class}"><div><div class="card-jalur">{jalur}</div><div class="card-member" title="{m_name}">{m_name}</div></div><div class="card-badge">{s_text}</div></div>'
            
            st.markdown(f"{html_cards_all}</div></div>", unsafe_allow_html=True)

        if not ada_member_ditemukan and search_query:
            st.markdown(f"""
                <div style='text-align: center; padding: 50px 20px; color: #9ca3af; font-size: 15px; border-radius: 12px; background-color: #f9fafb; border: 1px solid rgba(0,0,0,0.03);'>
                    🔍 Maaf, Oshi "<b>{search_query}</b>" tidak ditemukan di event Meet & Greet ini.
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Terjadi kendala teknis saat menyusun tampilan: {e}")

# --- 7. MODERN TABS LAYOUT ---
tab1, tab2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])

with tab1:
    search_2shot = st.text_input("Cari member 2-Shot favoritmu...", key="s_2shot", placeholder="Ketik nama member kesayanganmu...")
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True) 
    data_2shot = fetch_jkt48_data(URL_2SHOT)
    render_modern_ldp_cards(data_2shot, search_2shot)

with tab2:
    search_mng = st.text_input("Cari member M&G favoritmu...", key="s_mng", placeholder="Ketik nama member kesayanganmu...")
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    data_mng = fetch_jkt48_data(URL_MNG)
    render_modern_ldp_cards(data_mng, search_mng)
