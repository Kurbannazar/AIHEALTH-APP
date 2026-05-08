import streamlit as st
import google.generativeai as genai

# --- KRİTİK AYAR: GEMINI API ANAHTARI ---
# Buraya kendi API anahtarını tırnak içine yapıştır!
API_KEY = "BURAYA_API_ANAHTARINI_YAPISTIR" 

# API Yapılandırması
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash') # Hızlı ve güncel model
except:
    st.error("API Anahtarı eksik veya hatalı!")

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH", layout="wide")

# --- PREMIUM SİYAH-MAVİ TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Ana Ekran */
    .stApp {
        background: linear-gradient(180deg, #020205, #001529);
        color: #ffffff;
    }
    
    /* Logo ve Başlık Alanı (Stickerlar Silindi) */
    .header-box {
        text-align: center;
        padding: 40px;
        border-bottom: 1px solid #00d2ff;
        margin-bottom: 40px;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 55px;
        font-weight: 800;
        background: -webkit-linear-gradient(#00d2ff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 3px;
    }

    /* Şikayet Kutusu */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #00d2ff !important;
        border-radius: 15px;
    }

    /* PARLAYAN SİYAH-MAVİ BUTON */
    div.stButton > button {
        background: linear-gradient(45deg, #000000, #004e92);
        color: #00d2ff;
        border: 2px solid #00d2ff;
        padding: 20px 40px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 12px;
        cursor: pointer;
        transition: 0.4s;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
        width: 100%;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.9);
        transform: translateY(-3px);
        color: white;
        border: 2px solid white;
    }

    /* Yanıt Paneli */
    .response-area {
        background: rgba(0, 210, 255, 0.07);
        padding: 25px;
        border-left: 5px solid #00d2ff;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST PANEL ---
st.markdown('<div class="header-box"><div class="main-title">AIHEALTH</div></div>', unsafe_allow_html=True)

# --- ANA İÇERİK ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Şikayet ve Belirtiler")
    user_input = st.text_area(
        "", 
        height=250, 
        placeholder="Belirtilerinizi buraya yazın (Örn: Baş dönmesi, şiddetli karın ağrısı...)",
        key="complaint_input"
    )

with col2:
    st.markdown("### ⚙️ Analiz Merkezi")
    # BUTON BURADA ÇALIŞIYOR
    submit_button = st.button("ANALİZ ET VE KAYDET")
    
    st.markdown("---")
    st.info("💡 **Hızlı Erişim**\n\n- [En Yakın Hastane](https://www.google.com/maps/search/hastane)\n- [Nöbetçi Eczane](https://www.google.com/maps/search/eczane)")

# --- BUTON MANTIĞI VE GEMINI BAĞLANTISI ---
if submit_button:
    if user_input.strip() == "":
        st.warning("Lütfen önce bir şikayet giriniz.")
    else:
        with st.spinner('AIHEALTH Verileri Analiz Ediyor...'):
            try:
                # Prompt Engineering (Sistemi sağlık asistanı gibi davranmaya zorluyoruz)
                prompt = f"""
                Sen profesyonel bir tıbbi asistan yazılımısın (AIHEALTH). 
                Kullanıcının şu şikayetini analiz et: '{user_input}'
                Yanıtını şu formatta ver:
                1. ANALİZ: Olası durumları basitçe açıkla.
                2. ACİLİYET: (DÜŞÜK / ORTA / YÜKSEK) şeklinde belirt.
                3. ÖNERİ: İlk yardım veya yapılması gerekenler.
                *Not: Teşhis koymadığını, bunun sadece bir ön analiz olduğunu belirt.*
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown("### 🤖 Yapay Zeka Sonucu")
                st.markdown(f'<div class="response-area">{response.text}</div>', unsafe_allow_html=True)
                st.success("Analiz başarılı! Veritabanına kaydedilmeye hazır.")
                
            except Exception as e:
                st.error(f"Sistem bir hata ile karşılaştı. API anahtarınızı kontrol edin.")

st.markdown("<br><br><center><p style='color: grey;'>AIHEALTH © 2026 | Tüm Hakları Saklıdır.</p></center>", unsafe_allow_html=True)
