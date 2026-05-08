import streamlit as st
import google.generativeai as genai

# --- KRİTİK AYAR: GEMINI API ANAHTARI ---
# Buraya kendi API anahtarını tırnak içine yapıştır!
# API anahtarı olmadan buton çalışmaz.
API_KEY = "BURAYA_API_ANAHTARINI_YAPISTIR" 

# API Yapılandırması
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash') # Hızlı ve güncel model
except:
    st.error("API Anahtarı eksik veya hatalı!")

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="AIHEALTH - Akıllı Sağlık Asistanı", 
    page_icon="⚕️",
    layout="wide"
)

# --- PREMIUM SİYAH-MAVİ TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Ana Ekran */
    .stApp {
        background: linear-gradient(180deg, #020205, #001529);
        color: #ffffff;
    }
    
    /* Logo ve Başlık Alanı (Temizlendi ve Güncellendi) */
    .header-box {
        text-align: center;
        padding: 50px 20px;
        border-bottom: 2px solid #00d2ff;
        margin-bottom: 50px;
        position: relative;
    }
    
    /* Temizlenmiş Logo Görseli */
    .header-logo-img {
        width: 150px; /* Logo Boyutu */
        margin-bottom: 15px;
        /* Premium Glow Efekti */
        filter: drop-shadow(0 0 15px rgba(0, 210, 255, 0.7));
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 60px;
        font-weight: 900;
        background: -webkit-linear-gradient(#ffffff, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        margin-top: 0px;
    }

    /* Şikayet Kutusu */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #00d2ff !important;
        border-radius: 15px;
        font-size: 16px;
    }

    /* PARLAYAN SİYAH-MAVİ BUTON */
    div.stButton > button {
        background: linear-gradient(45deg, #000000, #004e92);
        color: #00d2ff;
        border: 2px solid #00d2ff;
        padding: 20px 40px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 15px;
        cursor: pointer;
        transition: 0.4s;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.5);
        width: 100%;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 0 40px rgba(0, 210, 255, 1);
        transform: translateY(-4px) scale(1.02);
        color: white;
        border: 2px solid white;
    }

    /* Yanıt Paneli */
    .response-area {
        background: rgba(0, 210, 255, 0.1);
        padding: 30px;
        border-left: 6px solid #00d2ff;
        border-radius: 12px;
        margin-top: 25px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Hızlı Erişim Linkleri */
    .quick-access-box {
        background-color: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(0, 210, 255, 0.2);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST PANEL (LOGO VE BAŞLIK) ---
# Logonun temizlenmiş, filigransız hali bu kod bloğunun içine gömülüdür.
st.markdown(f"""
    <div class="header-box">
        <img src="data:image/png;base64,{st.secrets['LOGO_IMAGE_BASE64']}" class="header-logo-img" alt="AIHEALTH Logo">
        <div class="main-title">AIHEALTH</div>
    </div>
    """, unsafe_allow_html=True)

# --- ANA İÇERİK ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Şikayet ve Belirtiler")
    st.caption("AI Asistanına nasıl hissettiğinizi anlatın.")
    user_input = st.text_area(
        "", 
        height=280, 
        placeholder="Belirtilerinizi buraya yazın (Örn: Sol kolumda uyuşma ve göğüs ağrısı var, nefes alırken zorlanıyorum...)",
        key="complaint_input"
    )

with col2:
    st.markdown("### ⚙️ Analiz Merkezi")
    submit_button = st.button("ANALİZ ET VE KAYDET")
    
    st.markdown("---")
    
    with st.expander("💡 Hızlı Erişim Paneli", expanded=True):
        st.markdown("""
