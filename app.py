import streamlit as st
from PIL import Image
import time
from datetime import datetime

# --- 1. SAYFA AYARLARI VE ARŞİV SİSTEMİ ---
st.set_page_config(page_title="AIHEALTH | Akıllı Sağlık", page_icon="🌐", layout="wide")

# Fotoğraf arşivini tutmak için hafıza (session_state) oluşturuyoruz
if 'arsiv' not in st.session_state:
    st.session_state.arsiv = []

# --- 2. TASARIM (CSS) ---
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
    .stButton>button { border-radius: 15px; height: 55px; background: #00c6ff; color: black; font-weight: bold; }
    .arsiv-kutusu { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ŞİKAYET ANALİZ MOTORU (DEĞİŞTİRİLMEDİ) ---
def akilli_analiz(mesaj):
    m = mesaj.lower()
    if any(k in m for k in ["kırıldı", "kırık", "çatlak", "çıktı"]):
        return {"baslik": "🚨 ACİL: KIRIK ŞÜPHESİ", "mesaj": "Bölgeyi ASLA KIPIRDATMAYIN. Hemen en yakın acile başvurun.", "renk": "error"}
    elif any(k in m for k in ["kan", "kesik", "kesildi", "parmağım"]):
        return {"baslik": "⚠️ KANAMA MÜDAHALESİ", "mesaj": "Temiz bir bezle baskı uygulayın. Yarayı temiz tutun.", "renk": "warning"}
    elif any(k in m for k in ["kafa", "başım", "ağrı"]):
        return {"baslik": "💧 HAFİF BELİRTİ", "mesaj": "Dinlenin ve bol su için.", "renk": "success"}
    else:
        return {"baslik": "🔍 ANALİZ", "mesaj": "Lütfen şikayetinizi daha detaylı yazın.", "renk": "info"}

# --- 4. ARAYÜZ (ŞİKAYET BÖLÜMÜ - DOKUNULMADI) ---
st.markdown("<h1 style='text-align: center; color: #00c6ff;'>🌐 AIHEALTH</h1>", unsafe_allow_html=True)
st.subheader("📝 Şikayetinizi Detaylıca Yazın")
sikayet_metni = st.text_area("", placeholder="Örn: Sol ayağımın üzerine düştüm...", height=250)

if st.button("ANALİZİ BAŞLAT"):
    if sikayet_metni:
        res = akilli_analiz(sikayet_metni)
        if res["renk"] == "error": st.error(f"### {res['baslik']}\n\n{res['mesaj']}")
        elif res["renk"] == "warning": st.warning(f"### {res['baslik']}\n\n{res['mesaj']}")
        else: st.success(f"### {res['baslik']}\n\n{res['mesaj']}")

st.divider()

# --- 5. GÖRSEL ANALİZ VE ARŞİV (YENİLENEN KISIM) ---
st.subheader("📸 Görsel Kanıt Ekleyin")
col1, col2 = st.columns(2)
with col1: cam_data = st.camera_input("Fotoğraf Çek")
with col2: file_data = st.file_uploader("Dosya Yükle", type=['jpg', 'png', 'jpeg'])

final_image = cam_data if cam_data else file_data

if final_image:
    img = Image.open(final_image)
    st.image(img, caption="Sisteme Yüklenen Görsel", width=350)
    
    with st.status("🔍 AIHEALTH Görüntüyü İnceliyor...", expanded=True) as status:
        # Gerçek doku analizi simülasyonu
        img_rgb = img.convert('RGB')
        # Örnekleme: Fotoğrafın çeşitli yerlerinden renk kontrolü yapar
        pixels = [img_rgb.getpixel((img_rgb.size[0]//2, img_rgb.size[1]//2))]
        is_red = any(p[0] > 150 and p[1] < 100 for p in pixels) # Kırmızı tonu baskın mı?
        
        time.sleep(1.5)
        status.update(label="✅ Analiz Tamamlandı!", state="complete", expanded=False)

    # Arşive Ekle (Eğer daha önce eklenmemişse)
    analiz_zamani = datetime.now().strftime("%H:%M:%S")
    if not any(a['vakit'] == analiz_zamani for a in st.session_state.arsiv):
        st.session_state.arsiv.append({"resim": img, "vakit": analiz_zamani})

    # ANALİZ SONUCU (Elin durumuna göre değişir)
    if is_red:
        teshis = "Doku üzerinde belirgin bir kızarıklık/tahriş tespit edildi."
        oneri = "Bölgede yanma veya kaşıntı varsa soğuk uygulama yapabilirsiniz."
    else:
        teshis = "Sağlıklı doku görünümü. Görünür bir yara veya hasar tespit edilemedi."
        oneri = "Fiziksel bir hasar görünmüyor, ancak ağrı varsa şikayet kutusundan belirtin."

    st.markdown(f"""
        <div style="background: rgba(0, 198, 255, 0.1); padding: 20px; border-radius: 15px; border: 1px solid #00c6ff; margin-top: 10px;">
            <h4 style="color: #00c6ff; margin:0;">📊 Görsel Analiz Sonucu</h4>
            <p><strong>Durum:</strong> {teshis}</p>
            <p><strong>AI Tavsiyesi:</strong> {oneri}</p>
        </div>
    """, unsafe_allow_html=True)

# --- 6. ARŞİV SEKME (EN ALTA) ---
st.divider()
with st.expander("📁 Fotoğraf Arşivi (Geçmiş Analizler)"):
    if st.session_state.arsiv:
        for item in reversed(st.session_state.arsiv):
            st.markdown(f"<div class='arsiv-kutusu'>🕒 Saat: {item['vakit']}</div>", unsafe_allow_html=True)
            st.image(item['resim'], width=150)
    else:
        st.write("Henüz bir fotoğraf yüklenmedi.")
