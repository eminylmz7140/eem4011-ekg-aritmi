# EEM4011 — Q1 Makale İddia Tablosu (Hafta 1)

**Öğrenci:** Yıldıray Yılmaz (213204045)  
**Hedef Dergi:** Biomedical Signal Processing and Control (Elsevier, Q1)  
**Yedek Dergi:** Computers in Biology and Medicine (Elsevier, Q1)  

## Tek Cümlelik Katkı (Single-Sentence Contribution)

> We show that, under a patient-independent DS1/DS2 split and a 5-fold cross-validation protocol on 43 MLII recordings from the open MIT-BIH Arrhythmia Database, a 20-feature Random Forest classifier increases ventricular ectopic beat F1 score from 0.702 to 0.870 over an untrained Pearson template-correlation baseline by reducing false positives from 2,398 to 682.

## İddia Tablosu (Claims Table)

| İddia | Kanıt (Kendi Çıktımızdan Sayı veya Şekil) | Şekil / Tablo | Durum |
| :--- | :--- | :--- | :---: |
| **C1.** Hasta-bağımsız sabit DS2 test kümesinde (21 kayıt, 47.140 atım) 20 öznitelikli Random Forest sınıflandırıcısı, eğitimsiz şablon-korelasyon baseline yöntemine göre V-F1 skorunu artırır ve yanlış alarmları düşürür. | DS2 test çıktısı: Baseline V-F1 = 0,702 (TP=3.027, FP=2.398, FN=173, Se=0,946, PPV=0,558); kNN V-F1 = 0,525 (FP=4.972); Random Forest V-F1 = 0,870 (TP=2.988, FP=682, FN=212, Se=0,934, PPV=0,814). | Tablo 2, Şekil 2, Şekil 3 | **var** |
| **C2.** Değerlendirme tekil DS1/DS2 ayrımı dışında 43 hasta kaydının tamamı üzerinde hasta-bağımsız katlı bölmeyle tekrarlandığında katlar arası morfolojik değişimin etkisi ölçülür. | 5 katlı hasta-bağımsız çapraz doğrulama çıktısı (n=5 kat, 43 hasta): Baseline V-F1 = 0,73 ± 0,16; Random Forest V-F1 = 0,66 ± 0,28 (Hafta 3'te 10 kata genişletilecek). | Tablo 3 | **var** |
| **C3.** Aynı hasta-bağımsız bölme düzeninde, literatürde yayımlanmış ve kodu açık bir referans yöntem yeniden koşularak önerilen modelle aynı katlarda karşılaştırılır. | Yayımlanmış açık kodlu yöntemin aynı DS1/DS2 ve hasta katlarındaki V-F1, Se ve PPV değerleri ile eşleştirilmiş farkın %95 bootstrap güven aralığı. | Tablo 3, Şekil 2 | **yapılacak** |
| **C4.** RR zamanlama özniteliklerinin (önceki ve sonraki RR) eklenmesi, yalnız 18 noktalı QRS morfolojisi kullanımına kıyasla DS2 V-F1 başarımını artırır (duyarlılık / ablasyon deneyi). | Yalnız 18 morfolojik örnek vs. 18 morfoloji + yalnız önceki RR vs. 18 morfoloji + 2 RR öznitelik kümelerinin aynı DS2 kayıtlarındaki V-F1 karşılaştırması. | Tablo 4 | **yapılacak** |
