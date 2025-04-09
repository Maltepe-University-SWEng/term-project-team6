import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from transformers import pipeline

print("📂 JSON dosyası yükleniyor...")
with open("fikralarFinal.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("🧹 Gereksiz başlık içeren satırlar temizleniyor...")
# "Fıkra Metni" geçen satırları çıkarıyoruz
data = [d for d in data if "Fıkra Metni" not in d["icerik"]]

print("📊 Veriler DataFrame'e aktarılıyor...")
df = pd.DataFrame(data)

print("🔎 Embedding modeli yükleniyor (SentenceTransformer)...")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

print("🧠 Fıkralar vektörleştiriliyor (embedding)...")
embeddings = model.encode(df["icerik"].tolist(), show_progress_bar=True)

print("🔗 KMeans ile kümelere (clusterlara) ayrılıyor...")
kmeans = KMeans(n_clusters=10, random_state=42)
clusters = kmeans.fit_predict(embeddings)
df["cluster"] = clusters

print("🤖 Zero-shot classification modeli yükleniyor...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

kategori_adaylari = ["evlilik", "temel", "keloğlan", "hayvanlar", "okul", "çocuklar", "deli", "nasreddin hoca", "dini"]

print("🏷️ Her fıkraya kategori etiketi tahmin ediliyor...")
tahmin_edilenler = []
for i, metin in enumerate(df["icerik"], 1):
    print(f"  > {i}/{len(df)} fıkra için kategori tahmini yapılıyor...")
    sonuc = classifier(metin, kategori_adaylari)
    tahmin_edilenler.append(sonuc["labels"][0])

df["kategori"] = tahmin_edilenler

print("💾 Kategorili JSON dosyası kaydediliyor...")
df.to_json("fikralar_kategorili.json", orient="records", force_ascii=False, indent=2)

print("✅ İşlem tamam! Sonuç dosyası: 'fikralar_kategorili.json'")
