# EEM4011 — EKG’de ventriküler atım tespiti

**Aşama 2 ana projesi:** MIT-BIH kayıtlarında, önceki hastalarda seçilmiş eğitimsiz bir şablon benzerliği eşiği yeni hastalardaki V ve E atımlarını ne ölçüde bulabiliyor? Bu çalışma bir ders deneyi ve başlangıç ölçümüdür; klinik tanı aracı değildir.

## Veri

[MIT-BIH Arrhythmia Database v1.0.0](https://physionet.org/content/mitdb/1.0.0/) kullanıldı. Kaynak arşivde 48 kayıt bulunur; bu deneyde yalnız MLII kanalı bulunan 43 kayıt işlendi. Pacemaker kayıtları 102, 104, 107 ve 217 dışarıda bırakıldı. 202, aynı kişiye ait 201 kaydıyla hasta ayrımını bozacağı için kullanılmadı. DS1’de 22 kayıt eşik seçimi için, DS2’de 21 kayıt bir kezlik test için kullanıldı. Ham veri GitHub’a yüklenmedi.

Bu analizde atım konumları PhysioNet .atr uzman anotasyonlarından alınır. Dolayısıyla sonuç otomatik R-tepesi bulma başarısını ölçmez. Her kayıt için şablon, o kaydın anotasyonlu atım pencerelerinden etiketsiz biçimde oluşturulur; test kaydı için bu, etiketsiz kayıt içi uyarlama anlamına gelir ve bağımsız, hiç görülmemiş sinyal üzerinde doğrulama değildir.

## Yöntem

Her anotasyonlu R konumunun 36 örnek öncesi ve 54 örnek sonrası alınarak 90 örneklik pencere oluşturuldu (360 Hz; yaklaşık −100 ile +150 ms). Kaydın sınırını aşan pencereler çıkarıldı. Her kaydın şablonu, geçerli pencerelerin her örnekteki medyanıdır. Her pencere ile aynı kaydın şablonu arasındaki Pearson korelasyonu hesaplandı.

RR aralıkları tüm anotasyon konumlarından hesaplandı; ilk ve son atım değerlendirmeye alınmadı. Ancak bu Aşama 2 baseline kararında RR oranı veya ek T2 filtresi kullanılmadı. Karar kuralı yalnızca kor < T biçimindedir. Formdaki özel yönlendirme de eşik T’nin DS1’de seçilip DS2’de bir kez uygulanmasını istiyor.

T, 0,30–0,95 aralığında 0,05 adımlarla DS1’in birleştirilmiş V-F1 değerini en yüksek yapan eşik olarak seçildi. DS2’de T yeniden ayarlanmadı. Pozitif sınıf V ve E sembolleridir.

## Sonuçlar

| Bölüm | Kayıt sayısı | Uygun atım | V/E atımı |
|---|---:|---:|---:|
| DS1 | 22 | 50.555 | 3.788 |
| DS2 | 21 | 47.140 | 3.200 |

DS1’de N/S korelasyon medyanı 0,9929, V/E medyanı 0,6611 oldu. Seçilen eşik **T = 0,90**.

| DS2 baseline ölçütü | Sonuç |
|---|---:|
| TP | 3.027 |
| FP | 2.398 |
| FN | 173 |
| Duyarlılık (Se) | 0,946 |
| Kesinlik (PPV) | 0,558 |
| **V-F1** | **0,702** |

Yanlış pozitif sayısı yüksek; PPV 0,558 olduğu için bu baseline yanlış alarmı azaltacak bir sonraki adım için başlangıç noktasıdır. Bu raporda iyileştirme sonucu iddia edilmez.

## Şekil ve doğrulama

[Şekil 1](https://github.com/eminylmz7140/eem4011-ekg-aritmi/blob/main/sekil1_sablon_119.png), kayıt 119’un ilk 10 saniyesini, N/V atım pencerelerini ve kayıt şablonunu gösterir. Görselde N pencereleri şablona daha çok benzerken V pencerelerinin çoğu farklı görünür. Kod tam veri üzerinde iki kez çalıştırıldı; sonuç JSON dosyalarının SHA-256 özetleri aynı çıktı. DS1’de beklenen N/S ile V/E korelasyon sırası sağlandı. Colab’da ayrıca baştan sona çalıştırma henüz doğrulanmadı.

Kod: [11_phase2_v_baseline.py](https://github.com/eminylmz7140/eem4011-ekg-aritmi/blob/main/11_phase2_v_baseline.py). [Sonuç JSON dosyası](https://github.com/eminylmz7140/eem4011-ekg-aritmi/blob/main/phase2_v_results.json). Çalıştırma yönergesi: [README](https://github.com/eminylmz7140/eem4011-ekg-aritmi#readme) ve [Colab defteri](https://colab.research.google.com/github/eminylmz7140/eem4011-ekg-aritmi/blob/main/EEM4011_Asama2_V_Colab.ipynb).

## Sınırlamalar ve sonraki aşama

Bu bir baseline’dır; tek test bölmesi ve kayıt içi etiketsiz şablon kullanımı nedeniyle bağımsız dış doğrulama değildir. 201/202 aynı kişiye ait olduğu için birlikte kullanılmadı; bu bilinen hasta tekrarını önler. PPV’nin düşük olması yanlış alarmların önemli olduğunu gösterir. Ek RR oran filtresi ve makine öğrenmesi bu sonuçlara dahil değildir. Hocanın özel notuna göre makine öğrenmesi Aşama 3’te aynı test hastalarında baseline ile karşılaştırılacaktır; SVM ve 1B-CNN bu ana planın parçası değildir.

48 kayıtlı R-tepesi tespit deneyi ayrı bir sinyal işleme alıştırmasıdır; onun F1 değerleri bu V-F1 sonucuyla karıştırılmamalıdır. kNN sınıflandırma deneyi de vize sonrası ayrı genişletmedir.

## Form için gerçek değerler

- Proje: Hasta bazlı V atımı tespiti.
- Veri: MIT-BIH; bu deneyde 43 kayıt.
- Ana metrik ve baseline: DS2 V-F1 = **0,702**.
- Seçilen T: **0,90**.
- İyileştirme sonrası değer: bu rapor hazırlanırken yok; sayı uydurulmamalı.
- GitHub: https://github.com/eminylmz7140/eem4011-ekg-aritmi
- Formun “kendi cümlelerinle” alanı öğrenci tarafından yazılmalı. Sohbet paylaşım bağlantısı yalnız uygulamanın Paylaş düğmesinden alınmalı.
