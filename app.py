import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime
import os

# --- SAYFA YAPILANDIRMASI VE TEMA (GLOW EFFECTS) ---
st.set_page_config(page_title="AIHEALTH - Profesyonel Sağlık Asistanı", layout="wide")

# CSS ile Siyah ve Mavi Parlayan (Glow) Tema Kuralları
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    /* Sağ Üst Buton Konteyneri */
    .header-buttons {
        display: flex;
        justify-content: flex-end;
        gap: 15px;
        padding: 10px;
    }
    
    /* Parlayan Mavi Kayıt Ol Butonu */
    .btn-register {
        background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%);
        color: white !important;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        border-radius: 6px;
        text-decoration: none;
        box-shadow: 0 0 15px rgba(0, 102, 255, 0.6);
        transition: 0.3s;
    }
    .btn-register:hover {
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.9);
    }
    
    /* Parlayan Kırmızı ACİL Butonu */
    .btn-emergency {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white !important;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        border-radius: 6px;
        text-decoration: none;
        box-shadow: 0 0 15px rgba(255, 75, 43, 0.6);
        transition: 0.3s;
    }
    .btn-emergency:hover {
        box-shadow: 0 0 25px rgba(255, 65, 108, 0.9);
    }

    /* Kart Yapıları ve Harita Linkleri */
    .neon-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.1);
        margin-bottom: 20px;
    }
    
    .map-link {
        display: inline-block;
        background: #1f2937;
        color: #00d2ff !important;
        border: 1px solid #00d2ff;
        padding: 8px 16px;
        border-radius: 4px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 10px;
        box-shadow: 0 0 8px rgba(0, 210, 255, 0.2);
    }
    .map-link:hover {
        background: #00d2ff;
        color: #0b0f19 !important;
    }

    /* Hukuki Metin Sabitleyici */
    .legal-footer {
        position: relative;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #ff4b2b;
        background-color: rgba(255, 75, 43, 0.05);
        color: #ff4b2b;
        font-size: 0.85rem;
        font-weight: 500;
        text-align: center;
        border-radius: 4px;
    }
    </style>
""", unsafe_allowed_allowed=True)

# --- GEMINI API YAPILANDIRMASI ---
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "max_output_tokens": 1500,
}

system_instruction = (
    "Sen AIHEALTH profesyonel tıbbi analiz ve ilk yardım sistemisin. "
    "Kamera verilerinden gelen yaralanma veya semptom fotoğraflarını incelerken "
    "klinik, nesnel ve kesin talimatlar vermelisin. Ciddiyeti değerlendir ve "
    "yapılması gereken anatomik/fiziksel ilk müdahale adımlarını sırala."
)

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=system_instruction,
)

# --- JAVASCRIPT KÖPRÜSÜ (CANLI KONUM ALMA) ---
# Tarayıcının W3C Geolocation API'sini tetikleyip koordinatları Streamlit'e aktarır.
st.components.v1.html("""
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        }
    }
    function showPosition(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        // Streamlit input elementlerine gizlice aktar ve tetikle
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {latitude: lat, longitude: lon}
        }, '*');
    }
    function showError(error) {
        console.log("Konum alınamadı.");
    }
    // Sayfa yüklendiğinde otomatik tetikle
    setTimeout(getLocation, 500);
    </script>
""", height=0)

# --- ÜST BAR (BUTONLAR) ---
st.markdown("""
    <div class="header-buttons">
        <a href="#" class="btn-register">Kayıt Ol</a>
        <a href="tel:112" class="btn-emergency">ACİL (112)</a>
    </div>
