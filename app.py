import streamlit as st
import requests

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Stok JKT48", layout="wide")

# Styling dasar Streamlit (Menyembunyikan padding berlebih)
st.markdown("""
    <style>
    .title-text { font-weight: 700; margin-bottom: -10px; font-family: 'Helvetica Neue', sans-serif;}
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid rgba(150,150,150,0.2); }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border: none; padding: 10px 5px;}
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #E52B38; color: #E52B38; font-weight: 600;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<h2 class="title-text">Dashboard Ketersediaan Tiket</h2>', unsafe_allow_html=True)
st.caption("Update real-time ketersediaan slot member")
st.divider()

# --- URL ENDPOINT ---
URL_2SHOT = "https://jkt48.com/api/v1/exclusives/EX579E/bonus?lang=id"
URL_MNG = "https://jkt48.com/api/v1/exclusives/EXE588/bonus?lang=id"

# --- FUNGSI TARIK DATA API ---
@st.cache_data(ttl=60)
def fetch_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return None

# --- FUNGSI RENDER UI MINIMALIST MODERN ---
def render_minimalist_cards(data, search_query=""):
    if not data or data.get('status') is not True:
        st.warning("Data tidak valid atau sedang ditarik dari API.")
        return
    
    try:
        items = data.get('data', []) 
        
        # CSS Khusus Minimalist Modern Card
        st.markdown("""
            <style>
            .m-sesi { margin-bottom: 40px; font-family: 'Inter', 'Helvetica Neue', sans-serif;}
            .m-wrapper { display: flex; flex-wrap: wrap; gap: 16px; }
            
            /* Desain Card Utama */
            .m-card {
                border: 1px solid rgba(150, 150, 150, 0.2);
                border-radius: 8px; 
                padding: 16px; 
                width: 170px;
                display: flex; 
                flex-direction: column; 
                justify-content: space-between;
                background-color: transparent;
                transition: transform 0.2s ease, border-color 0.2s ease;
            }
            .m-card:hover { border-color: rgba(150, 150, 150, 0.6); transform: translateY(-3px); }
            
            /* Status Indicators */
            .m-card.avail { border-bottom: 3px solid #10B981; } /* Hijau elegan */
            .m-card.sold { border-bottom: 3px solid rgba(150, 150, 150, 0.4); opacity: 0.6; filter: grayscale(100%); }
            
            /* Typography */
            .m-jalur { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.6; margin-bottom: 6px; }
            .m-member { font-weight: 600; font-size: 15px; margin-bottom: 16px; line-height: 1.3; }
            
            /* Badge Status Minimalis */
            .m-stock-badge {
                align-self: flex-start;
                font-size: 11px;
                font-weight: 600;
                padding: 4px 10px;
                border-radius: 12px;
                letter-spacing: 0.5px;
            }
            .m-card.avail .m-stock-badge { background-color: rgba(16, 185, 129, 0.1); color: #10B981; }
            .m-card.sold .m-stock-badge { background-color: rgba(150, 150, 150, 0.15); color: inherit; opacity: 0.8; }
            </style>
        """, unsafe_allow_html=True)

        ada_hasil_pencarian = False

        for sesi in items:
            nama_sesi = sesi.get('label', 'Sesi ?')
            waktu_mulai = sesi.get('start_time', '')
            waktu_selesai = sesi.get('end_time', '')
            members = sesi.get('session_members', [])
            
            if search_query:
                members = [m for m in members if search_query.lower() in m.get('member_name', '').lower()]
            
            if not members:
                continue
                
            ada_hasil_pencarian = True

            # Header sesi yang lebih clean
            st.markdown(f"#### {nama_sesi} <span style='font-weight:400; font-size:16px; opacity:0.6;'>&nbsp; | &nbsp; {waktu_mulai[:5]} - {waktu_selesai[:5]}</span>", unsafe_allow_html=True)
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            
            html_cards = '<div class="m-sesi"><div class="m-wrapper">'
            
            for member in members:
                nama_member = member.get('member_name', '')
                jalur = member.get('label', '')
                kuota = member.get('quota', 0)
                
                if kuota > 0:
                    c_class = "avail"
                    s_text = f"{kuota} TERSISA"
                else:
                    c_class = "sold"
                    s_text = "SOLD OUT"
                
                # RAHASIA FIX: Tetap ditulis 1 baris agar tidak dirusak Streamlit Markdown
                html_cards += f'<div class="m-card {c_class}"><div><div class="m-jalur">{jalur}</div><div class="m-member">{nama_member}</div></div><div class="m-stock-badge">{s_text}</div></div>'
            
            html_cards += '</div></div>'
            
            st.markdown(html_cards, unsafe_allow_html=True)

        if not ada_hasil_pencarian:
            st.info("Tidak ada member yang cocok dengan pencarian.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses UI: {e}")


# --- LAYOUTING UI DENGAN TABS (KODE EX DIHILANGKAN) ---
tab1, tab2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])

with tab1:
    search_2s = st.text_input("🔍 Cari Member", key="search_2s", placeholder="Ketik nama member...")
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner('Memuat data 2-Shot...'):
        data_2s = fetch_data(URL_2SHOT)
        render_minimalist_cards(data_2s, search_2s)

with tab2:
    search_mng = st.text_input("🔍 Cari Member", key="search_mng", placeholder="Ketik nama member...")
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner('Memuat data Meet & Greet...'):
        data_mng = fetch_data(URL_MNG)
        render_minimalist_cards(data_mng, search_mng)

# --- KONTROL MANUAL REFRESH ---
st.divider()
if st.button("🔄 Segarkan Data Sekarang", use_container_width=True):
    st.cache_data.clear()
    st.rerun()