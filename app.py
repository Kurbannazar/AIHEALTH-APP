import streamlit as st
from PIL import Image
import time
from datetime import datetime

# --- 1. SAYFA AYARLARI VE HAFIZA ---
st.set_page_config(page_title="AIHEALTH | Akıllı Sağlık", page_icon="🌐", layout="wide")

if 'arsiv' not in st.session_state:
    st.session_state.arsiv = []

# --- 2. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #000000 0%, #001f3f 50%, #004a99 100%); color: white; }
    
    /* Üst Bar Tasarımı */
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 10px; }
    
    /* Acil Butonu Stili */
    div.stButton > button:first-child {
        background-color: #ff4b4b !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* Geniş Şikayet Kutusu */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #00c6ff !important;
        border-radius: 15px !important;
        font-size: 18px !important;
    }
    
    /* Analiz Butonu */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #00c6ff !important;
        color: black !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ANALİZ FONKSİYONU ---
def akilli_analiz(mesaj):
    m = mesaj.lower()
    if any(k in m for k in ["kırıldı", "kırık", "çatlak", "çıktı", "diz"]):
        return {"baslik": "🚨 ACİL: KIRIK ŞÜPHESİ", "mesaj": "Bölgeyi ASLA KIPIRDATMAYIN. En yakın acile başvurun.", "renk": "error"}
    elif any(k in m for k in ["kan", "kesik", "kesildi"]):
        return {"baslik": "⚠️ KANAMA MÜDAHALESİ", "mesaj": "Temiz bir bezle baskı uygulayın.", "renk": "warning"}
    elif any(k in m for k in ["kafa", "başım", "ağrı"]):
        return {"baslik": "💧 HAFİF BELİRTİ", "mesaj": "Dinlenin ve bol su için.", "renk": "success"}
    else:
        return {"baslik": "🔍 ANALİZ", "mesaj": "Lütfen şikayetinizi daha detaylı yazın.", "renk": "info"}

# --- 4. ÜST BAR (ACİL DURUM VE KAYIT OL) ---
col_header, col_btns = st.columns([2, 1])
with col_header:
    st.markdown("<h1 style='color: #00c6ff; margin:0;'>🌐 AIHEALTH</h1>", unsafe_allow_html=True)

with col_btns:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚨 ACİL DURUM"):
            st.toast("112 ve Yakınlarınıza Sinyal Gönderiliyor!", icon="🚨")
    with c2:
        st.button("👤 Kayıt Ol")

# --- 5. ŞİKAYET BÖLÜMÜ (ENTER DESTEĞİ İÇİN FORM) ---
st.subheader("📝 Şikayetinizi Yazın")
# st.form kullanarak Enter tuşuyla çalışmasını sağlıyoruz
with st.form("sikayet_formu", clear_on_submit=False):
    sikayet_metni = st.text_area("", placeholder="Şikayetinizi buraya yazıp Enter'a basabilir veya butona tıklayabilirsiniz...", height=200)
    submit_button = st.form_submit_button("ANALİZİ BAŞLAT")

if submit_button:
    if sikayet_metni:
        res = akilli_analiz(sikayet_metni)
        if res["renk"] == "error": st.error(f"### {res['baslik']}\n\n{res['mesaj']}")
        elif res["renk"] == "warning": st.warning(f"### {res['baslik']}\n\n{res['mesaj']}")
        else: st.success(f"### {res['baslik']}\n\n{res['mesaj']}")
    else:
        st.warning("Lütfen bir açıklama yazın.")

st.divider()

# --- 6. GÖRSEL ANALİZ VE ARŞİV ---
st.subheader("📸 Görsel Kanıt")
col1, col2 = st.columns(2)
with col1: cam_data = st.camera_input("Fotoğraf Çek")
with col2: file_data = st.file_uploader("Dosya Yükle", type=['jpg', 'png', 'jpeg'])

final_image = cam_data if cam_data else file_data

if final_image:
    st.image(final_image, width=300)
    with st.status("İnceleniyor...", expanded=False):
        time.sleep(1)
        st.write("Analiz tamamlandı.")
    
    # Arşive ekleme mantığı
    zaman = datetime.now().strftime("%H:%M")
    if not any(a['vakit'] == zaman for a in st.session_state.arsiv):
        st.session_state.arsiv.append({"resim": Image.open(final_image), "vakit": zaman})

# --- 7. KONUM VE SAĞLIK MERKEZLERİ (YENİ) ---
st.divider()
st.subheader("📍 Yakındaki Sağlık Merkezleri")
st.write("Size en yakın acil, hastane ve nöbetçi eczaneler:")

m1, m2, m3 = st.columns(3)
with m1:
    st.info("🏥 **Hastaneler**\n\nSize en yakın 3 hastane listeleniyor.")
with m2:
    st.warning("🚑 **Acil Merkezleri**\n\nYoğunluk oranı düşük merkezler.")
with m3:
    st.success("💊 **Nöbetçi Eczaneler**\n\nBugün açık olan eczaneler.")

# Harita Görünümü (Temsili konum)
st.map() 

# --- 8. ARŞİV ---
with st.expander("📁 Geçmiş Fotoğraflar"):
    for item in reversed(st.session_state.arsiv):
        st.image(item['resim'], width=100, caption=item['vakit'])
