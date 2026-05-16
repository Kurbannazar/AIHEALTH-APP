import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime

st.set_page_config(page_title="AIHEALTH - Profesyonel Sağlık Asistanı", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    .header-buttons { display: flex; justify-content: flex-end; gap: 15px; padding: 10px; }
    .btn-register { background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%); color: white !important; border: none; padding: 10px 24px; font-weight: bold; border-radius: 6px; text-decoration: none; box-shadow: 0 0 15px rgba(0, 102, 255, 0.6); }
    .btn-emergency { background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%); color: white !important; border: none; padding: 10px 24px; font-weight: bold; border-radius: 6px; text-decoration: none; box-shadow: 0 0 15px rgba(255, 75, 43, 0.6); }
    .neon-card { background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 20px; box-shadow: 0 0 10px rgba(0, 210, 255, 0.1); margin-bottom: 20px; }
    .map-link { display: inline-block; background: #1f2937; color: #00d2ff !important; border: 1px solid #00d2ff; padding: 8px 16px; border-radius: 4px; text-decoration: none; font-weight: bold; margin-top: 10px; }
    .legal-footer { margin-top: 50px; padding: 20px; border-top: 1px solid #ff4b2b; background-color: rgba(255, 75, 43, 0.05); color: #ff4b2b; font-size: 0.85rem; text-align: center; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# GÜVENLİ API ÇAĞRISI (Anahtarı Streamlit ayarlarından alacak)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config={"temperature": 0.2, "top_p": 0.95, "max_output_tokens": 1500},
  system_instruction="Sen AIHEALTH profesyonel tıbbi analiz sistemisin. Kamera fotoğraflarını klinik ve kesin talimatlarla analiz et. Her zaman 112 uyarısı yap."
)

st.components.v1.html("""
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                window.parent.postMessage({ type: 'streamlit:setComponentValue', value: {latitude: lat, longitude: lon} }, '*');
            });
        }
    }
    setTimeout(getLocation, 500);
    </script>
""", height=0)

st.markdown('<div class="header-buttons"><a href="#" class="btn-register">Kayıt Ol</a><a href="tel:112" class="btn-emergency">ACİL (112)</a></div>', unsafe_allow_html=True)
st.title("AIHEALTH")
st.markdown("### Profesyonel Sağlık ve Entegre Klinik Sistem")
st.write("---")

st.header("Donanım Bazlı Fotoğraf Analizi")
camera_image = st.camera_input("Yaralı Bölgeyi Net Bir Şekilde Fotoğraflayın")
if camera_image:
    if st.button("Görseli Analiz Et"):
        with st.spinner("Klinik analiz yapılıyor..."):
            img = Image.open(camera_image)
            response = model.generate_content(["Bu fotoğraftaki durumu analiz et ve ilk yardım adımlarını söyle.", img])
            st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
            st.subheader("📋 Klinik Görsel Analiz Raporu")
            st.write(response.text)
            st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.header("Konum Bazlı Acil Entegrasyon")
current_lat, current_lon = 41.018, 28.646
current_hour = datetime.datetime.now().hour

col1, col2 = st.columns(2)
with col1:
    if st.button("En Yakın Hastane Rotalarını Göster"):
        maps_url = f"https://www.google.com/maps/dir/?api=1&origin={current_lat},{current_lon}&destination=Hospital"
        st.markdown(f'<a href="{maps_url}" target="_blank" class="map-link">Haritada Rotayı Başlat</a>', unsafe_allow_html=True)
with col2:
    if st.button("Eczaneleri Listele"):
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        if current_hour >= 19 or current_hour < 8:
            st.warning("⏰ Saat 19:00 sonrası: Nöbetçi Eczaneler")
            st.markdown("<a href='tel:02120000000' style='color:#ff416c;'>📞 Eczaneyi Ara</a>", unsafe_allow_html=True)
        else:
            st.success("Normal Çalışma Saatleri")
            maps_url = f"https://www.google.com/maps/search/?api=1&query=pharmacy&location={current_lat},{current_lon}"
            st.markdown(f'<a href="{maps_url}" target="_blank" class="map-link">Eczaneleri Göster</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="legal-footer">YASAL UYARI: AIHEALTH bir yapay zeka sistemidir. Acil durumlarda derhal 112\'yi arayınız.</div>', unsafe_allow_html=True)
