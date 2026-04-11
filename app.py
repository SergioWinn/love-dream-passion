import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LOVE DREAM PASSION", layout="wide", page_icon="🔴")

# --- 2. STABLE REFRESH (5 Detik) ---
st_autorefresh(interval=5000, key="ldp_stable_refresh")

# --- INISIALISASI SESSION STATE UNTUK TRACKING KUOTA ---
if "quota_history" not in st.session_state:
    st.session_state.quota_history = {}

# --- FUNGSI NOTIFIKASI TELEGRAM ---
def send_telegram_alert(message):
    try:
        # Mengambil token dan ID dari brankas rahasia Streamlit Cloud
        bot_token = st.secrets["TELEGRAM_BOT_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        # Jika st.secrets belum diatur, lewati tanpa membuat error di layar
        pass

# --- 3. PREMIUM UI STYLING ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }

/* Header & Badge */
.ldp-header { text-align: center; margin-bottom: 30px; border-bottom: 1px solid rgba(128,128,128,0.2); padding-bottom: 20px; }
.ldp-title { font-weight: 800; font-size: 2.5rem; margin: 0; margin-bottom: 10px; }
.live-badge { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; font-size: 12px; color: #10B981; background: rgba(16,185,129,0.1); padding: 5px 15px; border-radius: 30px; border: 1px solid rgba(16,185,129,0.2); }
.live-dot { height: 8px; width: 8px; background: #10B981; border-radius: 50%; animation: blink 2s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.3; transform: scale(1.2); } }

/* Grid System */
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; justify-content: center; }

/* Card Design */
.ldp-card { 
    background: rgba(128,128,128,0.05); 
    border-radius: 15px; 
    padding: 24px 15px; 
    border: 1px solid rgba(128,128,128,0.15); 
    display: flex; 
    flex-direction: column; 
    justify-content: space-between; 
    text-align: center; 
    transition: 0.3s ease;
}
.ldp-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-color: rgba(128,128,128,0.3); }

/* Border Status */
.ldp-card.avail { border-bottom: 5px solid #10B981; }
.ldp-card.warn { border-bottom: 5px solid #FBBF24; animation: glow 2s infinite; }
.ldp-card.sold { border-bottom: 5px solid #EF4444; opacity: 0.7; filter: grayscale(30%); }

@keyframes glow { 0% { box-shadow: 0 0 5px rgba(251,191,36,0.1); } 50% { box-shadow: 0 0 15px rgba(251,191,36,0.3); } 100% { box-shadow: 0 0 5px rgba(251,191,36,0.1); } }

.c-jalur { font-size: 10px; opacity: 0.5; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px; }
.c-member { font-weight: 700; font-size: 16px; line-height: 1.2; margin-bottom: 20px; height: 2.5em; overflow: hidden; }

.c-badge { font-size: 10px; font-weight: 800; padding: 7px; border-radius: 20px; text-transform: uppercase; width: 100%; display: block; }
.ldp-card.avail .c-badge { background: rgba(16,185,129,0.15); color: #10B981; }
.ldp-card.warn .c-badge { background: rgba(251,191,36,0.2); color: #D97706; }
.ldp-card.sold .c-badge { background: #EF4444; color: #fff; }

/* Mobile optimization */
@media (max-width: 500px) { 
    .cards-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; } 
    .ldp-card { padding: 18px 10px; }
    .c-member { font-size: 14px; }
}
</style>
"""
st.markdown(css.replace('\n', '').replace('\r', ''), unsafe_allow_html=True)

# --- 4. RENDER HEADER ---
st.markdown('<div class="ldp-header"><h1 class="ldp-title">Meet & Greet - 23 May</h1><div class="live-badge"><span class="live-dot"></span> MONITORING LIVE</div></div>', unsafe_allow_html=True)

# ===== TAMBAHKAN KODE INI UNTUK TESTING =====
if st.button("🧪 Test Notifikasi Telegram"):
    send_telegram_alert("✅ <b>TESTING BERHASIL!</b>\nBot Restock LDP sudah berhasil terhubung.")
    st.success("Pesan test sedang dikirim ke Telegram!")
# ============================================

# --- 5. DATA ENGINE ---
@st.cache_data(ttl=4)
def fetch_data(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def draw_section(url, key_prefix, ev_type):
    s_key = f"input_{key_prefix}"
    st.text_input("Cari Oshi...", key=s_key, placeholder="Ketik nama member...")
    query = st.session_state.get(s_key, "").lower().strip()
    
    data = fetch_data(url)
    if not data:
        st.info("Menunggu data terbaru dari server JKT48...")
        return

    for sesi in data.get('data', []):
        members = sesi.get('session_members', [])
        if query:
            members = [m for m in members if query in m.get('member_name', '').lower()]
        
        if not members: continue

        st.markdown(f"#### {sesi['label']} <small style='opacity:0.5'>| {sesi['start_time'][:5]}-{sesi['end_time'][:5]}</small>", unsafe_allow_html=True)
        
        html = '<div class="cards-grid">'
        for m in members:
            current_quota = m.get('quota', 0)
            limit = 5 if ev_type == "2shot" else 20
            
            # --- CEK RESTOCK TIKET ---
            ticket_key = f"{ev_type}_{sesi['label']}_{m['member_name']}_{m['label']}"
            
            if ticket_key in st.session_state.quota_history:
                prev_quota = st.session_state.quota_history[ticket_key]
                if current_quota > prev_quota:
                    # Notifikasi Streamlit Toast
                    st.toast(f"RESTOCK: {m['member_name']} ({m['label']}) - Sesi {sesi['label']} (Kuota: {current_quota})", icon="🚨")
                    # Notifikasi Telegram
                    alert_msg = f"🚨 <b>RESTOCK ALERT!</b>\nOshi: <b>{m['member_name']}</b>\nJalur: {m['label']}\nSesi: {sesi['label']}\nKuota Nambah: {prev_quota} ➡️ {current_quota}"
                    send_telegram_alert(alert_msg)
                    
            # Simpan kuota saat ini untuk perbandingan di refresh berikutnya
            st.session_state.quota_history[ticket_key] = current_quota
            # --------------------------
            
            if current_quota <= 0: cls, lbl = "sold", "HABIS"
            elif current_quota < limit: cls, lbl = "warn", f"SISA {current_quota}"
            else: cls, lbl = "avail", f"SISA {current_quota}"
            
            html += f'<div class="ldp-card {cls}"><div class="c-jalur">{m["label"]}</div><div class="c-member">{m["member_name"]}</div><div class="c-badge">{lbl}</div></div>'
        
        st.markdown(html + '</div>', unsafe_allow_html=True)
        st.write("")

# --- 6. TABS ---
t1, t2 = st.tabs(["📸 2-Shot", "🤝 Meet & Greet"])
with t1:
    draw_section("https://jkt48.com/api/v1/exclusives/EX579E/bonus?lang=id", "2s", "2shot")
with t2:
    draw_section("https://jkt48.com/api/v1/exclusives/EXE588/bonus?lang=id", "mng", "mng")
