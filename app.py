import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH Pro - İlk Yardım Asistanı", page_icon="🚑", layout="centered")

# --- TASARIM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #004aad; color: white; }
    .emergency-box { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 15px; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .success-box { background-color: #28a745; color: white; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- GEMINI API AYARI ---
# Buraya kendi API anahtarını yazmalısın
API_KEY = "BURAYA_GEMINI_API_KEY_YAZILACAK" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- BAŞLIK VE GİRİŞ ---
st.title("🚑 AIHEALTH Pro")
st.subheader("Akıllı İlk Yardım ve Klinik Yönetim Asistanı")

# ACİL DURUM UYARISI
st.markdown('<div class="emergency-box">DİKKAT: Hayati tehlike varsa hemen 112 Acil Servis\'i arayın!</div>', unsafe_allow_html=True)

# --- ANA MENÜ ---
tab1, tab2, tab3 = st.tabs(["🆘 İlk Yardım Asistanı", "📋 Klinik Yönetimi", "ℹ️ Hakkında"])

with tab1:
    st.write("### Belirti veya Durumu Yazın")
    user_input = st.text_input("Örn: Kolumda derin bir kesik var veya bayılan birine ne yapılır?", placeholder="Durumu buraya yazın...")
    
    if st.button("Hızlı Müdahale Adımlarını Getir"):
        if user_input:
            with st.spinner('Hayat kurtarıcı bilgiler hazırlanıyor...'):
                prompt = f"Sen bir ilk yardım uzmanısın. Şu durumda yapılması gerekenleri çok kısa, net ve maddeler halinde (en kritik olan en başta olacak şekilde) anlat: {user_input}. Not: Önce 112'yi aramasını hatırlat."
                response = model.generate_content(prompt)
                st.markdown("### ✅ Yapılması Gerekenler:")
                st.info(response.text)
        else:
            st.warning("Lütfen bir durum belirtin.")

with tab2:
    st.write("### Klinik Takip Paneli")
    col1, col2 = st.columns(2)
    with col1:
        hasta_adi = st.text_input("Hasta Adı Soyadı")
        kan_grubu = st.selectbox("Kan Grubu", ["A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-"])
    with col2:
        randevu_tarihi = st.date_input("Randevu Tarihi")
        notlar = st.text_area("Klinik Notlar")
    
    if st.button("Kaydı Tamamla"):
        st.success(f"{hasta_adi} için kayıt başarıyla oluşturuldu.")

with tab3:
    st.write(f"**Geliştirici:** Kurbannazar Ulashov")
    st.write("**Bölüm:** Sağlık Yönetimi, Altınbaş Üniversitesi")
    st.write("Bu uygulama, yapay zeka desteğiyle ilk yardım farkındalığı yaratmak için tasarlanmıştır.")
