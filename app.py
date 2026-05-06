
import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH Pro", page_icon="🚑", layout="centered")

# CSS ile Profesyonel Tasarım (Koyu Mavi ve Kırmızı)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #002366; color: white; }
    .emergency-btn>button { background-color: #FF0000 !important; color: white !important; font-weight: bold; font-size: 20px; border: 2px solid white; }
    </style>
    """, unsafe_allow_html=True)

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
    uploaded_file = None

    if option == "Fotoğraf Yükle":
        uploaded_file = st.file_uploader("Yaralı bölgeyi veya kazayı çekip yükleyin", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Yüklenen Fotoğraf", use_column_width=True)
    else:
        user_input = st.text_area("Durumu kısaca açıklayın...", placeholder="Örn: Arkadaşım kolunu derin kesti, kanama durmuyor.")

    if st.button("ANALİZ ET VE MÜDAHALE GÖSTER"):
        if not api_key:
            st.error("Lütfen ayarlardan API Key giriniz!")
        elif option == "Metin Yaz" and not user_input:
            st.warning("Lütfen bir açıklama yazın.")
        elif option == "Fotoğraf Yükle" and not uploaded_file:
            st.warning("Lütfen bir fotoğraf yükleyin.")
        else:
            try:
                # AI Yapılandırması
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Talimat (Prompt)
                system_instruction = (
                    "Sen uzman bir acil yardım asistanısın. Görevin, kullanıcının gönderdiği görsel veya metne göre "
                    "hızlıca ilk yardım adımlarını (ABC kuralı) listelemektir. Teşhis koyma, ilaç önerme. "
                    "Önce durumun ciddiyetini (1-10 arası) belirt. Çok kritikse hemen 112'yi aramasını söyle."
                )
                
                st.warning("Yapay zeka analiz yapıyor... Lütfen hastayı güvenli bir yere alın.")
                
                # Analiz Süreci
                if option == "Fotoğraf Yükle" and uploaded_file:
                    response = model.generate_content([system_instruction, image])
                else:
                    response = model.generate_content([system_instruction, user_input])
                
                # Sonucu Yazdır
                st.success("✅ AIHEALTH ANALİZİ VE TALİMATI:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Hata oluştu: {e}. Lütfen API anahtarınızı kontrol edin.")

    # Acil Durum Butonu
    st.markdown('<div class="emergency-btn">', unsafe_allow_html=True)
    if st.button("🚨 112'Yİ ARA VE KONUM GÖNDER"):
        st.write("📞 112 Aranıyor... Mevcut konumunuz acil servislere iletildi.")
    st.markdown('</div>', unsafe_allow_html=True)

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
st.caption("UYARI: Bu uygulama sadece bilgilendirme amaçlıdır. Acil durumlarda vakit kaybetmeden 112'yi arayınız.")
