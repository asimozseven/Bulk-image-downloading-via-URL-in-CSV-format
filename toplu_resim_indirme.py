import os
import requests
import csv
from urllib.parse import urlparse

def download_images_from_csv(save_folder):
    csv_file = "url.csv"  # CSV dosyasının adı

    # İndirme klasörünü oluştur
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # CSV dosyasını oku ve resimleri indir
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Satır boş değilse
                    url = row[0].strip()
                    try:
                        # URL'den dosya adını al
                        file_name = os.path.basename(urlparse(url).path)
                        save_path = os.path.join(save_folder, file_name)

                        # Resmi indir
                        response = requests.get(url, stream=True)
                        response.raise_for_status()  # Hata kontrolü
                        
                        # Resmi kaydet
                        with open(save_path, 'wb') as img_file:
                            for chunk in response.iter_content(1024):
                                img_file.write(chunk)
                        print(f"Resim indirildi: {save_path}")
                    except Exception as e:
                        print(f"Resim indirilemedi ({url}): {e}")
    except FileNotFoundError:
        print(f"CSV dosyası bulunamadı: {csv_file}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    # İndirme klasörünü belirt
    save_folder = "indirilen_resimler"

    # Resimleri indir
    download_images_from_csv(save_folder)
    print("İşlem tamamlandı.")
