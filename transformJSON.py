import pandas as pd

# Hatalı satırları atlamak için on_bad_lines='skip' parametresi kullanılır
csv_path = "fikralarFinaller5.csv"
df = pd.read_csv(csv_path, on_bad_lines='skip')

# Sütun isimlerini kontrol et
print("Sütunlar:", df.columns)

# Eğer sadece 1 sütun varsa ve ismi farklıysa yeniden adlandır
if df.shape[1] == 1:
    df.columns = ["icerik"]

# JSON olarak kaydet
json_path = "fikralarFinal.json"
df.to_json(json_path, orient="records", force_ascii=False, indent=2)

print(f"{json_path} dosyasına başarıyla dönüştürüldü.")
