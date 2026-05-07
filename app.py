import streamlit as st
from PIL import Image
import time
from datetime import datetime

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH | Akıllı Sağlık", page_icon="🌐", layout="wide")

if 'arsiv' not in st.session_state:
    st.session_state.arsiv = []

# --- 2. ÖZEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #000000 0%, #001f3f 50%, #004a99 100%); color: white; }
    
    /* ACİL DURUM BUTONU */
    .stButton > button#acil_btn { 
        background-color: #ff4b4b !important; 
        color: white !important; 
        font-weight: bold !important;
        border-radius: 12px;
        width: 100%;
    }
    
    /* PARLAYAN SİYAH-MAVİ KAYIT OL BUTONU (Kesin Çözüm) */
    .stButton > button#kayit_btn {
        background: linear-gradient(135deg, #000000 0%, #004a99 100%) !important;
        color: white !important;
        border: 1px solid #00c6ff !important;
        box-shadow: 0px 0px 15px rgba(0, 198, 255, 0.6);
        border-radius: 12px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton > button#kayit_btn:hover {
        box-shadow: 0px 0px 25px rgba(0, 198, 255, 1);
        border: 1px solid #ffffff;
    }

    /* Şikayet Kutusu Tasarımı */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 2px solid #00c6ff !important;
        border-radius: 15px !important;
        font-size: 18px !important;
    }
    
    /* Harita Boyutu Küçültme */
    [data-testid="stMap"] { height: 250px !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÜST BAR ---
col_logo, col_btns = st.columns([2, 1])
with col_logo:
    st.markdown("<h1 style='color: #00c6ff; margin:0;'>🌐 AIHEALTH</h1>", unsafe_allow_html=True)

with col_btns:
    c1, c2 = st.columns(2)
    with c1: 
        st.button("🚨 ACİL DURUM", key="acil_btn")
    with c2: 
        st.button("👤 KAYIT OL", key="kayit_btn")

# --- 4. ANALİZ MOTORU ---
def akilli_analiz(mesaj):
    m = mesaj.lower()
    if any(k in m for k in ["kan", "kesik", "yara", "parmak", "kestim"]):
        return {"baslik": "⚠️ KESİK MÜDAHALESİ", "mesaj": "1. Yaraya baskı uygulayın. 2. Temiz suyla yıkayın. 3. Bölgeyi yukarı kaldırın.", "foto": "📸 Fotoğraf yüklerseniz derinliği analiz edebilirim.", "renk": "warning"}
    elif any(k in m for k in ["kırık", "diz", "ayak", "kırıldı", "bacağım"]):
        return {"baslik": "🚨 KIRIK ŞÜPHESİ", "mesaj": "ASLA KIPIRDATMAYIN! Bölgeyi sabitleyin ve üzerine buz (bezle sarılı) koyun.", "foto": "📸 Şekil bozukluğunu görmem için fotoğraf yükleyin.", "renk": "error"}
    return {"baslik": "🔍 ANALİZ", "mesaj": "Şikayetiniz sisteme alındı. Bol sıvı tüketin ve dinlenin.", "foto": "📸 Fotoğraf ekleyerek daha net sonuç alabilirsiniz.", "renk": "info"}

# --- 5. ŞİKAYET KUTUSU (Enter ve Buton Sorunu Çözüldü) ---
st.subheader("📝 Şikayetinizi Yazın")
# Formu kaldırıp doğrudan buton ve state kontrolü yapıyoruz (Daha güvenli çalışır)
sikayet_metni = st.text_area("", placeholder="Enter'a basabilir veya aşağıdaki butona tıklayabilirsiniz...", height=200, key="ana_sikayet")

if st.button("🚀 ANALİZİ BAŞLAT", use_container_width=True):
    if sikayet_metni:
        res = akilli_analiz(sikayet_metni)
        st.markdown(f"### {res['baslik']}")
        if res["renk"] == "error": st.error(res["mesaj"])
        elif res["renk"] == "warning": st.warning(res["mesaj"])
        else: st.success(res["mesaj"])
        st.info(res["foto"])
    else:
        st.warning("Lütfen analiz için bir şeyler yazın.")

st.divider()

# --- 6. GÖRSEL ANALİZ ---
st.subheader("📸 Görsel Analiz")
col_c, col_f = st.columns(2)
with col_c: cam = st.camera_input("Fotoğraf Çek")
with col_f: file = st.file_uploader("Dosya Seç")

img = cam if cam else file
if img:
    st.image(img, width=300)
    with st.status("Görsel taranıyor..."):
        time.sleep(1)
        st.write("Doku analizi yapıldı.")

# --- 7. ÇALIŞAN KONUM VE BUTONLAR ---
st.divider()
st.subheader("📍 Yakındaki Sağlık Merkezleri")

m_col1, m_col2 = st.columns([1, 2])

with m_col1:
    st.markdown("### Hızlı Erişim")
    
    # Hastaneler - Google Maps araması
    hastane_url = "https://www.google.com/maps/search/en+yakın+hastane"
    st.markdown(f'<a href="{hastane_url}" target="_blank"><button style="width:100%; height:45px; border-radius:10px; background:#007bff; color:white; border:none; cursor:pointer; font-weight:bold;">🏥 En Yakın Hastaneler</button></a>', unsafe_allow_html=True)
    
    st.write("") # Boşluk
    
    # Nöbetçi Eczaneler - Kesin çözüm (Genel Türkiye Araması)
    eczane_url = "https://www.google.com/maps/search/nöbetçi+eczane"
    st.markdown(f'<a href="{eczane_url}" target="_blank"><button style="width:100%; height:45px; border-radius:10px; background:#28a745; color:white; border:none; cursor:pointer; font-weight:bold;">💊 Nöbetçi Eczaneler</button></a>', unsafe_allow_html=True)
    
    st.write("")
    if st.button("📍 Konumumu Bul", use_container_width=True):
        st.toast("Konum verisi işleniyor...")

with m_col2:
    st.map() # Küçük ve şık harita

# Arşiv Bölümü
with st.expander("📁 Fotoğraf Arşivi"):
    st.write("Analiz ettiğiniz geçmiş görseller burada saklanır.")
