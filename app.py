import streamlit as st

# Uygulama Başlığı ve Logosu
st.set_page_config(page_title="AIHEALTH", page_icon="🌐")

# Mavi Tasarım Ayarları
st.markdown("""
    <style>
    .stButton>button { background-color: #007bff; color: white; border-radius: 10px; font-weight: bold; }
    .emergency { background-color: #ff4b4b !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 AIHEALTH")
st.subheader("Yapay Zeka Sağlık Asistanı")

# Sekmeler (Tablar)
tab1, tab2, tab3 = st.tabs(["💬 AI Sohbet", "🏥 Acil Konum", "📸 Fotoğraf"])

with tab1:
    st.write("Şikayetinizi yazın:")
    st.text_input("Örn: Kolumda kızarıklık var...")
    st.button("AI'ya Sor")

with tab2:
    st.write("Size en yakın hastaneler:")
    st.map() # Harita gösterir

with tab3:
    st.write("Yara veya hasar bölgesini çekin:")
    st.camera_input("Kamerayı Aç")

# Acil Durum Butonu
st.markdown("---")
if st.button("🚨 ACİL DURUM (112)", key="emergency"):
    st.error("Acil durum sinyali gönderiliyor!")

# Hukuki Uyarı
st.markdown("<p style='color:red; font-size:12px;'>YASAL UYARI: Bu uygulama sadece bilgilendirme amaçlıdır. Acil durumlarda 112'yi arayın.</p>", unsafe_allow_html=True)