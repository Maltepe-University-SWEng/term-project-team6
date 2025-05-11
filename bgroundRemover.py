from rembg import remove
from PIL import Image
import os

def remove_background_from_all_jpgs(folder_path):
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, file)
            file_name, _ = os.path.splitext(file)
            output_path = os.path.join(folder_path, file_name + ".png")

            try:
                input_image = Image.open(full_path)
                output_image = remove(input_image)
                output_image.save(output_path)
                print(f"✔ {file} → {file_name}.png (arka plan kaldırıldı)")
            except Exception as e:
                print(f"❌ Hata oluştu ({file}): {e}")

# Kullanım örneği: bu satırı kendi klasörüne göre değiştir
remove_background_from_all_jpgs("/Users/erenaltin/Desktop/fotoğraflar")
