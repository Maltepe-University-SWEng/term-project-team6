import PyPDF2
import pandas as pd
import re

pdf_path = "/Users/erenaltin/Documents/School/jokesLLM/fikralar.pdf" 

with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

lines = text.split("\n")

fikralar = []
current_title = None
current_fikra = []

def is_title(line):
    return bool(re.match(r"^\d+\.\s+.*", line.strip()))

def clean_title(line):
    return re.sub(r"^\d+\.\s*", "", line).strip()

for line in lines:
    line = line.strip()
    
    if is_title(line): 
        if current_title and current_fikra:
            fikralar.append({"baslik": current_title, "icerik": " ".join(current_fikra)})

        current_title = clean_title(line)
        current_fikra = []
    else:
        if current_title: 
            current_fikra.append(line)

if current_title and current_fikra:
    fikralar.append({"baslik": current_title, "icerik": " ".join(current_fikra)})

df = pd.DataFrame(fikralar)

csv_path = "/Users/erenaltin/Documents/School/jokesLLM/fikralarNasreddin.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")

print("Fıkralar CSV dosyasına kaydedildi:", csv_path)
