import PyPDF2
import pandas as pd
import re

# PDF dosyasının yolunu belirle
pdf_path = "/Users/erenaltin/Documents/School/jokesLLM/fikralar.pdf"  # PDF dosyanın adını doğru yaz

# PDF dosyasını aç ve metni oku
with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

# Metni satırlara böl
lines = text.split("\n")

fikralar = []
current_title = None
current_fikra = []

# Numara ile başlayan satırları başlık olarak tespit eden regex
def is_title(line):
    return bool(re.match(r"^\d+\.\s+.*", line.strip()))

# Başlıktaki numarayı temizleme fonksiyonu
def clean_title(line):
    return re.sub(r"^\d+\.\s*", "", line).strip()

# Satırları analiz ederek başlıkları ve içerikleri ayır
for line in lines:
    line = line.strip()
    
    if is_title(line):  # Eğer numara ile başlıyorsa başlık olarak al
        if current_title and current_fikra:
            fikralar.append({"baslik": current_title, "icerik": " ".join(current_fikra)})

        current_title = clean_title(line)  # Yeni başlık başlar (numarasız)
        current_fikra = []
    else:
        if current_title:  # Başlık varsa içeriği ekle
            current_fikra.append(line)

# Son fıkrayı ekle
if current_title and current_fikra:
    fikralar.append({"baslik": current_title, "icerik": " ".join(current_fikra)})

# Pandas DataFrame'e çevir
df = pd.DataFrame(fikralar)

# CSV olarak kaydet
csv_path = "/Users/erenaltin/Documents/School/jokesLLM/fikralarNasreddin.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")

print("Fıkralar CSV dosyasına kaydedildi:", csv_path)
