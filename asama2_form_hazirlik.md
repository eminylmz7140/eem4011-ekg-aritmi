# EEM4011 Aşama 2 formu için doğrulanmış bilgiler

Bu sayfa, sohbette görülen form alanlarına karşılık gelir. Formun şıkları veya sırası değişirse ekrandaki gerçek ifadeyi esas alın. Gönderim yapılmadı.

| Görülen alan | Girilecek gerçek bilgi |
|---|---|
| Seçilen proje | “Kendi konumu seçtim (Aşama 1 formunda yazdım)” **yalnız Aşama 1'de gerçekten bu konu yazıldıysa**. Aksi hâlde formun menü/konu tutarsızlığı çözülmeden gönderme. |
| Veri setini indirip koda yükledin mi? | Evet. MIT-BIH verisinin 48 kaydı bu bilgisayarda indirildi ve işlendi. |
| Kaç kayıt / görüntü / kişi kullandın? | Form hangi birimi istiyorsa: **48 kayıt**, **47 kişi**, **109468 geçerli atım**. Tek kutu yalnız sayı istiyorsa projede saydığın birimi hocanın alan tarifine göre seç. |
| Ana metrik | **Macro-F1**. Sınıflar dengesiz olduğu için ana ölçüt olarak kullanıldı. |
| Baseline değeri | **0,3043**. Altı özellikli kNN'nin Macro-F1 sonucu. |
| İlk iyileştirmeden sonraki değer | **0,4261**. Dalga şekli ve RR özellikli kNN'nin aynı test bölümündeki Macro-F1 sonucu. |
| Genel doğruluk sorulursa | Önce **%76,37**, sonra **%74,50**. İyileşme iddiasını genel doğruluk için kullanma. |
| Şekil | `ekg_kayit100.png` gerçek EKG'nin ilk 8 saniyesini ve hazır anotasyonları gösterir. `sinif_f1_karsilastirma.png` aynı testteki beş sınıfın önce/sonra F1 değerlerini gösterir. |
| GitHub bağlantısı | **Henüz yok**. GitHub oturumu açılmadan URL uydurma. |
| Sohbet paylaşım bağlantısı | **Henüz doğrulanmadı**. Uygulamanın Paylaş düğmesinden gerçek bağlantıyı al. |
| “Kendi cümlelerinle 3 cümle” | Öğrencinin kendi sözleriyle doldurulmalı. İpuçları: kodun okuduğu veri; baseline sayısının kaynağı; seçtiğin şeklin gösterdiği şey. |

## Aşama 1'deki gap sorusu

20. soru hâlâ bu formda görünüyorsa, genel “henüz hiç çalışılmamış” iddiası doğrulanmadığı için **“Kısmen: bir kısmı çalışılmış”** daha savunulabilir. [Qin ve ark.](https://doi.org/10.1038/s41598-017-06596-z) kayıt bazlı, [Zhang ve ark.](https://doi.org/10.1155/2021/9946596) hastalar arası değerlendirme yaptı. Mevcut deney derin öğrenme karşılaştırması değildir.

## AI kullanımı ve doğrulama

Kullanılan araçları ve gerçekten yaptığın kontrolleri `proje.md` dosyasındaki AI günlüğüne göre yaz. Formda kendi değerlendirmene ait bir puan veya serbest yanıt isteniyorsa bunu sen doldur. Yanıtları göndermeden önce kodun gerçek çıktılarını ve şekilleri bir kez açıp incele.
