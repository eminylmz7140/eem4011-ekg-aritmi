# Tam Veri Kümesi — İlk Baseline Sonuçları

## Veri ve çalıştırma

- Kaynak: MIT-BIH Arrhythmia Database, PhysioNet.
- Arşiv doğrulandı; 48 kaydın tamamı ve her kayıt için `.hea`, `.dat`, `.atr` dosyaları açıldı.
- Özellik tablosuna alınan geçerli atım: **109.468**.
- Eğitim: **85.782 atım**. Test: **23.686 atım**.
- Testte 11 kayıt kimliği ve **10 hasta grubu** vardı. 201 ve 202 aynı kişiden geldiğinden tek grupta tutuldu.
- Kanal seçimi MLII, yoksa II, yoksa ilk kanal biçimindedir. 102 ve 104 kayıtlarında seçilen kanal V5 olduğundan kayıtlar arasında lead tamamen aynı değildir.
- Model: tek EKG kanalı, altı basit istatistiksel özellik, StandardScaler ve uzaklık ağırlıklı kNN (`k=5`).
- Tek kayıt gruplu holdout bölmesi (`random_state=42`); bu, tekrarlı çapraz doğrulama değildir.

## Sonuçlar

| Ölçüt | Değer |
|---|---:|
| Accuracy | 0,764 |
| Macro-F1 | 0,304 |
| Weighted-F1 | 0,770 |

| Sınıf | Test desteği | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| N | 20.073 | 0,880 | 0,848 | 0,864 |
| S | 519 | 0,021 | 0,033 | 0,026 |
| V | 1.011 | 0,272 | 0,652 | 0,384 |
| F | 16 | 0,000 | 0,000 | 0,000 |
| Q | 2.067 | 0,364 | 0,188 | 0,248 |

Karmaşıklık matrisi satırları gerçek sınıfı, sütunları tahmin sınıfını gösterir; sıra **N, S, V, F, Q**:

```text
[[17024, 750, 1639, 43, 617],
 [  367,  17,  109,  0,  26],
 [  318,   0,  659,  1,  33],
 [   14,   0,    1,  0,   1],
 [ 1632,  35,   11,  1, 388]]
```

## Yorum

Accuracy, baskın N sınıfı nedeniyle tek başına yanıltıcıdır. Macro-F1 0,304 ve S/F sınıflarındaki düşük sonuçlar, bu basit kNN baseline'ının nadir sınıfları iyi ayıramadığını gösterir. F test desteği yalnızca 16 atımdır. Bu sayılar nihai ya da klinik performans iddiası değildir; sonraki iyileştirme sınıf dengesizliği, özellikler ve tekrarlı hasta-gruplu değerlendirmeyi ele almalıdır.

Proje tüm MIT-BIH kayıtlarını kullanır ve pacing içeren kayıtları özel olarak dışlamaz; bu nedenle sonuçlar resmi/katı AAMI EC57 benchmark sonucu olarak sunulmamalıdır.
