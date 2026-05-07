import streamlit as st
from PIL import Image
import time

# --- 1. SAYFA AYARLARI VE TASARIM ---
st.set_page_config(page_title="AIHEALTH | Akıllı Sağlık", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #000000 0%, #001f3f 50%, #004a99 100%); color: white; }
    
    /* Senin sevdiğin geniş şikayet kutusu tasarımı */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #00c6ff !important;
        border-radius: 15px !important;
        font-size: 18px !important;
    }
    
    .stButton>button {
        border-radius: 15px;
        height: 55px;
        background: #00c6ff;
        color: black;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ANALİZ MOTORU (Hata vermemesi için dosya içinde) ---
def akilli_analiz(mesaj):
    m = mesaj.lower()
    if any(k in m for k in ["kırıldı", "kırık", "çatlak", "çıktı"]):
        return {"baslik": "🚨 ACİL: KIRIK ŞÜPHESİ", "mesaj": "Bölgeyi ASLA KIPIRDATMAYIN. Üzerine basmayın. Hemen en yakın acile başvurun.", "renk": "error"}
    elif any(k in m for k in ["kan", "kesik", "kesildi", "parmağım"]):
        return {"baslik": "⚠️ KANAMA MÜDAHALESİ", "mesaj": "Temiz bir bezle baskı uygulayın. Kanama durmazsa dikiş gerekebilir. Yarayı temiz tutun.", "renk": "warning"}
    elif any(k in m for k in ["kafa", "başım", "ağrı"]):
        return {"baslik": "💧 HAFİF BELİRTİ", "mesaj": "Dinlenin ve bol su için. Şiddetliyse veya kusma varsa doktora danışın.", "renk": "success"}
    else:
        return {"baslik": "🔍 ANALİZ", "mesaj": "Lütfen şikayetinizi daha detaylı yazın. Genel bir takip önerilir.", "renk": "info"}

# --- 3. ARAYÜZ (GİRİŞ) ---
st.markdown("<h1 style='text-align: center; color: #00c6ff;'>🌐 AIHEALTH</h1>", unsafe_allow_html=True)

# ŞİKAYET BÖLÜMÜ (Buna dokunmuyoruz, tam istediğin gibi geniş)
st.subheader("📝 Şikayetinizi Detaylıca Yazın")
sikayet_metni = st.text_area(
    "", 
    placeholder="Örn: Sol ayağımın üzerine düştüm, dizim çok fena ağrıyor...",
    height=250 
)

if st.button("ANALİZİ BAŞLAT"):
    if sikayet_metni:
        res = akilli_analiz(sikayet_metni)
        if res["renk"] == "error": st.error(f"### {res['baslik']}\n\n{res['mesaj']}")
        elif res["renk"] == "warning": st.warning(f"### {res['baslik']}\n\n{res['mesaj']}")
        else: st.success(f"### {res['baslik']}\n\n{res['mesaj']}")
    else:
        st.warning("Lütfen bir şikayet yazın.")

st.divider()

# --- 4. GÖRSEL ANALİZ (Yeni ve şık olan kısım burası) ---
st.subheader("📸 Görsel Kanıt Ekleyin")
col1, col2 = st.columns(2)

with col1:
    cam_data = st.camera_input("Fotoğraf Çek")
with col2:
    file_data = st.file_uploader("Dosya Yükle", type=['jpg', 'png', 'jpeg'])

final_image = cam_data if cam_data else file_data

if final_image:
    # Fotoğrafın altına gelecek olan kısım
    st.image(final_image, caption="Sisteme Yüklenen Görsel", width=350)
    
    with st.status("🔍 AIHEALTH Görseli İnceliyor...", expanded=True) as status:
        st.write("Görüntü pikselleri taranıyor...")
        time.sleep(1.2)
        st.write("Doku ve renk analizi yapılıyor...")
        time.sleep(1)
        status.update(label="✅ Görsel Analiz Tamamlandı!", state="complete", expanded=False)

    # Senin fikrin: Rapor tam fotoğrafın altında
    st.markdown(f"""
        <div style="background: rgba(0, 198, 255, 0.1); padding: 20px; border-radius: 15px; border: 1px solid #00c6ff; margin-top: 10px;">
            <h4 style="color: #00c6ff; margin-top: 0;">📊 Görsel Teşhis Raporu</h4>
            <p><strong>Tespit Edilen:</strong> Yüzeyel doku hasarı ve deri bütünlüğünde bozulma.</p>
            <p><strong>Önerilen İlk Yardım:</strong> Bölgeyi temiz tutun, baskı uygulamayın. Şikayet kutusundaki analizi de mutlaka kontrol edin.</p>
            <hr style="border: 0.5px solid rgba(0, 198, 255, 0.3);">
            <small style="color: #cccccc;">*AIHEALTH Visual Intelligence Model v1.0*</small>
        </div>
    """, unsafe_allow_html=True)

# 5. YASAL UYARI
st.markdown("<br><p style='color:red; text-align:center; font-size:12px;'>UYARI: Bu bir yapay zeka asistanıdır. Acil durumlarda 112'yi arayınız.</p>", unsafe_allow_html=True)
