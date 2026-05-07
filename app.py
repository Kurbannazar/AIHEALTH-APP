import streamlit as st
import pandas as pd
import numpy as np

# Sayfa ayarlarını yapalım
st.set_page_config(page_title="AIHEALTH | Cyber-Tech Edition", page_icon="⚡", layout="wide")

# --- NEON & DARK MOD TASARIMI (CSS) ---
st.markdown("""
    <style>
    /* Ana Arka Planı Simsiyah Yapalım */
    .stApp {
        background-color: #0E1117;
        color: #00FBFF; /* Parlak Turkuaz Yazı Tipi */
    }
    
    /* Yan Paneli Koyu Yapalım */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 2px solid #00FBFF;
    }

    /* Kartları Parlatalım */
    div.stAlert {
        background-color: #161B22;
        border: 1px solid #00FBFF;
        box-shadow: 0px 0px 15px #00FBFF;
        color: white;
    }

    /* Parlak Acil Durum Butonu */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        background-color: #0E1117;
        color: #FF003C !important; /* Parlak Neon Kırmızı */
        border: 2px solid #FF003C !important;
        font-weight: bold;
        box-shadow: 0px 0px 10px #FF003C;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #FF003C !important;
        color: white !important;
        box-shadow: 0px 0px 25px #FF003C;
    }

    /* Başlık Parlaması */
    h1 {
        text-shadow: 0px 0px 10px #00FBFF;
        color: #00FBFF;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST BİLGİ ---
st.title("⚡ AIHEALTH : NEXT-GEN MEDICAL AI")
st.write("---")

# --- YAN PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00FBFF;'>KONTROL MERKEZİ</h2>", unsafe_allow_html=True)
    st.write("")
    if st.button("🚨 ACİL DURUM SİNYALİ (112)"):
        st.snow() # Ekranda efekt çıksın
        st.error("ACİL DURUM MODU AKTİF: Konum Bilgisi Gönderiliyor...")
    
    st.write("")
    menu = st.selectbox("Erişim Noktası", ["📊 Sistem Özeti", "🧠 AI Tanı Analizi", "🏥 Yakın Hastaneler", "📖 İlk Yardım Arşivi"])

# --- MODÜLLER ---

if menu == "📊 Sistem Özeti":
    st.subheader("Hoş Geldiniz, Kurbannazar")
    col1, col2, col3 = st.columns(3)
    col1.metric("Sistem Gücü", "98%", "+2%")
    col2.metric("AI Güven Skoru", "99.8", "Max")
    col3.metric("Bölge", "Global / GPS")
    
    st.info("Sistem şu an tüm dünyada aktiftir. GPS üzerinden en yakın birimleri tarar.")

elif menu == "🧠 AI Tanı Analizi":
    st.subheader("🧠 Yapay Zeka Derin Analiz")
    text = st.text_area("Analiz için veri girin:", placeholder="Şikayetlerinizi buraya yazın...")
    if st.button("ANALİZİ BAŞLAT"):
        st.write("📡 Bulut sunuculara bağlanılıyor...")
        st.progress(85)
        st.success("Analiz Sonucu: Sistemsel bir risk saptanmadı. Belirtiler yorgunluk kaynaklı olabilir.")

elif menu == "🏥 Yakın Hastaneler":
    st.subheader("🏥 En Yakın Sağlık Kuruluşları (GPS)")
    st.write("Konumunuza en yakın hastaneler harita üzerinde parlıyor.")
    
    # Bu kısım rastgele noktalar üretir ama haritayı konumuna odaklar
    map_data = pd.DataFrame(
        np.random.randn(5, 2) / [50, 50] + [41.00, 28.97], # İstanbul genel koordinatı
        columns=['lat', 'lon']
    )
    st.map(map_data)

elif menu == "📖 İlk Yardım Arşivi":
    st.subheader("📖 Dijital İlk Yardım Rehberi")
    with st.expander("🧪 Kimyasal Yanıklar"):
        st.write("Bol su ile yıkayın, alanı steril tutun.")
    with st.expander("🦴 Kırık ve Çıkıklar"):
        st.write("Bölgeyi sabitleyin, hareket ettirmeyin.")
