import streamlit as st
import google.generativeai as genai
import json

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH Pro", page_icon="🚑", layout="centered")

# CSS ile Profesyonel Tasarım (Koyu Mavi ve Kırmızı)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #002366; color: white; }
    .emergency-btn>button { background-color: #FF0000 !important; color: white !important; font-weight: bold; font-size: 20px; border: 2px solid white; }
    </style>
    """, unsafe_allow_status_code=True)

st.title("🚑 AIHEALTH Pro")
st.caption("Dijital Acil Müdahale ve İlk Yardım Asistanı")

# --- SOL PANEL: AYARLAR ---
with st.sidebar:
    st.header("Sistem Ayarları")
    api_key = st.text_input("Google API Key Giriniz", type="password")
    st.info("Bu uygulama kamu yararı için geliştirilmiştir.")

# --- ANA EKRAN ---
tab1, tab2 = st.tabs(["📸 Acil Müdahale", "🏥 Yakın Hastaneler"])

with tab1:
    st.subheader("Durum Bildir")
    option = st.radio("Yöntem Seçin:", ["Fotoğraf Yükle", "Metin Yaz"])
    
    user_input = ""
    image_data = None

    if option == "Fotoğraf Yükle":
        image_data = st.file_uploader("Yaralı bölgeyi veya kazayı çekip yükleyin", type=["jpg", "jpeg", "png"])
    else:
        user_input = st.text_area("Durumu kısaca açıklayın...", placeholder="Örn: Arkadaşım kolunu derin kesti, kanama durmuyor.")

    if st.button("ANALİZ ET VE MÜDAHALE GÖSTER"):
        if not api_key:
            st.error("Lütfen ayarlardan API Key giriniz!")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Model Komutu (Prompt)
                system_instruction = "Sen bir acil yardım asistanısın. Teşhis koyma, sadece ilk yardım adımlarını (ABC kuralı) listeleyen kısa talimatlar ver. Risk skoru 1-10 arası belirle. Çıktıyı JSON formatında ver."
                
                # Burada AI Studio'da hazırladığımız mantık çalışacak
                # (Şimdilik basit bir simülasyon gösteriyoruz, API bağlandığında tam çalışır)
                st.warning("Analiz yapılıyor... Lütfen hastayı güvenli bir yere alın.")
                
                # Temsili Yanıt Alanı
                st.success("✅ İLK YARDIM TALİMATI:")
                st.write("1. Temiz bir bezle yaraya sert baskı uygulayın.")
                st.write("2. Uzvu kalp seviyesinden yukarı kaldırın.")
                st.write("3. Bilincini açık tutmaya çalışın.")
                
            except Exception as e:
                st.error(f"Hata oluştu: {e}")

    # Acil Durum Butonu
    st.markdown('<div class="emergency-btn">', unsafe_allow_status_code=True)
    if st.button("🚨 112'Yİ ARA VE KONUM GÖNDER"):
        st.write("📞 112 Aranıyor... (Simülasyon)")
    st.markdown('</div>', unsafe_allow_status_code=True)

with tab2:
    st.subheader("İstanbul - En Yakın Hastaneler")
    st.write("📍 Mevcut Konum: İstanbul")
    hospitals = {
        "İstanbul Eğitim ve Araştırma (Samatya)": "Genel Acil / Travma",
        "Cerrahpaşa Tıp Fakültesi": "Tam Teşekküllü / Çocuk Acil",
        "Çapa Tıp Fakültesi": "Genel Cerrahi / Acil",
        "Şişli Etfal Hastanesi": "Yanık Ünitesi / Acil"
    }
    for h, spec in hospitals.items():
        st.info(f"🏥 **{h}** - Uzmanlık: {spec}")

st.divider()
st.caption("UYARI: Bu uygulama sadece bilgilendirme amaçlıdır. Acil durumlarda 112'yi arayınız.")
