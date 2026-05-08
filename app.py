import streamlit as st
import google.generativeai as genai
import os

# --- 1. GEMINI YAPILANDIRMASI ---
API_KEY = "BURAYA_ANAHTARINI_YAPISTIR" # Anahtarı buraya ekle!
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH", layout="wide")

# --- 3. PREMIUM TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #020205, #001529);
        color: white;
    }
    
    /* Logo Konumlandırma ve Temizleme */
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: -50px;
    }
    
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 65px;
        font-weight: 900;
        background: -webkit-linear-gradient(#ffffff, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 5px;
        margin-top: -20px;
    }

    /* Şikayet Alanı */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid #00d2ff !important;
        border-radius: 15px;
    }

    /* PARLAYAN BUTON */
    div.stButton > button {
        background: linear-gradient(45deg, #000000, #004e92);
        color: #00d2ff;
        border: 2px solid #00d2ff;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4);
        width: 100%;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 0 40px rgba(0, 210, 255, 0.8);
        color: white;
        transform: scale(1.02);
    }
    
    /* Yanıt Kutusu */
    .ai-response {
        background: rgba(0, 210, 255, 0.1);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #00d2ff;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ÜST KISIM: LOGO VE İSİM ---
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
# Dosya adının tam olarak eşleştiğinden emin ol (Aı heal.jpg)
if os.path.exists("Aı heal.jpg"):
    st.image("Aı heal.jpg", width=200) 
else:
    st.write("⚠️ Logo dosyası bulunamadı! (Dosya adını kontrol et)")

st.markdown('<div class="main-title">AIHEALTH</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. ARA YÜZ VE FONKSİYONLAR ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Belirtilerinizi Yazın")
    complaint = st.text_area("", placeholder="Örn: Ani başlayan göğüs ağrısı...", height=250)

with col2:
    st.markdown("### ⚙️ İşlemler")
    # BUTONUN ÇALIŞTIĞI ANA NOKTA
    if st.button("ANALİZ ET VE KAYDET"):
        if complaint:
            with st.spinner('AI Analiz Ediyor...'):
                try:
                    full_prompt = f"Sen profesyonel bir sağlık asistanısın. Şu şikayeti analiz et ve ilk yardım önerisi ver: {complaint}"
                    response = model.generate_content(full_prompt)
                    
                    st.session_state['ai_result'] = response.text
                except Exception as e:
                    st.error("API hatası! Anahtarı kontrol edin.")
        else:
            st.warning("Lütfen bir şikayet yazın.")

    st.markdown("---")
    st.markdown("📍 [En Yakın Hastaneler](https://www.google.com/maps/search/hastane)")
    st.markdown("💊 [Nöbetçi Eczaneler](https://www.google.com/maps/search/eczane)")

# --- 6. SONUÇ EKRANI ---
if 'ai_result' in st.session_state:
    st.markdown("### 🤖 Analiz Sonucu")
    st.markdown(f'<div class="ai-response">{st.session_state["ai_result"]}</div>', unsafe_allow_html=True)

st.markdown("<br><center>AIHEALTH © 2026</center>", unsafe_allow_html=True)
 
