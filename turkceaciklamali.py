import numpy as np
import matplotlib.pyplot as plt
import logging
from datetime import datetime
from tqdm import tqdm  # tqdm kütüphanesini ekleyin

# Yeşil renk kodları
GREEN = '\033[92m'
RESET = '\033[0m'

# Logger yapılandırması
logging.basicConfig(filename='logdosyasi.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('my_logger')

def print_green(message):
    print(f"{GREEN}{message}{RESET}")

def input_green(prompt):
    return input(f"{GREEN}{prompt}{RESET}")

# İki şehir arasındaki mesafeyi hesaplama
def mesafe(sehir1, sehir2):
    return np.linalg.norm(sehir1 - sehir2)

try:
    print_green("--------------------------------------------------")
    print_green("Simulated Annealing for Traveling Salesman Problem")
    print_green("----------Created by [enesdilaversahin]----------")
    print_green("")
    # Kullanıcıdan parametreleri alma
    sehir_sayisi = int(input_green("Şehir sayısını girin: "))
    baslangic_sicaklik = float(input_green("Başlangıç sıcaklığını girin: "))
    soguma_orani = float(input_green("Soğuma oranını girin (0'dan büyük ve 1'den küçük olmalı): "))
    durdurma_sicaklik = 1e-3

    # Şehirleri oluşturma fonksiyonu
    def sehirler_olustur(sayi):
        return np.random.rand(sayi, 2) * 50  # Şehirleri 0-50 arasında oluştur

    # Benzetim tavlama algoritması (örnek bir implementasyon)
    def benzetim_tavlama(sehirler, baslangic_sicaklik, soguma_orani, durdurma_sicaklik):
        n = len(sehirler)
        en_iyi_tur = list(range(n))
        np.random.shuffle(en_iyi_tur)
        en_iyi_mesafe = float('inf')
        mesafeler = []

        sicaklik = baslangic_sicaklik
        iteration = 0

        # 'tqdm' ile yükleme çubuğu oluşturma
        with tqdm(total=10000, desc=f"{GREEN}Simülasyon İlerleme{RESET}") as pbar:
            while sicaklik > durdurma_sicaklik:
                for _ in range(100):
                    # Rastgele iki şehir seç
                    a, b = np.random.randint(0, n, 2)
                    yeni_tur = en_iyi_tur[:]
                    yeni_tur[a], yeni_tur[b] = yeni_tur[b], yeni_tur[a]
                    
                    # Mesafe hesapla
                    eski_mesafe = sum(mesafe(sehirler[en_iyi_tur[i]], sehirler[en_iyi_tur[i - 1]]) for i in range(n))
                    yeni_mesafe = sum(mesafe(sehirler[yeni_tur[i]], sehirler[yeni_tur[i - 1]]) for i in range(n))
                    
                    if yeni_mesafe < en_iyi_mesafe or np.random.rand() < np.exp((eski_mesafe - yeni_mesafe) / sicaklik):
                        en_iyi_tur = yeni_tur
                        en_iyi_mesafe = yeni_mesafe
                    
                    mesafeler.append(en_iyi_mesafe)
                    
                sicaklik *= soguma_orani
                iteration += 1
                pbar.update(100)  # Her iterasyonda yükleme çubuğunu güncelleme
        
        return en_iyi_tur, en_iyi_mesafe, mesafeler

    # Şehirleri oluşturma
    sehirler = sehirler_olustur(sehir_sayisi)

    # İlerleme mesajı
    print_green("Simülasyon başlatılıyor. Lütfen bekleyin...")
    logger.info("Simülasyon başlatılıyor. Lütfen bekleyin...")

    # Benzetim tavlama algoritmasını çalıştırma
    en_iyi_tur, en_iyi_mesafe, mesafeler = benzetim_tavlama(sehirler, baslangic_sicaklik, soguma_orani, durdurma_sicaklik)

    # Tarih ve saat bilgisini al
    simulasyon_zamani = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Sonuçları çizme
    plt.figure(figsize=(15, 7))

    # Şehirleri ve en iyi turu gösterme
    plt.subplot(1, 2, 1)
    plt.scatter(sehirler[:, 0], sehirler[:, 1], c='red')
    tur_sehirler = np.array([sehirler[i] for i in en_iyi_tur + [en_iyi_tur[0]]])
    plt.plot(tur_sehirler[:, 0], tur_sehirler[:, 1], 'b-')
    plt.title('En İyi Tur')

    # Mesafelerin değişimini gösterme
    plt.subplot(1, 2, 2)
    plt.plot(mesafeler)
    plt.title('Tur Mesafesinin Değişimi')
    plt.xlabel('Iterasyon')
    plt.ylabel('Mesafe')

    # Log bilgilerini kaydetme
    logger.info(f"Bu tur için en iyi mesafe: {en_iyi_mesafe}")

    # Grafiği kaydetme
    plt.tight_layout()
    plt.savefig(f'sonuclar_{simulasyon_zamani}.png')  # Tarih ve saat ile dosya adını oluştur
    plt.show()

    # İşlem tamamlandığında kullanıcıya bilgi verme
    print_green(f"Simülasyon tamamlandı. Sonuçlar 'sonuclar_{simulasyon_zamani}.png' dosyasına kaydedildi.")
    logger.info(f"Simülasyon tamamlandı. Sonuçlar 'sonuclar_{simulasyon_zamani}.png' dosyasına kaydedildi.")

except Exception as e:
    logger.error("Bir hata oluştu: " + str(e))
    print_green("Bir hata oluştu. Detaylar için log dosyasını kontrol edin.")
