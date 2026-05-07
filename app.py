import streamlit as st
from PIL import Image

# --- TASARIM (CSS) ---
# Kutuları daha belirgin ve şık yapmak için küçük dokunuşlar
st.markdown("""
    <style>
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #00c6ff !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00c6ff;'>🌐 AIHEALTH ASİSTANI</h1>", unsafe_allow_html=True)

# --- 1. ŞİKAYET BÖLÜMÜ (Geniş ve Aşağı Doğru Uzun) ---
st.subheader("📝 Şikayetiniz Nedir?")
# height=200 yaparak kutuyu aşağıya doğru genişlettik
sikayet = st.text_area(
    "Lütfen nasıl hissettiğinizi veya yaralanmanın nasıl olduğunu detaylıca anlatın:", 
    placeholder="Örn: Sol ayağımın üzerine düştüm, şu an dizim çok ağrıyor ve şişmeye başladı. Hareket ettiremiyorum...",
    height=200
)

if st.button("ANALİZİ BAŞLAT"):
    if sikayet:
        # Daha önce yazdığımız 'akilli_analiz' fonksiyonunu burada çağırıyoruz
        from logic import akilli_analiz # Eğer fonksiyon farklı dosyadaysa
        res = akilli_analiz(sikayet) 
        
        st.markdown(f"### {res['baslik']}")
        if res["renk"] == "error": st.error(res["mesaj"])
        elif res["renk"] == "warning": st.warning(res["mesaj"])
        else: st.success(res["mesaj"])
    else:
        st.warning("Analiz için lütfen bir açıklama yazın.")

st.divider()

# --- 2. KAMERA VE DOSYA YÜKLEME (Daha Küçük ve Yan Yana) ---
st.subheader("📸 Görsel Kanıt Ekleyin")
col1, col2 = st.columns(2)

with col1:
    # Fotoğraf Çekme (Küçük ve sadece buton gibi görünecek)
    cam_data = st.camera_input("Fotoğraf Çek", label_visibility="visible")

with col2:
    # Dosya Yükleme (Klasik yükleme kutusu)
    file_data = st.file_uploader("Galeriden Seç", type=['jpg', 'png', 'jpeg'])

# Görsel önizleme (Ekranı kaplamaması için boyutunu sınırladık)
final_image = cam_data if cam_data else file_data

if final_image:
    st.image(final_image, caption="Yüklenen Görsel", width=250)
    st.info("AIHEALTH: Görsel başarıyla alındı. Teşhis için analiz ediliyor...")
