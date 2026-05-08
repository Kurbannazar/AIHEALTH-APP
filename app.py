import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from streamlit_js_eval import streamlit_js_eval
import time

# Sayfa yapılandırması
st.set_page_config(
    page_title="AIHEALTH - Profesyonel Sağlık Asistanı",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Özel CSS - Premium Tasarım Dili
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp {
        background: linear-gradient(180deg, #020205 0%, #001529 100%);
        color: #ffffff;
    }
    
    /* Başlık ve Glow Efekti */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.8), 0 0 30px rgba(0, 212, 255, 0.4);
        margin-bottom: 0px;
        letter-spacing: 5px;
    }
    
    /* Kayıt Ol Butonu Tasarımı */
    .stButton > button {
        background-color: transparent;
        color: #00d4ff;
        border: 1px solid #00d4ff;
        border-radius: 5px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
    }
    .stButton > button:hover {
        background-color: rgba(0, 212, 255, 0.1);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        border: 1px solid #ffffff;
        color: #ffffff;
    }
    
    /* Acil Durum Butonu */
    .emergency-btn > button {
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        padding: 20px 50px !important;
        border-radius: 50px !important;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.6) !important;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
        70% { box-shadow: 0 0 0 20px rgba(255, 75, 75, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }
    
    /* Metin Alanı ve Girdiler */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
    }
    
    /* Hukuki Uyarı */
    .legal-disclaimer {
        color: #ff4b4b;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 10px;
        font-weight: 500;
    }
    
    /* Spinner ve Animasyonlar */
    .stSpinner > div {
        border-top-color: #00d4ff !important;
    }
    
    /* Blokları Gizle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Üst Bölüm: Kayıt Ol | Logo | Başlık
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("<div style='padding-top: 50px;'></div>", unsafe_allow_html=True)
    if st.button("Kayıt Ol"):
        st.info("Kayıt sistemi yakında aktif edilecektir.")

with col2:
    if os.path.exists("ai_heal.jpg"):
        st.image("ai_heal.jpg", width=200, use_container_width=False)
    st.markdown("<h1 class='main-title'>AIHEALTH</h1>", unsafe_allow_html=True)

# Gemini Yapılandırması (Kullanıcı anahtarı yoksa Manus'un OpenAI uyumlu Gemini modelini simüle ederiz veya placeholder bırakırız)
# Gerçek uygulamada st.secrets veya environment variable kullanılmalıdır.
API_KEY = os.environ.get("GOOGLE_API_KEY", "") # Kullanıcıdan alınabilir
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("Gemini API anahtarı bulunamadı. Lütfen yapılandırın.")

# Şikayet Giriş Alanı
st.markdown("### Şikayetinizi Belirtin")
complaint = st.text_area("Belirtilerinizi detaylıca yazın...", height=150, placeholder="Örn: Şiddetli baş ağrısı, halsizlik ve hafif ateş...")

# Medya Araçları Butonları
m_col1, m_col2, m_col3 = st.columns([1, 1, 4])
with m_col1:
    camera_photo = st.camera_input("Kamera")
with m_col2:
    uploaded_file = st.file_uploader("Fotoğraf Yükle", type=['jpg', 'jpeg', 'png'])

# AI Analiz Fonksiyonu
def analyze_health(text, image=None):
    if not API_KEY:
        return "Hata: Gemini API anahtarı eksik. Lütfen yapılandırın."
    
    prompt = f"""
    Sen profesyonel bir medikal yapay zeka asistanısın. Kullanıcının şu şikayetini analiz et:
    Şikayet: {text}
    
    Eğer bir görsel sağlandıysa, görseldeki belirtileri de dikkate al.
    Yanıtını şu yapıda ver:
    1. Olası Durumlar (Tıbbi teşhis değildir, sadece ihtimaller)
    2. Önerilen Adımlar
    3. Hangi Bölüme Gidilmeli?
    
    DİL: Türkçe. Üslup: Ciddi, profesyonel, medikal teknoloji odaklı.
    """
    
    try:
        if image:
            img = Image.open(image)
            response = model.generate_content([prompt, img])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Analiz sırasında bir hata oluştu: {str(e)}"

# Analiz Tetikleyici
if complaint:
    with st.spinner("AIHEALTH Verileri Analiz Ediyor..."):
        analysis_result = analyze_health(complaint, camera_photo or uploaded_file)
        st.markdown("---")
        st.markdown("### AI Ön Analiz Raporu")
        st.markdown(analysis_result)
        st.markdown(f"<p class='legal-disclaimer'>Bu bir yapay zeka analizidir, tıbbi teşhis yerine geçmez. Acil durumlarda lütfen 112'yi arayın veya en yakın sağlık kuruluşuna başvurun.</p>", unsafe_allow_html=True)

st.markdown("---")

# Konum Bazlı Fonksiyonlar
st.markdown("### Hızlı Erişim")
loc_col1, loc_col2 = st.columns(2)

# JS ile konum alma
location = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition((pos) => { return {lat: pos.coords.latitude, lon: pos.coords.longitude} })", key="location")

if loc_col1.button("En Yakın Hastane"):
    if location:
        lat, lon = location['lat'], location['lon']
        url = f"https://www.google.com/maps/search/hastane/@{lat},{lon},14z"
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{url}\'">', unsafe_allow_html=True)
    else:
        st.info("Konum bilgisi alınıyor veya izin verilmedi. Lütfen bekleyin veya tarayıcı izinlerini kontrol edin.")

if loc_col2.button("Nöbetçi Eczane"):
    if location:
        lat, lon = location['lat'], location['lon']
        url = f"https://www.google.com/maps/search/nöbetçi+eczane/@{lat},{lon},14z"
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{url}\'">', unsafe_allow_html=True)
    else:
        st.info("Konum bilgisi alınıyor...")

# Acil Durum Butonu
st.markdown("<br><br>", unsafe_allow_html=True)
_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    st.markdown('<div class="emergency-btn">', unsafe_allow_html=True)
    if st.button("ACİL DURUM", key="emergency"):
        st.error("ACİL DURUM SİNYALİ OLUŞTURULDU. LÜTFEN 112'Yİ ARAYIN!")
    st.markdown('</div>', unsafe_allow_html=True)
