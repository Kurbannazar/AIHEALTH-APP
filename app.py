import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH - Profesyonel Asistan", layout="wide")

# --- PREMIUM TEMA (SİYAH-MAVİ) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button {
        background: linear-gradient(45deg, #000428, #004e92);
        color: white; border-radius: 12px; border: 1px solid #00d4ff;
        padding: 15px; font-weight: bold; width: 100%;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    .stTextArea textarea { background-color: #161b22; color: white; border: 1px solid #004e92; border-radius: 10px; }
    .emergency-card { background: #1c1f26; border-left: 5px solid #ff4b4b; padding: 20px; border-radius: 10px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST BAŞLIK ---
st.title("🌐 AIHEALTH")
st.markdown("### Akıllı İlkyardım ve Sağlık Rehberi")
st.write("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### 📝 Şikayetinizi Yazın")
    user_input = st.text_area("", placeholder="Örn: Elimi derin kestim, kanıyor...", height=150)
    
    st.markdown("#### 📸 Görsel Yükle")
    uploaded_file = st.file_uploader("Yara fotoğrafı seçin", type=['jpg', 'png', 'jpeg'])

    if st.button("ANALİZ ET VE KAYDET"):
        if user_input:
            with st.spinner('AIHEALTH analiz ediyor...'):
                # ÖZEL MANTIK: Kesik uyarısı
                if "kesik" in user_input.lower() or "kan" in user_input.lower():
                    st.markdown("""
                        <div class="emergency-card">
                            <h3>🚨 ACİL MÜDAHALE GEREKLİ</h3>
                            <p><b>1. ADIM:</b> Temiz bir bezle yaranın üzerine 5 dakika boyunca baskı uygulayın.</p>
                            <p><b>2. ADIM:</b> Kanayan bölgeyi kalbinizden yukarıda tutun.</p>
                            <p><b>3. ADIM:</b> Kanama durmuyorsa hemen en yakın sağlık kuruluşuna gidin.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("Analiz tamamlandı. (Gemini API bağlandığında buraya detaylı cevap gelecek)")
        else:
            st.warning("Lütfen bir şikayet belirtin.")

with col2:
    st.markdown("#### 🏥 Hızlı Erişim")
    st.markdown("""
        <a href="https://www.google.com/maps/search/hastane" target="_blank"><button style="width:100%; padding:10px; margin-bottom:10px; cursor:pointer;">🏥 En Yakın Hastaneler</button></a>
        <a href="https://www.google.com/maps/search/eczane" target="_blank"><button style="width:100%; padding:10px; cursor:pointer;">💊 Nöbetçi Eczaneler</button></a>
    """, unsafe_allow_html=True)
    
    st.info("💡 Unutmayın: Bu bir yardımcıdır, tıbbi teşhis koymaz. Acil durumlarda 112'yi arayın.")
