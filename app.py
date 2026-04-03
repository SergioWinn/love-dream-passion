import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LOVE DREAM PASSION", layout="wide")

# Silently refresh every 1 seconds
st_autorefresh(interval=1000, key="jkt48_refresh")

# --- UI/UX STYLING MODERN ---
st.markdown("""
    <style>
    /* Sembunyikan padding atas bawaan Streamlit agar seperti Web App asli */
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* Header & Live Badge */
    .header-wrapper { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; border-bottom: 1px solid rgba(150,150,150,0.1); padding-bottom: 15px;}
    .title-text { font-weight: 800; font-family: 'Inter', 'Helvetica Neue', sans-serif; margin: 0; font-size: 28px; color: #1f2937;}
    .live-badge { 
        background-color: rgba(16, 185, 129, 0.1); 
        color: #10B981; 
        font-size: 12px; 
        font-weight: 700; 
        padding: 4px 10px; 
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        animation: pulse 2s infinite;
    }
    .live-dot { height: 8px; width: 8px; background-color: #10B981; border-radius: 50%; display: inline-block; }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }

    /* Styling Tabs yang lebih bersih */
    .stTabs [data-baseweb="tab-list"] { gap: 30px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border: none; padding: 10px 0px; font-size: 16px;}
    .stTabs [aria-selected="true"] { border-bottom: 3px solid #E52B38; color: #E52B38; font-weight: 700;}
    </style>
""", unsafe_allow_html=True)

# Render Header with Live Badge
st.markdown("""
    <div class="header-wrapper">
        <h2 class="title-text">Ketersediaan Tiket</h2>
        <div class="live-badge"><span class="live-dot"></span> LIVE</div>
    </div>
""", unsafe_allow_html=True)

# --- URL ENDPOINT ---
URL_2SHOT = "https://jkt48.com/api/v1/exclusives/EX579E/bonus?lang=id"
URL_MNG = "https://jkt48.com/api/v1/exclusives/EXE588/bonus?lang=id"

# --- FUNGSI TARIK DATA API ---
@st.cache_data(ttl=5) 
def fetch_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

# --- FUNGSI RENDER UI MINIMALIST ---
def render_minimalist_cards(data, search_query=""):
    if not data or data.get('status') is not True:
        st.info("Memuat data terbaru dari server...")
        return
    
    try:
        items = data.get('data', []) 
        
        st.markdown("""
            <style>
            .m-sesi { margin-bottom: 45px; font-family: 'Inter', 'Helvetica Neue', sans-serif;}
            .m-sesi-title { font-size: 18px; font-weight: 600; margin-bottom: 15px; color: #374151; display: flex; align-items: center; gap: 10px;}
            .m-sesi-time { font-size: 14px; font-weight: 400; color: #9ca3af; background: #f3f4f6; padding: 2px 8px; border-radius: 6px;}
            .m-wrapper { display: flex; flex-wrap: wrap; gap: 16px; }
            
            /* Enhanced Card Design */
            .m-card {
                border: 1px solid rgba(0, 0, 0, 0.05);
                border-radius: 12px; 
                padding: 18px; 
                width: 175px;
                display: flex; 
                flex-direction: column; 
                justify-content: space-between;
                background-color: #ffffff;
                box-shadow: 0 2px 8px rgba(0,0,0,0.02);
                transition: all 0.2s ease;
            }
            .m-card:hover { box-shadow: 0 8px 16px rgba(0,0,0,0.06); transform: translateY(-3px); }
            
            .m-card.avail { border-bottom: 4px solid #10B981; }
            .m-card.sold { border-bottom: 4px solid #e5e7eb; background-color: #f9fafb; opacity: 0.7;}
            
            .m-jalur { font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #6b7280; margin-bottom: 4px; }
            .m-member { font-weight: 700; font-size: 15px; margin-bottom: 16px; line-height: 1.3; color: #111827;}
            
            .m-stock-badge { align-self: flex-start; font-size: 11px; font-weight: 700; padding: 5px 10px; border-radius: 20px; }
            .m-card.avail .m-stock-badge { background-color: #ecfdf5; color: #059669; }
            .m-card.sold .m-stock-badge { background-color: #f3f4f6; color: #9ca3af; }
            </style>
        """, unsafe_allow_html=True)

        for sesi in items:
            nama_sesi = sesi.get('label', 'Sesi ?')
            waktu = f"{sesi.get('start_time', '')[:5]} - {sesi.get('end_time', '')[:5]}"
            members = sesi.get('session_members', [])
            
            if search_query:
                members = [m for m in members if search_query.lower() in m.get('member_name', '').lower()]
            
            if not members: continue

            # Modern Section Header
            st.markdown(f"<div class='m-sesi-title'>{nama_sesi} <span class='m-sesi-time'>🕒 {waktu}</span></div>", unsafe_allow_html=True)
            
            html_cards = '<div class="m-sesi"><div class="m-wrapper">'
            for m in members:
                c_class = "avail" if m.get('quota', 0) > 0 else "sold"
                s_text = f"{m.get('quota', 0)} TERSISA" if c_class == "avail" else "HABIS"
                # RAHASIA FIX: 1 baris string panjang untuk menghindari bug parser Markdown Streamlit
                html_cards += f'<div class="m-card {c_class}"><div><div class="m-jalur">{m.get("label", "")}</div><div class="m-member">{m.get("member_name", "")}</div></div><div class="m-stock-badge">{s_text}</div></div>'
            html_cards += '</div></div>'
            
            st.markdown(html_cards, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Terjadi kendala memproses data UI: {e}")

# --- TABS ---
tab1, tab2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])

with tab1:
    search_2s = st.text_input("Cari member favoritmu...", key="search_2s", placeholder="Ketik nama member di sini...")
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True) # Tambah ruang nafas
    render_minimalist_cards(fetch_data(URL_2SHOT), search_2s)

with tab2:
    search_mng = st.text_input("Cari member favoritmu...", key="search_mng", placeholder="Ketik nama member di sini...")
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    render_minimalist_cards(fetch_data(URL_MNG), search_mng)
