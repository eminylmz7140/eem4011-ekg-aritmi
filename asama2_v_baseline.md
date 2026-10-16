# EEM4011 ana proje — Aşama 2 V atımı başlangıç deneyi

Güncelleme: 16 Ekim 2026. Hocanın kişisel formundaki güncel kapsam esas alındı. **Form henüz gönderilmedi.**

## Soru ve veri

MIT-BIH Arrhythmia Database v1.0.0'da, önceki hastalarda seçilmiş sabit bir morfoloji eşiği yeni hastalardaki ventriküler atımları (V ve E) ne kadar iyi bulur? PhysioNet kaynağı: <https://physionet.org/content/mitdb/1.0.0/>. Kaynak veri GitHub'a konmaz.

DS1 (22 kayıt): 101, 106, 108, 109, 112, 114, 115, 116, 118, 119, 122, 124, 201, 203, 205, 207, 208, 209, 215, 220, 223, 230.

DS2 (21 kayıt): 100, 103, 105, 111, 113, 117, 121, 123, 200, 210, 212, 213, 214, 219, 221, 222, 228, 231, 232, 233, 234.

102, 104, 107 ve 217 pacemaker kayıtları dışarıda bırakıldı. 202, DS1'deki 201 ile aynı kişiden olduğu için DS2'den çıkarıldı. Bu seçim 43 kayıt bırakır. Yalnız MLII kanalı kullanıldı; `.atr` anotasyonlarının R konumları ve sembolleri okundu. Bu çalışma otomatik R tepesi tespitini değerlendirmez.

## Yöntem

Her anotasyonlu atım için R işaretinin 36 örnek öncesinden 54 örnek sonrasına kadar 90 örneklik pencere alındı (360 Hz). Kayıt başı/sonunda tam sığmayan pencereler dışlandı. Her kayıttaki geçerli pencerelerin örnek bazında medyanı şablon oldu. Her pencere ile kendi kaydının şablonu arasındaki Pearson korelasyonu `kor` hesaplandı. RR önceki ve sonraki aralıkları, uygun atımlar seçilmeden önce tüm atım dizisinden çıkarıldı; ilk/son atım değerlendirilmedi. Etiketler: N, L, R, e, j, A, a, J, S, V, E; pozitif V/E.

`T` eşiği 0,30–0,95 aralığında 0,05 adımlarla **yalnız DS1 toplam V-F1** en yüksek olacak şekilde seçildi. Eşitlikte daha küçük T kullanıldı. Sabit T, **DS2'de bir kez** uygulandı: `kor < T` ise V tahmini. DS2 üzerinde eşik yeniden seçilmedi.

## Gerçek sonuçlar

| Bölüm | Uygun atım | V/E atımı |
|---|---:|---:|
| DS1 | 50.555 | 3.788 |
| DS2 | 47.140 | 3.200 |

DS1'de N/S korelasyon medyanı **0,9929**, V/E medyanı **0,6611**; beklenen sıra sağlandı. DS1'de seçilen **T = 0,90**.

| DS2 başlangıç metriği | Değer |
|---|---:|
| TP | 3.027 |
| FP | 2.398 |
| FN | 173 |
| Duyarlılık (Se) | 0,946 |
| Kesinlik (PPV) | 0,558 |
| **V-F1** | **0,702** |

Şekil 1 `sekil1_sablon_119.png`: üstte kayıt 119'un ilk 10 saniyesi, altta medyan şablon ile 20 N ve 20 V atım penceresi. Şablon N pencereleriyle örtüşüyor; V pencerelerinin çoğu belirgin farklı. Grafik görsel olarak kontrol edildi. Kod tam veride iki kez çalıştırıldı ve `results.json` dosyalarının SHA-256 özeti aynı çıktı. Sayılar doğrulanmış yerel çıktıdır; Colab'da ayrı baştan sona koşu henüz yapılmadı.

## Formda kullanılacak bilgiler

Ana proje seçimi: **Ana projem**. Veri indirildi: **Evet, tamamını** (yerel bilgisayarda 48 kayıt indirilmiş, bunların 43'ü bu deneyde kullanılmıştır). Kullanılan kayıt sayısı: **43**. Ana metrik: **V-F1 (DS2, hasta bazlı, V+E)**. Baseline değeri: **0,702**. İlk iyileştirme henüz yapılmadı; alanı boş bırak. GitHub bağlantısı: <https://github.com/eminylmz7140/eem4011-ekg-aritmi>. Sohbet bağlantısı yalnız uygulamadaki **Paylaş** düğmesinden alınan gerçek link olmalı. Formun “kendi cümlelerinle 3 cümle” kısmını öğrenci kendisi yazmalıdır.

Kayıtların tümü aynı kişiden bağımsız değildir; bilinen tekrar 201/202 özel olarak ayrıldı. PPV'nin 0,558 olması, yanlış alarmın hâlâ önemli bir sorun olduğunu gösterir. T1/T2 ve ek RR kuralı henüz uygulanmadı; bu nedenle iyileşme iddiası yoktur. Eğitim amaçlı analizdir, klinik tanı aracı değildir.
