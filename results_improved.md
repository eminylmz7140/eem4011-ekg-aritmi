# EEM4011 — Geliştirilmiş kNN karşılaştırması

Aynı 48 kayıt, 109468 atım ve aynı hasta bazlı test bölümü kullanıldı.
Model, yalnızca eğitim hastaları içindeki iki doğrulama bölmesinin ortalama macro-F1 değerine göre seçildi.

Seçilen model: shape_rr_knn7_cap5000; 36 özellik; eğitimde kullanılan atım: 18048.

| Ölçüt | Önce | Sonra |
|---|---:|---:|
| Accuracy | 0.7637 | 0.7450 |
| Macro-F1 | 0.3043 | 0.4261 |

| Sınıf | Önce F1 | Sonra F1 | Test desteği |
|---|---:|---:|---:|
| N | 0.8635 | 0.8424 | 20073 |
| S | 0.0257 | 0.1114 | 519 |
| V | 0.3843 | 0.3808 | 1011 |
| F | 0.0000 | 0.0000 | 16 |
| Q | 0.2478 | 0.7957 | 2067 |

Adaylarda dalga şekli ve RR özellikleri değerlendirildi.
Seçilen modelin sınıf başına örnek sınırı: 5000.
Karşılaştırma amacıyla hep eğitimdeki çoğunluk sınıfını (N) tahmin eden model: accuracy=0.8475, macro-F1=0.1835.
Macro-F1 ve accuracy değişimleri ayrı yorumlanmalıdır; sınıf bazlı sonuçlar yukarıdadır.

Sınırlar: Önceden raporlanmış test grubu tekrar kullanıldı; sonuç dış doğrulama değildir. R tepe konumları referans anotasyonlardan alınır. Sonraki RR bilgisi kullanıldığından yöntem çevrimdışıdır. Pacing kayıtları ve farklı lead'ler dahil; katı EC57 karşılaştırması değildir. F sınıfının testte 16 örneği vardır.
