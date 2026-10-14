# EEM4011 Aşama 2: EKG'de R tepesi bulma

Öğrenci: Yıldıray Yılmaz  
Durum: 48 kayıtta çalıştırıldı; sonuçlar 14 Ekim 2026'da kontrol edildi.

## Problem

EKG kaydında kalp atımlarının konumlarını otomatik bulmak, nabız ve ritim incelemesinin ilk adımıdır. Bu aşamadaki soru: **Ham genlik eşiğine göre, bant geçiren filtre ve enerji zarfı R tepelerini daha doğru buluyor mu?** Bu çalışma makine öğrenmesi içermez. Aritmi sınıflandırması vize sonrası genişletme olarak ayrı tutulur.

## Veri

[PhysioNet MIT-BIH Arrhythmia Database v1.0.0](https://physionet.org/content/mitdb/1.0.0/) kullanıldı. Veri 48 yaklaşık yarım saatlik, 360 Hz, iki kanallı EKG kaydından ve uzman anotasyonlarından oluşur. Kayıtlar 47 kişiye aittir. Mümkün olduğunda MLII, sonra II, son seçenek olarak ilk kanal kullanıldı. Referans olarak AAMI atım simgelerine karşılık gelen 109.494 anotasyon alındı. Bu sayı, kNN aşamasındaki pencere koşulunu geçen 109.468 atımdan farklıdır.

## Yöntem

1. **İlk yöntem:** Sinyalin medyanını çıkarıp mutlak genliğinde sabit oranlı eşik ve 250 ms asgari tepe aralığıyla tepe bulma.
2. **İyileştirme:** 5–15 Hz Butterworth bant geçiren filtre; türev karesi; 120 ms hareketli ortalamalı enerji zarfı; aynı asgari tepe aralığı. Zarf tepesinin çevresindeki 100 ms içinde filtreli sinyalin en büyük mutlak genliğine konum düzeltmesi.
3. **Karşılaştırma:** Algoritma referans anotasyonları görmeden çalışır. Bulunan tepe ile uzman anotasyonu en fazla 150 ms uzaklıktaysa, bire bir eşleştirilir. Tüm kayıtların TP, FP ve FN sayıları birleştirilerek precision, recall ve F1 hesaplanır.

Parametreler tüm kayıtlarda aynıdır; kayıt başına referansa bakılarak ayarlanmaz. Kod: [`10_phase2_rpeaks.py`](10_phase2_rpeaks.py).

## Doğrulanmış sonuç

| Yöntem | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Ham eşik | 109.162 | 44.197 | 332 | 0,7118 | 0,9970 | 0,8306 |
| Filtre + enerji zarfı | 105.413 | 116 | 4.081 | 0,9989 | 0,9627 | 0,9805 |

İyileştirilmiş yöntem yanlış pozitifleri ciddi biçimde azaltırken bazı gerçek atımları kaçırdı. Kayıt 100'ün ilk 10 saniyesini gösteren [`rpeak_kayit100.png`](https://github.com/eminylmz7140/eem4011-ekg-aritmi/blob/main/rpeak_kayit100.png) şekli açılıp kontrol edildi. Sayılar [`phase2_results.json`](https://github.com/eminylmz7140/eem4011-ekg-aritmi/blob/main/phase2_results.json) dosyasından ve tam veri çalıştırmasından doğrulandı.

## Sınırlar

Bu, MIT-BIH üzerinde sabit parametrelerle yapılan ders deneyidir; başka bir veri kümesinde dış doğrulama yoktur. F1, atımlar birleştirilerek hesaplandığından tek tek kayıtların performansını özetlemez; 104, 116, 203 ve 208 gibi bazı kayıtlarda iyileştirilmiş yöntemin F1 değeri düşmüştür. Hazır uzman anotasyonları yalnız değerlendirmede kullanıldı. Tespit edilen tepeler klinik tanı için kullanılmamalıdır.

## Çalıştırma

```bash
python -m pip install -r requirements.txt
python 02_download_data.py
python 10_phase2_rpeaks.py
```

İndirilen veri dosyaları GitHub'a veya ders formuna yüklenmez. Sonuçlar varsayılan olarak `artifacts/phase2/results.json` ve `artifacts/phase2/rpeak_kayit100.png` dosyalarına kaydedilir.

## Vize sonrası plan

R-tepe tespitinden sonra atım pencereleri ve RR aralıkları çıkarılıp kNN ile aritmi sınıflandırması çalışılabilir. Hazır olan kNN deneyinin sonuçları ayrı belgede saklanır; Aşama 2'nin sayıları olarak sunulmaz.
