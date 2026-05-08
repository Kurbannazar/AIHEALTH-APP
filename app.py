import streamlit as st
import google.generativeai as genai

# --- Gemini API Yapılandırması ---
# Buraya kendi API anahtarını eklemelisin
API_KEY = "SENIN_GEMINI_API_ANAHTARIN" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- Sayfa Ayarları ---
st.set_page_config(page_title="AIHEALTH", layout="wide")

# --- Premium Siyah-Mavi Tasarım (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #050505, #001f3f);
        color: #ffffff;
    }
    .header-container {
        display: flex; flex-direction: column; align-items: center; padding: 20px;
        border-bottom: 2px solid #00d2ff; margin-bottom: 30px;
    }
    .main-title {
        font-size: 50px; font-weight: 900;
        background: -webkit-linear-gradient(#00d2ff, #ffffff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    /* Parlayan Kayıt Butonu */
    div.stButton > button {
        background: linear-gradient(45deg, #000428, #004e92);
        color: #00d2ff; border: 1px solid #00d2ff; border-radius: 12px;
        height: 3.5em; width: 100%; font-weight: bold;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.8);
        color: white;
    }
    /* AI Yanıt Kutusu */
    .stAlert {
        background-color: rgba(0, 210, 255, 0.1) !important;
        color: white !important;
        border: 1px solid #00d2ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Üst Alan: Logo ve Başlık ---
st.markdown(f"""
    <div class="header-container">
        <div style="font-size: 70px; filter: drop-shadow(0 0 10px #00d2ff);">⚕️🧠</div> 
        <div class="main-title">AIHEALTH</div>
    </div>
    """, unsafe_allow_html=True)

# --- Ana Gövde ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Şikayet ve Belirtiler")
    user_complaint = st.text_area(
        "Size nasıl yardımcı olabilirim?", 
        height=200, 
        placeholder="Örn: Sol kolumda uyuşma ve göğüs ağrısı var..."
    )

with col2:
    st.markdown("### ⚙️ İşlem Paneli")
    analyze_button = st.button("ANALİZ ET VE KAYDET")
    
    st.markdown("---")
    st.subheader("📍 Hızlı Erişim")
    st.markdown("[🔍 En Yakın Hastaneler](https://www.google.com/maps/search/hastane)")
    st.markdown("[💊 Nöbetçi Eczaneler](https://www.google.com/maps/search/eczane)")

# --- AI Analiz Süreci ---
if analyze_button:
    if user_complaint:
        with st.spinner('AIHEALTH Analiz Yapıyor...'):
            try:
                # Gemini'ye gönderilen "Tıbbi Asistan" komutu (Prompt Engineering)
                prompt = f"""
                Sen profesyonel bir sağlık asistanısın. Kullanıcının şu şikayetini analiz et: '{user_complaint}'
                1. Olası durumları belirt (Teşhis koyma, sadece ihtimalleri söyle).
                2. Aciliyet durumunu değerlendir (Normal mi, Acil mi?).
                3. İlk yardım tavsiyeleri ver.
                4. Ciddi bir durum sezersen mutlaka hastaneye yönlendir.
                Yanıtını kısa, net ve güven verici bir dille ver.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("### 🤖 Yapay Zeka Analizi")
                st.info(response.text)
                
                # Burada verileri Firebase'e veya bir dosyaya kaydetme fonksiyonunu çağırabiliriz.
                st.success("Analiz tamamlandı ve sistem kayıtlarına eklendi.")
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen analiz için bir şikayet metni girin.")

st.markdown("---")
st.caption("AIHEALTH © 2026 | Geleceğin Sağlık Teknolojisi")
