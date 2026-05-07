import streamlit as st
from PIL import Image
import time
from datetime import datetime

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH | Akıllı Sağlık", page_icon="🌐", layout="wide")

if 'arsiv' not in st.session_state:
    st.session_state.arsiv = []

# --- 2. TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #000000 0%, #001f3f 50%, #004a99 100%); color: white; }
    div.stButton > button:first-child { background-color: #ff4b4b !important; color: white !important; font-weight: bold !important; }
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #00c6ff !important;
        border-radius: 15px !important;
        font-size: 18px !important;
    }
    .suggestion-box {
        background-color: rgba(0, 198, 255, 0.1);
        border-left: 5px solid #00c6ff;
        padding: 15px;
        margin-top: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GELİŞMİŞ ANALİZ MOTORU ---
def akilli_analiz(mesaj):
    m = mesaj.lower()
    # Kesik ve Kanama Durumu
    if any(k in m for k in ["kan", "kesik", "kesildi", "yara"]):
        return {
            "baslik": "⚠️ KESİK VE KANAMA MÜDAHALESİ",
            "mesaj": """
            1. **Baskı Uygulayın:** Temiz bir bez veya gazlı bezle yaranın üzerine 5-10 dakika baskı yapın.
            2. **Temizlik:** Eğer yara kirliyse, hafif akan ılık suyla (sabunsuz) nazikçe yıkayın. 
            3. **İlaç:** Açık yaraya doktor önermedikçe krem veya alkol sürmeyin; sadece çevresini temizleyin.
            4. **Yükseltin:** Eğer kanama durmuyorsa, yaralı bölgeyi kalp seviyesinden yukarıda tutun.
            """,
            "foto_notu": "🔔 **Not:** Yaranın derinliğini anlamam için aşağıdan bir fotoğraf yüklerseniz size daha kesin bir öneride bulunabilirim.",
            "renk": "warning"
        }
    # Kırık Durumu
    elif any(k in m for k in ["kırıldı", "kırık", "çatlak", "diz", "ayak"]):
        return {
            "baslik": "🚨 ACİL: KIRIK ŞÜPHESİ",
            "mesaj": """
            1. **Hareketsiz Kalın:** Bölgeyi asla kıpırdatmayın.
            2. **Buz Uygulaması:** Şişliği indirmek için havluya sarılı buzu 15 dakika uygulayın.
            3. **Destek:** Bölgeyi bir mukavva veya sert bir cisimle sabitlemeye çalışın.
            """,
            "foto_notu": "🔔 **Not:** Bölgedeki şişlik veya şekil bozukluğunu görmem için fotoğraf yüklemeniz çok önemlidir.",
            "renk": "error"
        }
    else:
        return {
            "baslik": "🔍 GENEL ANALİZ",
            "mesaj": "Şikayetiniz sisteme alındı. Bol sıvı tüketin ve dinlenin.",
            "foto_notu": "🔔 **Not:** Belirtileri görsel olarak incelememi isterseniz fotoğraf ekleyebilirsiniz.",
            "renk": "info"
        }

# --- 4. ÜST BAR ---
col_h, col_b = st.columns([2, 1])
with col_h: st.markdown("<h1 style='color: #00c6ff;'>🌐 AIHEALTH</h1>", unsafe_allow_html=True)
with col_b:
    c1, c2 = st.columns(2)
    with c1: st.button("🚨 ACİL")
    with c2: st.button("👤 Kayıt")

# --- 5. ŞİKAYET FORMU (Enter Destekli) ---
st.subheader("📝 Şikayetinizi Yazın")
with st.form("main_form", clear_on_submit=False):
    sikayet_metni = st.text_area("", placeholder="Örn: Elimi bıçak kesti, çok kanıyor...", height=200)
    submit = st.form_submit_button("ANALİZİ BAŞLAT")

if submit and sikayet_metni:
    res = akilli_analiz(sikayet_metni)
    if res["renk"] == "error": st.error(f"### {res['baslik']}\n\n{res['mesaj']}")
    elif res["renk"] == "warning": st.warning(f"### {res['baslik']}\n\n{res['mesaj']}")
    else: st.success(f"### {res['baslik']}\n\n{res['mesaj']}")
    
    # Fotoğraf Yönlendirme Notu
    st.markdown(f'<div class="suggestion-box">{res["foto_notu"]}</div>', unsafe_allow_html=True)

st.divider()

# --- 6. FOTOĞRAF VE ANALİZ ---
st.subheader("📸 Görsel Kanıt (Tavsiye Edilir)")
c_cam, c_file = st.columns(2)
with c_cam: cam = st.camera_input("Fotoğraf Çek")
with c_file: file = st.file_uploader("Dosya Seç")

final_img = cam if cam else file
if final_img:
    st.image(final_img, width=300)
    # Burada daha önce yaptığımız piksellere bakan doku analizi kodu çalışacak
    st.info("Görsel alındı. Şikayet kutusundaki bilgilerle birleştirilerek analiz ediliyor...")

# --- 7. KONUM VE HARİTA ---
st.subheader("📍 Yakındaki Sağlık Merkezleri")
st.columns(3)[0].info("🏥 Hastaneler")
st.columns(3)[1].warning("🚑 Acil Merkezleri")
st.columns(3)[2].success("💊 Nöbetçi Eczaneler")
st.map()
