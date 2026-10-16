# EEM4011 Aşama 2 formu: güncel ana proje

**16 Ekim 2026 düzeltmesi:** Hocanın güncellenmiş kişisel formu ana projeyi "hasta bazlı V atımı tespiti" olarak tanımlıyor. Bu dosyanın aşağıdaki eski R-tepesi sayıları artık **ana projenin sonuç alanlarına uygun değildir**. Güncel, doğrulanmış 43 kayıtlı V atımı başlangıç deneyi için [asama2_v_baseline.md](asama2_v_baseline.md) dosyasını kullanın. Ana metrik DS2 V-F1 = **0,702**; 48 kayıtlı R-tepesi F1 = 0,9805 bu metrik değildir.

Bu not yalnız gerçekten çalıştırılan **makine öğrenmesiz R-tepe tespiti** deneyini kapsar. Form gönderilmedi. Formda görünen şıkları ve alanların birimlerini esas al.

| Form alanı | Doğrulanmış yanıt |
|---|---|
| Seçilen proje | “Kendi konumu seçtim (Aşama 1 formunda yazdım)” **yalnız Aşama 1'de gerçekten bu konu yazıldıysa**. Önceki formda farklı konu varsa uyumunu hocaya göre düzelt. |
| Veri setini indirip koda yükledin mi? | Evet. MIT-BIH veri kümesinin 48 kaydı bu bilgisayarda indirildi ve işlendi. |
| Kaç kayıt / görüntü / kişi kullandın? | **48 kayıt**; veri kümesinde **47 kişi** ve değerlendirmede **109494 referans atım** vardır. Formun istediği birime göre sayı gir. |
| Ana metrik | **F1 skoru** (R tepesi tespitinde, 150 ms eşleştirme toleransı). |
| Baseline değeri | **0,8306** (ham eşik, tüm atımların birleştirilmiş F1'i). |
| İlk iyileştirmeden sonraki değer | **0,9805** (5–15 Hz filtre + enerji zarfı; tüm atımların birleştirilmiş F1'i). |
| Şekil | `rpeak_kayit100.png`: kayıt 100'ün ilk 10 saniyesinde EKG, referans, ham ve filtreli tepe konumları. |
| GitHub bağlantısı | https://github.com/eminylmz7140/eem4011-ekg-aritmi |
| Sohbet paylaşım bağlantısı | Henüz doğrulanmadı; uygulamanın **Paylaş** düğmesinden gerçek bağlantıyı al. |
| “Kendi cümlelerinle 3 cümle” | Öğrencinin kendi sözleriyle yazılmalı. Veri, ilk sayı ve şeklin ne gösterdiği anlatılmalı. |

**Aşama 2'de kNN'nin 0,3043 → 0,4261 Macro-F1 sonuçlarını kullanma.** Makine öğrenmesi vize sonrası çalışma olarak ayrıldı. R-tepe sonuçlarının ayrıntıları [`asama2_ekg_sinyal_isleme.md`](asama2_ekg_sinyal_isleme.md) belgesinde.

## Aşama 1'deki araştırma açığı sorusu

Genel “henüz hiç çalışılmamış” iddiası doğrulanmadığı için 20. soruda **“Kısmen: bir kısmı çalışılmış”** savunulabilir. Bu çalışmanın iddiası yeni yöntem keşfi değil, iki klasik sinyal işleme yaklaşımını aynı veride karşılaştırmaktır.

## AI beyanı ve kişisel alanlar

Kullanılan aracı, sorulan istekleri ve gerçekten yapılan kontrolleri dürüstçe belirt. “Kendi cümlelerinle 3 cümle”, serbest değerlendirme, sohbet linki ve form gönderimi öğrenci tarafından tamamlanmalıdır. Sonuçlar [`phase2_results.json`](https://github.com/eminylmz7140/eem4011-ekg-aritmi/blob/main/phase2_results.json) dosyasındaki sayılardan kontrol edilmelidir.
