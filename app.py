
import streamlit as st
from PIL import Image
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH | Akıllı Sağlık Asistanı", page_icon="🌐", layout="wide")

# --- KRİTİK TASARIM (CSS) ---
# Sunumdaki parlak siyah-mavi geçişini ve modern butonları buraya işledim.
st.markdown("""
    <style>
    /* Arka Plan: Siyah'tan Maviye Parlak Geçiş */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #001f3f 50%, #004a99 100%);
        color: #ffffff;
    }
    
    /* Başlık Alanı */
    .main-title {
        font-family: 'Urbanist', sans-serif;
        font-size: 50px;
        font-weight: 800;
        text-align: center;
        color: #00c6ff;
        text-shadow: 0px 0px 15px rgba(0, 198, 255, 0.5);
        margin-bottom: 5px;
    }
    
    /* Kayıt Ol Butonu (Sağ Üst) */
    .stButton>button[kind="secondary"] {
        float: right;
        border-radius: 30px;
        background: rgba(255,255,255,0.1);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Acil Durum Butonu (Kırmızı Parlak) */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) button {
        background-color: #ff4b4b !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 24px !important;
        height: 70px !important;
        border-radius: 15px !important;
        box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.6) !important;
        border: none !important;
    }

    /* AI ve Kamera Butonları (Mavi Cam Efekti) */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 60px;
        background: rgba(0, 198, 255, 0.1);
        color: white;
        border: 1px solid #00c6ff;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: rgba(0, 198, 255, 0.3);
        box-shadow: 0px 0px 15px #00c6ff;
    }

    /* Bilgi Kartları */
    .info-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    /* Hukuki Metin (En Alt Kırmızı) */
    .legal-footer {
        color: #ff4b4b;
        font-size: 13px;
        text-align: center;
        border-top: 1px solid rgba(255, 75, 75, 0.3);
        margin-top: 50px;
        padding-top: 20px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST BAR (Logo ve Kayıt) ---
col_l, col_r = st.columns([4, 1])
with col_l:
    # Logo Placeholder (Dünya Sağlık Örgütü benzeri asit mavisi ikon)
    st.markdown("<h2 style='color: #00c6ff; margin:0;'>🌐 AIHEALTH</h2>", unsafe_allow_html=True)
with col_r:
    st.button("👤 Kayıt Ol", type="secondary")

# --- ANA BAŞLIK ---
st.markdown("<div class='main-title'>AIHEALTH ASİSTANI</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#cbd5e1;'>Yapay Zeka ile Sağlıkta Triyaj ve Hızlı Müdahale Dönemi</p>", unsafe_allow_html=True)

# --- 🚨 ACİL DURUM BÖLÜMÜ ---
st.write("") # Boşluk
if st.button("🚨 ACİL DURUM: YARDIM ÇAĞIR"):
    st.error("⚠️ SİNYAL GÖNDERİLDİ! Konumunuz 112 birimlerine ve yakınlarınıza iletiliyor. Lütfen hattan ayrılmayın.")

st.divider()

# --- ETKİLEŞİM MERKEZİ ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.subheader("💬 AI Sohbet & Ses")
    st.write("Belirtilerinizi yazın veya sesli olarak söyleyin.")
    user_input = st.text_input("Nasıl hissediyorsunuz?", placeholder="Örn: Şiddetli baş ağrım var...")
    if st.button("🤖 AI Analizini Başlat"):
        if user_input:
            st.info("AIHEALTH Analiz Ediyor... Lütfen bekleyin.")
            # Buraya AI Modeli Bağlanacak
            st.success("Ön Değerlendirme: Durumunuz 'Düşük Öncelikli' görünüyor. Bol sıvı tüketin ve dinlenin. Acil servise gitmenize şu an gerek yoktur.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.subheader("📸 Kamera ile Hasar Analizi")
    st.write("Yara, döküntü veya hasarlı bölgeyi analiz edin.")
    img_file = st.camera_input("Fotoğraf Çek")
    if img_file:
        st.warning("Görüntü işleniyor... Deri hasarı derinliği analiz ediliyor.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- HARİTA ---
st.write("")
st.subheader("📍 En Yakın Acil Merkezleri")
# Örnek Hastane Verileri
map_data = pd.DataFrame({
    'lat': [41.0082, 41.0150, 41.0200],
    'lon': [28.9784, 28.9850, 28.9650]
})
st.map(map_data)

# --- HUKUKİ FOOTER ---
st.markdown("""
    <div class="legal-footer">
        <strong>ÖNEMLİ HUKUKİ UYARI:</strong> AIHEALTH bir yapay zeka bilgilendirme sistemidir. 
        Kesinlikle bir doktor teşhisi veya tıbbi tedavi yerine geçmez. 
        Gereksiz acil servis yoğunluğunu önlemek amacıyla rehberlik sunar. 
        Hayati tehlike durumunda derhal 112'yi arayınız. 
        Uygulama kullanımından doğabilecek kararların sorumluluğu kullanıcıya aittir.
    </div>
    """, unsafe_allow_html=True)
