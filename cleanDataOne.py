import pandas as pd
import re

# 1. Dosyayı yükle
df = pd.read_csv("temizlenmis_fikralar.csv")

# 2. Sütun adlarını normalize et (bazı dosyalarda boşluk olabilir)
df.columns = [col.strip().lower() for col in df.columns]

# 3. İlk 10 satırı atla (başlık, tanıtım, gereksiz içerik olabilir)
df = df.iloc[10:].reset_index(drop=True)

# 4. İçeriği temizle (boş, kısa veya sadece büyük harfli gürültülü verileri sil)
df['icerik'] = df['icerik'].astype(str).str.strip()
df = df[df['icerik'].str.len() > 30]

# 5. Gereksiz karakterleri kaldır (örn: çoklu boşluk, özel karakterler, büyük harf vs.)
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # fazla boşlukları sil
    text = re.sub(r'[“”‘’]', '"', text)
    text = re.sub(r'[^\w\s.,!?]', '', text)

    # Metnin sonunda yer alan "fıkralar123", "fikra_001" gibi şeyleri sil
    text = re.sub(r'(f[iı]kra(lar)?[_]?\d+)$', '', text).strip()

    return text

df['icerik'] = df['icerik'].apply(clean_text)

# 6. İçeriği boş kalanları temizle (emniyet için)
df = df[df['icerik'] != ""]

# 7. Sonuçları kaydet (isteğe bağlı)
df.to_csv("temizlenmis_fikralar2.csv", index=False)

print("Temizleme tamamlandı! Toplam fıkra sayısı:", len(df))
