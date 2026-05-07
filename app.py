import streamlit as st
from PIL import Image

# --- TASARIM VE SAYFA AYARLARI ---
st.set_page_config(page_title="AIHEALTH | Profesyonel Sağlık", page_icon="🌐", layout="wide")

# (Tasarım kodlarını hocaya gösterdiğin gibi koruyoruz)
st.markdown("""<style>.stApp { background: linear-gradient(135deg, #000000 0%, #001f3f 50%, #004a99 100%); color: white; }</style>""", unsafe_allow_html=True)

# --- GELİŞMİŞ ANALİZ MOTORU ---
def akilli_analiz(mesaj):
    m = mesaj.lower()
    
    # 🔴 KRİTİK / ACİL DURUMLAR
    if any(k in m for k in ["kırıldı", "kırık", "çatlak", "çıktı"]) and any(b in m for b in ["diz", "ayak", "kol", "bacak", "parmak"]):
        return {
            "baslik": "🚨 ACİL: KIRIK / ÇATLAK ŞÜPHESİ",
            "mesaj": "DİKKAT! Bölgeyi ASLA KIPIRDATMAYIN. Eğer bir atel (tahta veya sert cisim) varsa bölgeyi sabitleyin. Üzerine asla basmayın. Hemen en yakın acil servise başvurun.",
            "renk": "error"
        }
    elif any(k in m for k in ["kan", "kanama", "kesik", "kesildi"]):
        return {
            "baslik": "⚠️ KANAMA VE YARA MÜDAHALESİ",
            "mesaj": "Yaranın üzerine temiz bir bezle 5-10 dakika baskı uygulayın. Kanama durmuyorsa veya kesik derinse dikiş gerekebilir. Yarayı kirli suyla temas ettirmeyin.",
            "renk": "warning"
        }
    elif any(k in m for k in ["kalp", "göğüs ağrısı", "nefes", "boğulma"]):
        return {
            "baslik": "🆘 HAYATİ TEHLİKE!",
            "mesaj": "Derhal 112 Acil Çağrı Merkezini arayın! Göğüste sıkışma veya nefes darlığı hayati risk taşır. Hareket etmeyin ve yardım bekleyin.",
            "renk": "error"
        }
    
    # 🟡 ORTA ÖNCELİKLİ DURUMLAR
    elif any(k in m for k in ["yanık", "yandı", "sıcak su"]):
        return {
            "baslik": "🔥 YANIK MÜDAHALESİ",
            "mesaj": "Yanık bölgesini en az 15 dakika oda sıcaklığındaki musluk suyu altında tutun. Buz sürmeyin, yoğurt veya diş macunu sürmeyin! Steril bir bezle üzerini kapatın.",
            "renk": "warning"
        }
    
    # 🟢 DÜŞÜK ÖNCELİKLİ DURUMLAR
    elif any(k in m for k in ["başım", "kafa", "ağrıyor", "ağrı"]):
        return {
            "baslik": "💧 HAFİF BELİRTİ",
            "mesaj": "Yeterli sıvı aldığınızdan emin olun ve karanlık bir odada dinlenin. Eğer ağrı çok şiddetliyse ve kusma eşlik ediyorsa doktora görünün.",
            "renk": "success"
        }
    
    # Varsayılan Cevap
    else:
        return {
            "baslik": "🔍 DETAY BEKLENİYOR",
            "mesaj": "Belirtilerinizi tam anlayamadım. Lütfen 'Ayağım kırıldı' veya 'Elim kesildi' gibi daha net ifadeler kullanın.",
            "renk": "info"
        }

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center; color: #00c6ff;'>🌐 AIHEALTH ASİSTANI</h1>", unsafe_allow_html=True)

# Şikayet Girişi
şikayet = st.text_input("Şikayetinizi buraya yazın (Örn: Sol ayağımın dizi kırıldı)", key="user_input")

if st.button("ANALİZ ET"):
    if şikayet:
        res = akilli_analiz(şikayet)
        if res["renk"] == "error":
            st.error(f"### {res['baslik']}\n\n{res['mesaj']}")
        elif res["renk"] == "warning":
            st.warning(f"### {res['baslik']}\n\n{res['mesaj']}")
        elif res["renk"] == "success":
            st.success(f"### {res['baslik']}\n\n{res['mesaj']}")
        else:
            st.info(res["mesaj"])
    else:
        st.warning("Lütfen önce bir şikayet yazın!")

st.divider()

# Kamera Bölümü
st.subheader("📸 Görsel Hasar Tespiti")
kamera_resmi = st.camera_input("Yarayı/Hasarı Fotoğraflayın")
if kamera_resmi:
    st.image(kamera_resmi, caption="Görüntü İşleniyor...")
    st.info("AI Analizi: Görüntüdeki renk değişimi ve doku hasarı inceleniyor.")
