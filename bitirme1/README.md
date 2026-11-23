# EEM4011 + Bitirme 1 — Gerçek Zamanlı 10 Saniyelik EKG Akış (Streaming) Sürümü

**Öğrenci:** Yıldıray Yılmaz (213204045)  
**Danışman:** Arş. Gör. Dr. Meral Kılıçarslan Ouach  
**Geliştirme Seçeneği:** Akışta çalışma — kaydı 10 saniyelik parçalarla işleyen sürüm; atım başına gecikme (ms) ve çevrimdışı modelle aynı V-F1 skoru.

## Tek Cümlelik Geliştirme Özeti
MIT-BIH EKG kayıtlarını 10 saniyelik bloklar (3600 örnek, 360 Hz) halinde akış simülasyonunda işleyerek atım başına düşük gecikmeyle (**1,725 ms/atım**) ve çevrimdışı modelle birebir aynı doğrulukla (**0,870 DS2 V-F1**) ventriküler ektopik atım (VEB) tespiti yapmak.

## Doğrulanmış Akış (Streaming) Sonuçları (DS2 — 21 Kayıt, 47.140 Atım)

| Ölçüt | Çevrimdışı (Batch) | 10-sn Akış (Streaming) |
| :--- | :---: | :---: |
| **Test Kayıt / Atım Sayısı** | 21 kayıt / 47.140 atım | 21 kayıt / 47.140 atım (3.801 blok) |
| **Pozitif V/E Atım Sayısı** | 3.200 | 3.200 |
| **Sınıflandırıcı** | Random Forest (300 ağaç) | Random Forest (300 ağaç) |
| **DS2 V-F1 Skoru** | **0,870** | **0,870** |
| **Duyarlılık (Se) / Kesinlik (PPV)** | 0,934 / 0,814 | 0,934 / 0,814 |
| **TP / FP / FN** | 2.988 / 682 / 212 | 2.988 / 682 / 212 |
| **Atım Başına Uçtan Uca Gecikme** | — | **1,725 ms/atım** |
| **10-sn Blok Başına İşleme Süresi** | — | **21,387 ms/blok** |
| **Kayıt 200 Öznitelik Çıkarma Süresi** | — | **0,047 ms/atım** |

## Klasör İçeriği
- `14_bitirme_streaming.py`: MIT-BIH DS2 kayıtlarını 10 saniyelik pencerelerle akan veri (streaming) düzeninde işleyen, her bloktaki atımlar için 18 morfolojik örnek + 2 komşu RR aralığı çıkaran ve eğitilmiş 300 ağaçlı Random Forest ile atım başına gecikmeyi (ms) ve V-F1 skorunu ölçen Python betiği.
