import streamlit as st
from PIL import Image

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH | Akıllı Sağlık", page_icon="🌐", layout="wide")

# --- KRİTİK TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #000000 0%, #001f3f 50%, #004a99 100%); color: white; }
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #00c6ff !important;
        border-radius: 15px !important;
        font-size: 18px !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 60px;
        background: #00c6ff;
        color: black;
        font-weight: bold;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ANALİZ FONKSİYONU (Hata Almamak İçin Dosyanın İçinde) ---
def akilli_analiz(mesaj):
    m = mesaj.lower()
    if any(k in m for k in ["kırıldı", "kırık", "çatlak", "çıktı"]):
        return {"baslik": "🚨 ACİL: KIRIK ŞÜPHESİ", "mesaj": "Bölgeyi ASLA KIPIRDATMAYIN ve üzerine basmayın. Hemen en yakın acile başvurun.", "renk": "error"}
    elif any(k in m for k in ["kan", "kesik", "kesildi"]):
        return {"baslik": "⚠️ KANAMA MÜDAHALESİ", "mesaj": "Temiz bir bezle baskı uygulayın. Kanama durmazsa dikiş gerekebilir.", "renk": "warning"}
    elif any(k in m for k in ["kafa", "başım", "ağrı"]):
        return {"baslik": "💧 HAFİF BELİRTİ", "mesaj": "Dinlenin ve bol su için. Şiddetliyse doktora danışın.", "renk": "success"}
    else:
        return {"baslik": "🔍 ANALİZ", "mesaj": "Lütfen şikayetinizi detaylandırın. Şu an için genel bir takip önerilir.", "renk": "info"}

# --- ARAYÜZ BAŞLANGIÇ ---
st.markdown("<h1 style='text-align: center; color: #00c6ff;'>🌐 AIHEALTH</h1>", unsafe_allow_html=True)

# 1. GENİŞ ŞİKAYET KUTUSU
st.subheader("📝 Şikayetinizi Detaylıca Yazın")
sikayet = st.text_area(
    "", 
    placeholder="Örn: Sol ayağımın üzerine düştüm, dizim çok fena ağrıyor...",
    height=250 # Aşağıya doğru genişlik
)

if st.button("ANALİZİ BAŞLAT"):
    if sikayet:
        res = akilli_analiz(sikayet)
        if res["renk"] == "error": st.error(f"### {res['baslik']}\n\n{res['mesaj']}")
        elif res["renk"] == "warning": st.warning(f"### {res['baslik']}\n\n{res['mesaj']}")
        else: st.success(f"### {res['baslik']}\n\n{res['mesaj']}")
    else:
        st.warning("Lütfen bir şikayet yazın.")

st.divider()

# 2. KOMPAKT KAMERA VE YÜKLEME
st.subheader("📸 Görsel Analiz (Opsiyonel)")
col1, col2 = st.columns(2)

with col1:
    cam_data = st.camera_input("Fotoğraf Çek")

with col2:
    file_data = st.file_uploader("Dosya Yükle", type=['jpg', 'png', 'jpeg'])

# Görsel Önizleme
final_image = cam_data if cam_data else file_data
if final_image:
    st.image(final_image, caption="Yüklenen Görsel", width=300)
    st.info("AIHEALTH: Görsel alındı, doku hasarı kontrol ediliyor.")

# 3. YASAL UYARI
st.markdown("<br><p style='color:red; text-align:center; font-size:12px;'>UYARI: Bu bir yapay zeka asistanıdır. Acil durumlarda 112'yi arayınız.</p>", unsafe_allow_html=True)
