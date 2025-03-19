import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.frmtr.com/komik-seyler/373213-dunyanin-en-buyuk-fikra-arsivi.html"

headers = {"User-Agent": "Mozilla/5.0"}  
response = requests.get(url, headers=headers)

if response.status_code == 200:
    html_content = response.text
else:
    print("Sayfa yüklenemedi:", response.status_code)
    exit()

soup = BeautifulSoup(html_content, "html.parser")

text_content = soup.get_text()

lines = text_content.split("\n")

fikralar = []
current_title = None
current_fikra = []

for line in lines:
    line = line.strip()
    
    if not line: 
        if current_title and current_fikra:
            fikralar.append({"baslik": current_title, "icerik": " ".join(current_fikra)})
            current_title = None
            current_fikra = []
    else:
        if current_title is None:
            current_title = line  
        else:
            current_fikra.append(line)  

if current_title and current_fikra:
    fikralar.append({"baslik": current_title, "icerik": " ".join(current_fikra)})

for i, fikra in enumerate(fikralar[:5]):
    print(f"Fıkra {i+1}: {fikra['baslik']}\n{fikra['icerik']}\n{'-'*40}")

df = pd.DataFrame(fikralar)

df.to_csv("fikralar.csv", index=False, encoding="utf-8")

print("Fıkralar CSV olarak kaydedildi.")
