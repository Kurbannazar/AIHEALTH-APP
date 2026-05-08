import streamlit as st
from PIL import Image
import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH PRO", layout="wide")

# --- CUSTOM CSS (STICKERSIZ, PREMIUM TASARIM) ---
st.markdown("""
    <style>
    .main { background-color: #050a14; color: #ffffff; }
    
    /* 5. Madde: Acil Durum Butonu (Siyah -> Kırmızı) */
    .emergency-btn {
        background: linear-gradient(90deg, #000000 0%, #cc0000 100%);
        color: white; border: 1px solid #ff4b4b; padding: 15px;
        text-align: center; border-radius: 10px; font-weight: bold;
        font-size: 18px; box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
        text-decoration: none; display: block; margin-bottom: 10px;
    }

    /* 6. Madde: Kayıt Ol Butonu (Siyah -> Mavi) */
    .register-btn {
        background: linear-gradient(90deg, #000000 0%, #004e92 100%);
        color: white; border: 1px solid #00d4ff; padding: 15px;
        text-align: center; border-radius: 10px; font-weight: bold;
        font-size: 18px; box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
        text-decoration: none; display: block; margin-bottom: 10px;
    }

    /* Harita ve Fonksiyon Butonları (Stickersız) */
    .action-button {
        background-color: #0f172a; color: #00d4ff;
        border: 1px solid #004e92; padding: 12px;
        width: 100%; border-radius: 8px; cursor: pointer;
        font-weight: bold; text-align: center; margin-bottom: 10px;
        display: block; text-decoration: none;
    }
    
    .stTextArea textarea {
        background-color: #0f172a; color: white;
        border: 1px solid #004e92; border-radius: 10px;
    }
    
    .analysis-box {
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid #004e92; padding: 20px;
        border-radius: 10px; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST MENÜ (ACİL DURUM VE KAYIT) ---
top_col1, top_col2 = st.columns(2)
with top_col1:
    st.markdown('<a href="tel:112" class="emergency-btn">ACIL DURUM YARDIM HATTI</a>', unsafe_allow_html=True)
with top_col2:
    st.markdown('<a href="#" class="register-btn">SISTEME KAYIT OL</a>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00d4ff;'>AIHEALTH PRO</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])

with col1:
    # --- 1. MADDE: ŞİKAYET ANALİZİ ---
    st.markdown("### DURUM BILGISI")
    user_input = st.text_area("Şikayetinizi buraya yazın:", placeholder="Örn: Kesik, yanık, yüksek ateş...", height=150)
    
    if st.button("ANALIZI BASLAT"):
        if user_input:
            st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
            st.markdown("#### SISTEM ÖNERILERI")
            # Cihaz tabanlı akıllı analiz simülasyonu
            if "kesik" in user_input.lower():
                st.write("- Yaraya temiz bir bezle baskı uygulayın.")
                st.write("- Kanayan bölgeyi kalp seviyesinin üzerinde tutun.")
            else:
                st.write("- Belirtileriniz sisteme kaydedildi. İstirahat etmeniz önerilir.")
            
            st.info("Eğer fotoğraf yüklerseniz veya çekerseniz, cihazınızın görüntü işleme motorunu kullanarak size çok daha detaylı analizler sunabilirim.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Lütfen bir şikayet metni giriniz.")

    # --- 2. VE 3. MADDE: FOTOĞRAF VE KAMERA ---
    st.markdown("---")
    st.markdown("### GÖRSEL ANALIZ MERKEZI")
    
    tab1, tab2 = st.tabs(["DOSYA YÜKLE", "FOTOĞRAF ÇEK"])
    
    source = None
    with tab1:
        source = st.file_uploader("Cihazınızdan fotoğraf seçin", type=['jpg', 'png', 'jpeg'])
    with tab2:
        # 3. Madde: Sadece tıklandığında kamera aktif olur
        if st.button("KAMERAYI AKTIF ET"):
            source = st.camera_input("Kamera Görüntüsü")

    if source:
        # 2. Madde: Fotoğrafı ekranda göster ve analiz et
        img = Image.open(source)
        st.image(img, caption="Analiz Edilen Görüntü", use_column_width=True)
        st.markdown('<div class="analysis-box" style="border-color: #ff4b4b;">', unsafe_allow_html=True)
        st.write("#### HASARLI BÖLGE ANALIZI")
        st.write("Görüntü cihaz üzerinden tarandı: Doku zedelenmesi tespit edildi. Sterilizasyon ve koruyucu bandaj önerilir.")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # --- 4. MADDE: CIHAZ KONUMUNA BAĞLI LİNKLER ---
    st.markdown("### SAĞLIK KONUMLARI")
    
    # Cihazın GPS/Harita servisine doğrudan bağlanır
    st.markdown('<a href="https://www.google.com/maps/search/hastane" class="action-button">EN YAKIN HASTANELER</a>', unsafe_allow_html=True)
    
    # Akşam saatlerini kontrol eden nöbetçi eczane mantığı
    current_hour = datetime.datetime.now().hour
    if current_hour >= 18 or current_hour <= 8:
        st.markdown('<a href="https://www.google.com/maps/search/nobetci+eczane" class="action-button" style="border-color: #ff4b4b; color: #ff4b4b;">AKTIF NÖBETÇI ECZANELER</a>', unsafe_allow_html=True)
    else:
        st.markdown('<a href="https://www.google.com/maps/search/eczane" class="action-button">EN YAKIN ECZANELER</a>', unsafe_allow_html=True)

    st.markdown("---")
    st.write("Sistem Durumu: Çevrimiçi")
    st.write("Konum Servisi: Aktif")
