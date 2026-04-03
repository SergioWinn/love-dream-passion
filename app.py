import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Stok JKT48", layout="wide")

st_autorefresh(interval=2000, key="jkt48_refresh")

# Styling dasar Streamlit
st.markdown("""
    <style>
    .title-text { font-weight: 700; margin-bottom: -10px; font-family: 'Helvetica Neue', sans-serif;}
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid rgba(150,150,150,0.2); }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border: none; padding: 10px 5px;}
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #E52B38; color: #E52B38; font-weight: 600;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<h2 class="title-text">Dashboard Ketersediaan Tiket</h2>', unsafe_allow_html=True)
st.caption("Auto-refresh aktif: Setiap 5 detik")
st.divider()

# --- URL ENDPOINT ---
URL_2SHOT = "https://jkt48.com/api/v1/exclusives/EX579E/bonus?lang=id"
URL_MNG = "https://jkt48.com/api/v1/exclusives/EXE588/bonus?lang=id"

# --- FUNGSI TARIK DATA API ---
# TTL kita turunkan agar cache cepat basi dan data selalu segar
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
        st.warning("Menunggu data terbaru...")
        return
    
    try:
        items = data.get('data', []) 
        
        st.markdown("""
            <style>
            .m-sesi { margin-bottom: 40px; font-family: 'Inter', 'Helvetica Neue', sans-serif;}
            .m-wrapper { display: flex; flex-wrap: wrap; gap: 16px; }
            .m-card {
                border: 1px solid rgba(150, 150, 150, 0.2);
                border-radius: 8px; 
                padding: 16px; 
                width: 170px;
                display: flex; 
                flex-direction: column; 
                justify-content: space-between;
                background-color: transparent;
            }
            .m-card.avail { border-bottom: 3px solid #10B981; }
            .m-card.sold { border-bottom: 3px solid rgba(150, 150, 150, 0.4); opacity: 0.6; filter: grayscale(100%); }
            .m-jalur { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.6; margin-bottom: 6px; }
            .m-member { font-weight: 600; font-size: 15px; margin-bottom: 16px; line-height: 1.3; }
            .m-stock-badge {
                align-self: flex-start;
                font-size: 11px;
                font-weight: 600;
                padding: 4px 10px;
                border-radius: 12px;
            }
            .m-card.avail .m-stock-badge { background-color: rgba(16, 185, 129, 0.1); color: #10B981; }
            .m-card.sold .m-stock-badge { background-color: rgba(150, 150, 150, 0.15); color: inherit; }
            </style>
        """, unsafe_allow_html=True)

        for sesi in items:
            nama_sesi = sesi.get('label', 'Sesi ?')
            waktu = f"{sesi.get('start_time', '')[:5]} - {sesi.get('end_time', '')[:5]}"
            members = sesi.get('session_members', [])
            
            if search_query:
                members = [m for m in members if search_query.lower() in m.get('member_name', '').lower()]
            
            if not members: continue

            st.markdown(f"#### {nama_sesi} <span style='font-weight:400; font-size:16px; opacity:0.6;'>&nbsp; | &nbsp; {waktu}</span>", unsafe_allow_html=True)
            
            html_cards = '<div class="m-sesi"><div class="m-wrapper">'
            for m in members:
                c_class = "avail" if m.get('quota', 0) > 0 else "sold"
                s_text = f"{m.get('quota', 0)} TERSISA" if c_class == "avail" else "SOLD OUT"
                html_cards += f'<div class="m-card {c_class}"><div><div class="m-jalur">{m.get("label", "")}</div><div class="m-member">{m.get("member_name", "")}</div></div><div class="m-stock-badge">{s_text}</div></div>'
            html_cards += '</div></div>'
            st.markdown(html_cards, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")

# --- TABS ---
tab1, tab2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])

with tab1:
    search_2s = st.text_input("🔍 Cari Member", key="search_2s", placeholder="Cari nama...")
    render_minimalist_cards(fetch_data(URL_2SHOT), search_2s)

with tab2:
    search_mng = st.text_input("🔍 Cari Member", key="search_mng", placeholder="Cari nama...")
    render_minimalist_cards(fetch_data(URL_MNG), search_mng)
