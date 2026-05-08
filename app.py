def get_aihealth_response(user_problem):
    # Gemini'yi profesyonelleştiren o özel komut (Prompt)
    prompt = f"""
    Sen AIHEALTH profesyonel ilkyardım asistanısın. 
    Kullanıcının şikayeti: "{user_problem}"
    
    KURALLAR:
    1. ASLA genel geçer 'su iç', 'dinlen' gibi boş tavsiyeler verme.
    2. Eğer durum bir kesik, yanık, zehirlenme veya darbe ise saniyeler önemlidir.
    3. Cevabını şu formatta ver:
       - 🚨 **ACİLİYET DURUMU:** (Kritik / Orta / Hafif)
       - 🛠 **HEMEN YAPILMASI GEREKEN:** (Madde madde, kısa ve net)
       - ⚠️ **ASLA YAPILMAMASI GEREKEN:** (Yanlış bilinen doğrular)
       - 🏥 **Hastaneye gidilmeli mi?** (Evet/Hayır ve nedeni)
    """
    # Burada model.generate_content(prompt) çalışacak
    return response

# --- ARAYÜZDEKİ DEĞİŞİKLİK ---
if st.button("ANALİZ ET VE KAYDET"):
    with st.spinner('AIHEALTH Analiz Ediyor...'):
        # Yapay zeka burada devreye giriyor
        response = get_aihealth_response(user_input)
        
        # Eğer kesik gibi kritik bir durumsa ekranı kırmızıyla vurgula
        if "kesik" in user_input.lower() or "kan" in user_input.lower():
            st.error("### 🚨 KRİTİK MÜDAHALE GEREKLİ")
        
        st.markdown(f"""
            <div style="background-color: #1a1c23; border: 2px solid #00d4ff; padding: 20px; border-radius: 15px;">
                {response}
            </div>
        """, unsafe_allow_html=True)
