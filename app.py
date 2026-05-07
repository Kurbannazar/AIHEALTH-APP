import streamlit as st

# Uygulama sayfa ayarları
st.set_page_config(page_title="AIHEALTH Pro", page_icon="🚑", layout="centered")

# --- PROFESYONEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 15px; height: 3.5em; background-color: #007bff; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #0056b3; border: none; }
    div[data-testid="stMetricValue"] { font-size: 20px; color: #d9534f; }
    .sidebar .sidebar-content { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3004/3004451.png", width=100)
    st.title("AIHEALTH")
    st.write("Cebinizdeki Sağlık Rehberi")
    st.markdown("---")
    menu = st.radio("Menü", ["🏠 Ana Sayfa", "🤖 AI Sohbet", "📍 En Yakın Hastane", "🆘 İlk Yardım"])
    st.markdown("---")
    if st.button("🚨 ACİL DURUM: 112"):
        st.error("112 Acil Servis aranıyor... (Simüle edildi)")

# --- ANA SAYFA ---
if menu == "🏠 Ana Sayfa":
    st.title("Hoş Geldiniz, Kurbannazar")
    st.write("Bugün size nasıl yardımcı olabilirim?")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Sistem Durumu", value="Aktif")
    with col2:
        st.metric(label="AI Analiz", value="Hazır")

    st.info("Bilgi: Belirtilerinizi yazmak için 'AI Sohbet' sekmesine geçebilirsiniz.")

# --- AI SOHBET ---
elif menu == "🤖 AI Sohbet":
    st.subheader("🤖 Yapay Zeka Destekli Belirti Analizi")
    st.write("Lütfen şikayetinizi detaylıca yazın.")
    user_input = st.text_area("Örn: Şiddetli baş ağrısı ve ışığa duyarlılık var...", height=150)
    if st.button("Analizi Başlat"):
        with st.spinner('Analiz ediliyor...'):
            st.success("Analiz Tamamlandı: Belirtileriniz migren ile uyumlu görünüyor. Lütfen bir nöroloğa danışın.")
            st.warning("Not: Bu bir teşhis değil, sadece bilgilendirmedir.")

# --- HARİTA ---
elif menu == "📍 En Yakın Hastane":
    st.subheader("📍 Yakınımdaki Sağlık Kuruluşları")
    st.write("Mevcut konumunuza en yakın hastaneler listeleniyor.")
    st.map() # Harita fonksiyonu

# --- İLK YARDIM ---
elif menu == "🆘 İlk Yardım":
    st.subheader("🆘 Temel İlk Yardım Rehberi")
    search = st.text_input("Konu Ara (Örn: Kanama, Bayılma)")
    
    with st.expander("🔥 Yanık Durumunda"):
        st.write("Bölgeyi 15-20 dakika soğuk su altında tutun. Krem sürmeyin.")
    with st.expander("🩸 Kanama Durumunda"):
        st.write("Yaranın üzerine temiz bir bezle bastırın ve bölgeyi yukarı kaldırın.")