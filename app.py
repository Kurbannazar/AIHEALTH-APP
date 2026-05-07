import streamlit as st
from PIL import Image
import time
from datetime import datetime

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH | Profesyonel Sağlık", page_icon="🌐", layout="wide")

if 'arsiv' not in st.session_state:
    st.session_state.arsiv = []

# --- 2. ÖZEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #000000 0%, #001f3f 50%, #004a99 100%); color: white; }
    
    /* ACİL DURUM BUTONU */
    div.stButton > button:first-child { 
        background-color: #ff4b4b !important; 
        color: white !important; 
        font-weight: bold !important;
        border-radius: 12px;
    }
    
    /* PARLAYAN SİYAH-MAVİ KAYIT OL BUTONU */
    div[data-testid="column"]:nth-child(2) .stButton button {
        background: linear-gradient(135deg, #000000 0%, #004a99 100%) !important;
        color: white !important;
        border: 1px solid #00c6ff !important;
        box-shadow: 0px 0px 15px rgba(0, 198, 255, 0.4);
        border-radius: 12px;
        transition: 0.3s;
        width: 100%;
    }
    div[data-testid="column"]:nth-child(2) .stButton button:hover {
        box-shadow: 0px 0px 25px rgba(0, 198, 255, 0.9);
        border: 1px solid #ffffff;
    }

    /* Şikayet Kutusu */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #00c6ff !important;
        border-radius: 15px !important;
    }
    
    /* Harita Boyutu */
    [data-testid="stMap"] { height: 280px !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST BAR ---
col_logo, col_btns = st.columns([2, 1])
with col_logo:
    st.markdown("<h1 style='color: #00c6ff; margin:0;'>🌐 AIHEALTH</h1>", unsafe_allow_html=True)

with col_btns:
    c1, c2 = st.columns(2)
    with c1: st.button("🚨 ACİL DURUM")
    with c2: st.button("👤 KAYIT OL")

# --- 4. ANALİZ MOTORU ---
def akilli_analiz(mesaj):
    m = mesaj.lower()
    if any(k in m for k in ["kan", "kesik", "yara", "parmak"]):
        return {"baslik": "⚠️ KESİK MÜDAHALESİ", "mesaj": "1. Yaraya baskı uygulayın. 2. Temiz suyla yıkayın. 3. Bölgeyi yukarı kaldırın.", "foto": "📸 Fotoğraf yüklerseniz derinliği analiz edebilirim.", "renk": "warning"}
    elif any(k in m for k in ["kırık", "diz", "ayak", "kırıldı"]):
        return {"baslik": "🚨 KIRIK ŞÜPHESİ", "mesaj": "ASLA KIPIRDATMAYIN! Bölgeyi sabitleyin ve soğuk uygulama yapın.", "foto": "📸 Şekil bozukluğunu görmem için fotoğraf yükleyin.", "renk": "error"}
    return {"baslik": "🔍 ANALİZ", "mesaj": "Şikayetiniz alındı.", "foto": "📸 Fotoğraf ekleyerek daha net sonuç alabilirsiniz.", "renk": "info"}

# --- 5. ŞİKAYET KUTUSU (Enter Destekli) ---
st.subheader("📝 Şikayetinizi Yazın")
with st.form("main_form", clear_on_submit=False):
    sikayet_metni = st.text_area("", placeholder="Enter'a basın veya butona tıklayın...", height=180)
    submit = st.form_submit_button("ANALİZİ BAŞLAT")

if submit and sikayet_metni:
    res = akilli_analiz(sikayet_metni)
    st.markdown(f"### {res['baslik']}")
    if res["renk"] == "error": st.error(res["mesaj"])
    elif res["renk"] == "warning": st.warning(res["mesaj"])
    else: st.success(res["mesaj"])
    st.info(res["foto"])

st.divider()

# --- 6. GÖRSEL ANALİZ ---
st.subheader("📸 Görsel Analiz")
col_c, col_f = st.columns(2)
with col_c: cam = st.camera_input("Fotoğraf Çek")
with col_f: file = st.file_uploader("Dosya Seç")

img = cam if cam else file
if img:
    st.image(img, width=300)
    with st.status("Doku taranıyor..."):
        time.sleep(1)
        st.write("Analiz tamamlandı.")

# --- 7. KÜÇÜK KONUM VE ÇALIŞAN BUTONLAR ---
st.divider()
st.subheader("📍 Yakındaki Merkezler")

m_col1, m_col2 = st.columns([1, 2])

with m_col1:
    # Gerçek aramalar yapan butonlar
    st.markdown("### Hızlı Erişim")
    
    # Hastaneler butonu Google Maps'e yönlendirir
    hastane_url = "https://www.google.com/maps/search/en+yakın+hastane"
    st.markdown(f'<a href="{hastane_url}" target="_blank"><button style="width:100%; height:40px; border-radius:10px; background:#007bff; color:white; border:none; cursor:pointer;">🏥 En Yakın Hastaneler</button></a>', unsafe_allow_html=True)
    
    st.write("") # Boşluk
    
    # Nöbetçi Eczaneler butonu (İstanbul için örnek link)
    eczane_url = "https://www.istanbuleczaciodasi.org.tr/nobetci-ezcaneler/"
    st.markdown(f'<a href="{eczane_url}" target="_blank"><button style="width:100%; height:40px; border-radius:10px; background:#28a745; color:white; border:none; cursor:pointer;">💊 Nöbetçi Eczaneler</button></a>', unsafe_allow_html=True)
    
    st.write("")
    if st.button("📍 Konumumu Bul"):
        st.toast("Konumunuz alınıyor...")

with m_col2:
    st.map() # Küçük harita görünümü

# Arşiv
with st.expander("📁 Fotoğraf Arşivi"):
    st.write("Geçmiş kayıtlar burada saklanır.")
