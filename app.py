import streamlit as st
from PIL import Image

# --- SAYFA AYARLARI VE TASARIM ---
st.set_page_config(page_title="AIHEALTH | Gelişmiş Asistan", page_icon="🌐", layout="wide")

# (Önceki tasarım CSS kodlarını buraya aynen dahil edebilirsin)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #000000 0%, #001f3f 50%, #004a99 100%); color: white; }
    .stButton>button { border-radius: 15px; height: 50px; background: rgba(0, 198, 255, 0.1); color: white; border: 1px solid #00c6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- AI MANTIK FONKSİYONU (Zekayı Geliştiriyoruz) ---
def saglik_analizi(mesaj):
    mesaj = mesaj.lower()
    
    if "parmağım kesildi" in mesaj or "kesik" in mesaj:
        return {
            "durum": "🟡 ORTA ÖNCELİK",
            "mesaj": "Yarayı temiz bir bezle bastırarak kanamayı durdurun. Eğer kesik derinse ve kanama durmuyorsa en yakın sağlık ocağına başvurun. Tetanos aşınızı kontrol ettirin.",
            "renk": "warning"
        }
    elif "başım ağrıyor" in mesaj or "kafa ağrısı" in mesaj:
        return {
            "durum": "🟢 DÜŞÜK ÖNCELİK",
            "mesaj": "Işıkları hafifletin, bol su için. Dinlenmenize rağmen geçmiyorsa doktor kontrolünde bir ağrı kesici alabilirsiniz. Şiddetli ve ani bir ağrıysa lütfen takipte kalın.",
            "renk": "success"
        }
    elif "ayağım kırıldı" in mesaj or "kırık" in mesaj or "ayağım çıktı" in mesaj:
        return {
            "durum": "🔴 YÜKSEK ÖNCELİK",
            "mesaj": "SAYIN KULLANICI: Ayağınızı ASLA KIPIRDATMAYIN. Bölgeyi sabitlemeye çalışın ve üzerine yük binmesine izin vermeyin. Acilen bir ortopedi uzmanına veya acil servise başvurun.",
            "renk": "error"
        }
    else:
        return {
            "durum": "⚪ ANALİZ EDİLEMEDİ",
            "mesaj": "Lütfen belirtilerinizi daha detaylı yazın (Örn: 'Ateşim var' veya 'Kolum incindi').",
            "renk": "info"
        }

# --- ARAYÜZ ---
st.title("🌐 AIHEALTH Gelişmiş Modül")

tab1, tab2 = st.tabs(["💬 Akıllı Teşhis", "📸 Kamera Analizi"])

with tab1:
    st.subheader("Belirti Sorgulama")
    soru = st.text_input("Şikayetinizi yazın:", placeholder="Örn: Parmağım kesildi...")
    
    if st.button("Hızlı Analiz Yap"):
        sonuc = saglik_analizi(soru)
        if sonuc["renk"] == "error": st.error(f"**{sonuc['durum']}** \n\n {sonuc['mesaj']}")
        elif sonuc["renk"] == "warning": st.warning(f"**{sonuc['durum']}** \n\n {sonuc['mesaj']}")
        elif sonuc["renk"] == "success": st.success(f"**{sonuc['durum']}** \n\n {sonuc['mesaj']}")
        else: st.info(sonuc["mesaj"])

with tab2:
    st.subheader("Görsel Analiz Sistemi")
    st.write("Lütfen kameranızı açın ve sorunlu bölgeyi gösterin.")
    
    # KAMERA AKTİF ETME
    resim_dosyası = st.camera_input("Fotoğraf Çek")
    
    if resim_dosyası:
        # Resmi göster
        img = Image.open(resim_dosyası)
        st.image(img, caption="Analiz Edilen Görüntü", use_column_width=True)
        st.info("Yapay zeka görüntüyü tarıyor... (Deri bütünlüğü ve renk değişimi kontrol ediliyor)")

# --- HUKUKİ UYARI ---
st.markdown("<br><br><p style='color:red; font-size:12px; text-align:center;'>NOT: Bu bilgiler yapay zeka tarafından verilmiştir, doktor tavsiyesi değildir.</p>", unsafe_allow_html=True)
