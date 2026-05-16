import streamlit as st
import requests
import json
import time
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import io
import base64
import folium
from streamlit_folium import folium_static
import os

# Sayfa yapılandırması
st.set_page_config(
    page_title="AIHEALTH - Sağlık Sistem Yardımcısı",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# API Anahtarları (Gerçek uygulamada .env dosyasından yüklenmeli)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
GOOGLE_MAPS_API_KEY = st.secrets.get("GOOGLE_MAPS_API_KEY", "YOUR_GOOGLE_MAPS_API_KEY_HERE")

# Gemini AI'yı yapılandır
genai.configure(api_key=GEMINI_API_KEY)

# Özel CSS Stilleri
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    /* Başlık Stilleri */
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00b4d8, #0077b6, #03045e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 20px rgba(0, 180, 216, 0.3);
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #90e0ef;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Buton Stilleri */
    .stButton > button {
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: none;
        width: 100%;
    }
    
    .emergency-btn {
        background: linear-gradient(90deg, #d00000, #9d0208) !important;
        color: white !important;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.5) !important;
    }
    
    .emergency-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.7) !important;
    }
    
    .register-btn {
        background: linear-gradient(90deg, #0077b6, #0096c7) !important;
        color: white !important;
        box-shadow: 0 0 20px rgba(0, 119, 182, 0.5) !important;
    }
    
    .register-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(0, 119, 182, 0.7) !important;
    }
    
    .action-btn {
        background: linear-gradient(90deg, #1a1a2e, #16213e) !important;
        color: #90e0ef !important;
        border: 1px solid #00b4d8 !important;
        box-shadow: 0 0 15px rgba(0, 180, 216, 0.3) !important;
    }
    
    .action-btn:hover {
        transform: scale(1.03);
        box-shadow: 0 0 25px rgba(0, 180, 216, 0.5) !important;
    }
    
    /* Kart Stilleri */
    .feature-card {
        background: rgba(26, 26, 46, 0.8);
        border-radius: 16px;
        padding: 25px;
        border: 1px solid #1e6091;
        box-shadow: 0 0 25px rgba(0, 180, 216, 0.2);
        height: 100%;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 35px rgba(0, 180, 216, 0.3);
    }
    
    /* Uyarı Metni */
    .legal-warning {
        background: rgba(157, 2, 8, 0.1);
        border-left: 4px solid #d00000;
        padding: 15px;
        border-radius: 8px;
        margin-top: 30px;
        font-size: 0.9rem;
    }
    
    /* Görsel Analiz Sonuçları */
    .analysis-result {
        background: rgba(0, 119, 182, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid #00b4d8;
    }
    
    /* Konum Kartları */
    .location-card {
        background: rgba(26, 26, 46, 0.9);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #1e6091;
    }
    
    /* Responsive Tasarım */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .feature-card {
            padding: 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Navigasyon butonları (Sağ üst köşe)
col1, col2, col3 = st.columns([6, 1, 1])
with col2:
    if st.button("Kayıt Ol", key="register_top", help="Yeni hesap oluştur"):
        st.session_state.show_register = True
with col3:
    if st.button("ACİL", key="emergency_top", help="Acil durumda 112'yi ara"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:112">', unsafe_allow_html=True)

# Ana Başlık
st.markdown('<h1 class="main-title">🏥 AIHEALTH</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Akıllı Sağlık Sistem Yardımcısı - Profesyonel Tıbbi Destek</p>', unsafe_allow_html=True)

# Ana İçerik Alanı
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 📸 Donanım Bazlı Fotoğraf Analizi")
    st.markdown("Cihazınızın kamerasını kullanarak yaralı bölgeyi anında çekin ve AI analizi alın.")
    
    # Kameradan fotoğraf çekme
    captured_image = st.camera_input("Yaralı bölgeyi çekmek için kamerayı kullanın", 
                                     key="camera_input",
                                     help="Doğrudan cihaz kameranıza bağlanır")
    
    if captured_image:
        with st.spinner("Görsel AI analizi yapılıyor..."):
            try:
                # Görseli PIL formatına çevir
                image = Image.open(captured_image)
                
                # Görseli base64 formatına çevir
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                # Gemini Vision API için hazırlık
                model = genai.GenerativeModel('gemini-pro-vision
