import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- TASARIM VE GRADYAN ARKA PLAN ---
st.set_page_config(page_title="AIHEALTH", layout="wide")

# CSS ile Dark-Tech Tasarım
st.markdown("""
    <style>
    /* Arka planı siyahtan maviye geçişli yapıyoruz */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #001f3f 100%);
        color: white;
    }
    
    /* Başlık ve Metin Renkleri */
    h1, h2, h3, p, span {
        color: #e0f2ff !important;
    }

    /* Parlayan Mavi Butonlar (Kayıt ve Genel) */
    .stButton>button {
        background: linear-gradient(45deg, #004e92, #000428);
        color: #00d4ff !important;
        border: 1px solid #00d4ff !important;
        box-shadow: 0 0 10px #004e92;
        border-radius: 10px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px #00d4ff;
        color: white !important;
    }

    /* Parlayan Kırmızı Acil Butonu */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) button {
        background: linear-gradient(45deg, #8b0000, #ff0000) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 0 15px #ff0000 !important;
        font-size: 20px !important;
        height: 60px;
    }

    /* Input alanlarını koyulaştırma */
    .stTextInput>div>div>input {
        background-color: #001021 !important;
        color: white !important;
        border: 1px solid #004e92 !important;
    }

    /* Alt Bilgi (Hukuki) */
    .legal-footer {
        color: #ff4b4b;
        font-size: 11px;
        text-align: center;
        padding: 20px;
        border-top: 1px solid #004e92;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST BAR ---
col_logo, col_empty, col_reg = st.columns([2, 3, 1])
with col_logo:
    st.markdown("## ⚕️ AIHEALTH") # Sade ve şık bir ikon
with col_reg:
    st.button("KAYIT OL")

# --- ANA İÇERİK ---
st.title("Yapay Zeka Sağlık Asistanı")
st.write("Güvenliğiniz ve sağlığınız için her an yanınızdayız.")

# ACİL DURUM KISMI
st.button("🚨 ACİL YARDIM ÇAĞIR")

st.divider()

# --- MODÜLLER ---
col_chat, col_tools = st.columns([2, 1])

with col_chat:
    st.subheader("AI Chat Asistanı")
    user_msg = st.text_input("Şikayetinizi yazın...", placeholder="Örn: Bileğim burkuldu, ne yapmalıyım?")
    
    if user_msg:
        # Gemini Entegrasyonu (Arka planda çalışır)
        try:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Sisteme sağlık asistanı rolü veriyoruz
            prompt = f"Sen profesyonel bir sağlık asistanısın. Kullanıcıya kısa, net ve sakinleştirici bir ilk yardım tavsiyesi ver. Acilse doktora yönlendir: {user_msg}"
            response = model.generate_content(prompt)
            st.info(response.text)
        except:
            st.error("Sistem şu an meşgul, lütfen daha sonra tekrar deneyiniz.")

with col_tools:
    st.subheader("Hızlı İşlemler")
    st.camera_input("Hasar/Yara Fotoğrafı Çek")
    
    if st.button("📍 En Yakın Hastaneler"):
        st.markdown("[Hastaneleri Göster](https://www.google.com/maps/search/hastane/)")
        
    # Eczane Mantığı (Gündüz normal, Gece nöbetçi)
    hour = datetime.now().hour
    is_night = hour >= 19 or hour <= 8
    btn_label = "🌙 Nöbetçi Eczaneler" if is_night else "💊 Eczaneler"
    if st.button(btn_label):
        st.markdown(f"[Eczaneleri Göster](https://www.google.com/maps/search/eczane/)")

# --- HUKUKİ ALAN ---
st.markdown("""
    <div class="legal-footer">
        HUKUKİ BİLGİLENDİRME: Bu uygulama, devletin resmi acil servislerinin (112) yerini tutmaz. 
        Verilen yanıtlar yapay zeka tarafından üretilmektedir ve tıbbi kesinlik taşımaz. 
        Kritik durumlarda lütfen en yakın sağlık kuruluşuna başvurun.
    </div>
    """, unsafe_allow_html=True)
