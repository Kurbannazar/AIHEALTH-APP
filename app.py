import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- SAYFA AYARLARI VE TASARIM ---
st.set_page_config(page_title="AIHEALTH Pro", page_icon="🌐", layout="wide")

# Şık mavi-siyah geçişli tasarım ve parlayan butonlar için CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a2a6c 100%);
        color: white;
    }
    .stButton>button {
        border-radius: 20px;
        transition: 0.3s;
    }
    /* Mavi Parlayan Kayıt Butonu */
    div[data-testid="stVerticalBlock"] > div:nth-child(1) button {
        background-color: #007bff;
        box-shadow: 0 0 15px #007bff;
        border: none;
        color: white;
    }
    /* Kırmızı Parlayan Acil Butonu */
    .emergency-btn button {
        background-color: #ff0000 !important;
        box-shadow: 0 0 20px #ff0000 !important;
        font-weight: bold !important;
        font-size: 20px !important;
        width: 100%;
    }
    .footer-legal {
        color: #ff4b4b;
        font-size: 12px;
        text-align: center;
        margin-top: 50px;
        border-top: 1px solid #444;
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GEMINI AYARI ---
# Not: API anahtarını Streamlit Secrets kısmına eklemelisin
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("Lütfen API anahtarını yapılandırın.")

# --- ÜST MENÜ (Header) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.title("🌐 AIHEALTH")
with col3:
    if st.button("👤 Kayıt Ol"):
        st.info("Kayıt sistemi yakında aktif edilecek.")

# --- ANA İÇERİK ---
st.write("### Yapay Zeka Destekli Sağlık ve İlk Yardım Asistanı")

# Acil Durum Bölümü
with st.container():
    st.markdown('<div class="emergency-btn">', unsafe_allow_html=True)
    if st.button("🚨 ACİL DURUM - 112'Yİ ARA"):
        st.markdown("[112 Acil Çağrı Merkezini Ara](tel:112)")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Özellik Sekmeleri
tab1, tab2, tab3 = st.tabs(["💬 AI Chat Asistanı", "📸 Yara/Hasar Analizi", "🏥 Yakın Merkezler"])

with tab1:
    st.subheader("🤖 Sağlık Asistanına Sorun")
    user_input = st.chat_input("Belirtilerinizi yazın veya ilk yardım bilgisi isteyin...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        
        # Yapay zeka yanıtı (Sistem talimatı ile birlikte)
        prompt = f"Sen bir ilk yardım asistanısın. Kullanıcıya tıbbi tavsiye vermeden, sadece ilk yardım adımlarını anlat ve gerekirse acile yönlendir. Kullanıcı sorusu: {user_input}"
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.write(response.text)

with tab2:
    st.subheader("📷 Görüntülü Analiz")
    img_file = st.camera_input("Yaralanmanın fotoğrafını çekin")
    if img_file:
        st.success("Görüntü alındı. Analiz için Gemini Vision'a gönderiliyor...")
        # Burada görüntüyü Gemini'ye gönderen fonksiyon çalışacak

with tab3:
    st.subheader("📍 En Yakın Sağlık Kurumları")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏥 En Yakın Hastaneler"):
            st.markdown("[Google Haritalar: Hastaneler](https://www.google.com/maps/search/hastane)")
    with c2:
        current_hour = datetime.now().hour
        is_night = current_hour >= 19 or current_hour < 8
        label = "🌙 Nöbetçi Eczaneler" if is_night else "💊 Eczaneler"
        if st.button(label):
            st.markdown(f"[Google Haritalar: {label}](https://www.google.com/maps/search/eczane)")

# --- HUKUKİ UYARI (Sorumluluk Reddi) ---
st.markdown("""
    <div class="footer-legal">
        ⚠️ <b>HUKUKİ UYARI:</b> AIHEALTH bir yapay zeka asistanıdır ve profesyonel tıbbi teşhis koyma yetkisine sahip değildir. 
        Burada sunulan bilgiler sadece bilgilendirme amaçlıdır. Hayati tehlike durumunda derhal 112 Acil Servis'i arayınız. 
        Uygulamayı kullanarak bu sorumluluğu kabul etmiş sayılırsınız.
    </div>
    """, unsafe_allow_html=True)