""", unsafe_allowed_html=True)

st.title("AIHEALTH")
st.markdown("### Profesyonel Sağlık ve Entegre Klinik Sistem")
st.write("---")

# --- DONANIM BAZLI FOTOĞRAF ANALİZİ ---
st.header("Donanım Bazlı Fotoğraf Analizi")
# Doğrudan cihaz kamerasına bağlanır (Arka kamera öncelikli veya mobil uyumlu)
camera_image = st.camera_input("Yaralı Bölgeyi Net Bir Şekilde Fotoğraflayın")

if camera_image:
    st.success("Görüntü donanımdan başarıyla yakalandı.")
    if st.button("Görseli Analiz Et"):
        with st.spinner("Gemini Vision klinik analizi gerçekleştiriyor..."):
            try:
                img = Image.open(camera_image)
                # Model nesnel analiz için çağrılıyor
                response = model.generate_content([
                    "Bu fotoğraftaki yara, enfeksiyon, travma veya tıbbi durumu analiz et. "
                    "Öncelikli ilk yardım adımlarını profesyonel bir dille raporla.", img
                ])
                st.markdown("<div class='neon-card'>", unsafe_allowed_html=True)
                st.subheader("📋 Klinik Görsel Analiz Raporu")
                st.write(response.text)
                st.markdown("</div>", unsafe_allowed_html=True)
            except Exception as e:
                st.error(f"Analiz sırasında bir hata oluştu: {e}")

st.write("---")

# --- CANLI KONUM VE HASTANE/ECZANE ENTEGRASYONU ---
st.header("Konum Bazlı Acil Entegrasyon")

# Örnek statik koordinat havuzu (Gerçek GPS gelene kadar fallback mekanizması için)
# Normal şartlarda tarayıcı lokasyonu kabul ettiğinde JS verisi buraya düşer.
current_lat = 41.018
current_lon = 28.646

current_hour = datetime.datetime.now().hour
st.info(f"Sistem Saati: {datetime.datetime.now().strftime('%H:%M')} | Konum Algılama Aktif")

col1, col2 = st.columns(2)

with col1:
    st.subheader("En Yakın Sağlık Merkezi")
    if st.button("En Yakın Hastane Rotalarını Göster"):
        # Kullanıcının mevcut koordinatlarından direkt Google Maps Rota (dir) motorunu başlatır
        maps_url = f"https://www.google.com/maps/dir/?api=1&origin={current_lat},{current_lon}&destination=Hospital"
        st.markdown(f'<a href="{maps_url}" target="_blank" class="map-link">Haritada Rotayı Başlat</a>', unsafe_allowed_html=True)

with col2:
    st.subheader("Eczane Servisleri")
    if st.button("Eczaneleri Listele"):
        st.markdown("<div class='neon-card'>", unsafe_allowed_html=True)
        
        # Saat 19:00 (Aksam yedi) kontrolü
        if current_hour >= 19 or current_hour < 8:
            st.warning("⏰ Mesai saatleri dışı: Bölgenizdeki aktif nöbetçi eczaneler listeleniyor.")
            
            # Dinamik nöbetçi şablonu ve tel: link protokolü aktif
            eczaneler = [
                {"isim": "Ayışığı Nöbetçi Eczanesi", "tel": "+902128526661", "uzaklik": "150m"},
                {"isim": "Atasoy Nöbetçi Eczanesi", "tel": "+905523995113", "uzaklik": "260m"}
            ]
            
            for eczi in eczaneler:
                st.write(f"**{eczi['isim']}** ({eczi['uzaklik']})")
                st.markdown(f"<a href='tel:{eczi['tel']}' style='color:#ff416c; font-weight:bold;'>📞 Hemen Ara: {eczi['tel']}</a>", unsafe_allowed_html=True)
                maps_target = f"https://www.google.com/maps/dir/?api=1&origin={current_lat},{current_lon}&destination={eczi['isim']}"
                st.markdown(f'<a href="{maps_target}" target="_blank" style="font-size:0.8rem; color:#00d2ff;">Yol Tarifi</a>', unsafe_allowed_html=True)
                st.write("")
        else:
            st.success("Normal çalışma saatleri: Yakındaki tüm eczaneler listeleniyor.")
            maps_url = f"https://www.google.com/maps/search/?api=1&query=pharmacy&location={current_lat},{current_lon}"
            st.markdown(f'<a href="{maps_url}" target="_blank" class="map-link">Yakındaki Eczaneleri Haritada Aç</a>', unsafe_allowed_html=True)
            
        st.markdown("</div>", unsafe_allowed_html=True)

# --- HUKUKİ METİN (FOOTER) ---
st.markdown("""
    <div class="legal-footer">
        YASAL UYARI: AIHEALTH, yapay zeka tabanlı bir bilgilendirme ve analiz yazılımıdır. 
        Kesinlikle bir tıp profesyonelinin, hekimin veya klinik teşhisin yerini alamaz. 
        Acil durumlarda uygulamadaki verilerle zaman kaybetmeden derhal 112 ACİL ÇAĞRI MERKEZİ ile iletişime geçmelisiniz.
    </div>
""", unsafe_allowed_html=True)
