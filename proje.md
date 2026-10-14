# EEM4011 bireysel proje: EKG atımlarının hasta bazlı kNN sınıflandırması

Öğrenci: Yıldıray Yılmaz  
Durum: 48 kayıtla çalışan ders projesi; bağımsız dış doğrulama yapılmadı.  
Son güncelleme: 14 Ekim 2026.

## Olay ve problem

EKG atımlarının otomatik sınıflandırılması, uzun kayıtların incelenmesini destekleyebilir. Bu projede belirli bir haber olayı veya olay tarihi belgelenmedi; Aşama 1 formu böyle bir olay istiyorsa gerçek ve kaynaklı bir örnek ayrıca seçilmelidir. Burada ölçülen soru şudur: **Aynı hasta bazlı eğitim/test ayrımında, basit istatistiklere eklenen dalga şekli ve RR özellikleri kNN sınıflandırmasının sınıflar arası dengesini nasıl değiştirir?**

## Literatür

| Kaynak | Yöntem ve veri | Makalede bildirilen sonuç | Bizim deneyimizle ilişkisi |
|---|---|---|---|
| [1] Qin ve ark., 2017 | Dalgacık özellikleri + PCA + SVM; MIT-BIH, atım bazlı ve kayıt bazlı 10 katlı değerlendirme | Kayıt bazlı ortalama duyarlılık %44,40; özgüllük %88,88; doğruluk %81,47 | Ayrım biçiminin sonucu ciddi biçimde değiştirebildiğini gösterir. Altı sınıf ve farklı bölmeler kullandığı için doğrudan sayısal rakip değildir. |
| [2] Zhang ve ark., 2021 | Adversarial CNN ve RR özellikleri; MIT-BIH, hastalar arası değerlendirme | S sınıfı duyarlılığı %78,8 ve kesinliği %90,8; V duyarlılığı %92,5 ve kesinliği %94,3 | Hasta bazlı deney ve RR özelliklerinin daha önce kullanıldığını doğrular. Derin öğrenme ve farklı test bölmesi nedeniyle bizim sonuçlarla doğrudan sıralanmaz. |
| [3] Melek, 2026 | Özellik seçimi ile kNN ve SVM; MIT-BIH | kNN için ilk 15 seçilmiş özellikte doğrulama doğruluğu %98,34; SVM için 15 özellikte %98,57 | Klasik kNN karşılaştırmasının yeni olmadığını gösterir. Yayındaki doğrulama protokolü bizim hasta bazlı testimizle eşdeğer kabul edilmez. |

Makale sonuçları, farklı sınıf eşlemeleri, hasta bölmeleri ve metrikler nedeniyle bizim doğruluk ve Macro-F1 değerlerimizle doğrudan karşılaştırılamaz. Bu tablonun sayıları ve bağlantıları yayıncı sayfalarından kontrol edildi. Science AI Journal'ın otomatik derlemesi kaynak bulmaya yaradı; yayınların yerini tutmaz.

## Research gap ve doğrulama

Science AI Journal'ın 15 makalelik tablosu ve Pro Report sayfası EKG sınıflandırması için çeşitli araştırma açıkları önerdi. İlk seçilen “derin öğrenme ve klasik ML aynı veri üzerinde karşılaştırılmamış” iddiasını bu uygulama test etmiyor; kod yalnızca kNN seçeneklerini karşılaştırıyor. “Hastalar arası değerlendirme hiç yapılmamış” iddiası da [1] ve [2] ile çelişiyor. Bu nedenle araştırma açığı **tümüyle doğrulandı** denemez; Aşama 1'deki 20. soru için mevcut kanıtlar **“Kısmen: bir kısmı çalışılmış”** yanıtını destekler. Bu, form doldurulurken öğrencinin kendi değerlendirmesiyle son kez kontrol edilmelidir.

Bu projenin ölçülebilir katkısı, aynı hasta bazlı test örneklerinde altı basit özellikli kNN ile 36 özellikli kNN'nin sonuçlarını ve kayıplarını yeniden üretilebilir biçimde göstermektir. Literatürde ilk yöntem olduğu iddia edilmez.

## Veri

Kaynak [4] PhysioNet MIT-BIH Arrhythmia Database v1.0.0: 48 yaklaşık yarım saatlik kayıt, 47 kişi, 360 Hz, iki kanal ve referans atım anotasyonları. 201 ve 202 aynı kişiye aittir ve aynı bölümde tutulur. `.hea`, `.dat`, `.atr` dosyaları doğrulanıp okunmuştur. Eşlenen 109.494 atımdan tam pencere içeren 109.468 atım kullanıldı. Eğitim havuzunda 85.782, testte 23.686 atım vardır. Testte 11 kayıt kimliği, 10 kişi grubu vardır.

Kanal mümkün olduğunda MLII, yoksa II veya ilk kanaldır. 102 ve 104 kayıtlarında V5 kullanıldı. Her atımda referans konumu çevresinden 180 örnek, yani 0,5 saniyelik pencere alınır. Etiketler N, S, V, F, Q biçiminde beş gruba eşlenir. Pacing kayıtları dahil olduğundan bu resmi EC57 değerlendirmesi değildir. Veri dosyaları GitHub'a veya forma yüklenmemelidir; açık kaynağın bağlantısı verilmelidir.

## Yöntem

İlk model, her pencereden ortalama, standart sapma, minimum, maksimum, tepe-tepe genlik ve RMS çıkarır. `StandardScaler` ardından uzaklık ağırlıklı kNN (`k=5`) uygulanır.

Geliştirilmiş adaylar aynı altı özelliğe 24 normalize dalga şekli noktası ve altı RR özelliği ekler. RR özellikleri önceki ve sonraki atım süreleri ile son en çok 10 aralığın yerel medyanına göre türetilen değerlerdir. Böylece toplam 36 özellik olur. Dört aday, yalnız eğitim hastaları içindeki iki ayrı hasta bazlı doğrulama bölmesinde ortalama Macro-F1 ile değerlendirilir. Seçilen aday `k=7`, uzaklık ağırlığı ve her sınıftan en çok 5.000 eğitim örneği kullanır; nihai eğitimde 18.048 örnek vardır. Ölçekleyici yalnız ilgili eğitim örneklerinde öğrenilir. Test grubu seçenek seçimine katılmaz.

Python akışı `run_pipeline.py --improve` ile sekiz aşamada çalışır. `08_verify_improvement.py` grupların ayrık olduğunu, eğitimdeki ölçeklemeyi, kaydedilen tahminleri ve yeniden hesaplanan metrikleri denetler. Tam veriyle son çalıştırmada bu denetimler geçti.

## Başarı ölçütü ve gerçek sonuçlar

Ana ölçüt Macro-F1'dir; N sınıfı baskın olduğu için genel doğruluk tek başına yeterli değildir. Aynı 23.686 test atımında:

| Model | Doğruluk | Macro-F1 |
|---|---:|---:|
| Sürekli N diyen kontrol | %84,75 | 0,1835 |
| Altı özellikli ilk kNN | %76,37 | 0,3043 |
| 36 özellikli seçilen kNN | %74,50 | 0,4261 |

| Sınıf | Test atımı | İlk F1 | Yeni F1 |
|---|---:|---:|---:|
| N | 20.073 | 0,8635 | 0,8424 |
| S | 519 | 0,0257 | 0,1114 |
| V | 1.011 | 0,3843 | 0,3808 |
| F | 16 | 0 | 0 |
| Q | 2.067 | 0,2478 | 0,7957 |

Macro-F1 0,1218 arttı, genel doğruluk 1,86 yüzde puan düştü. S sınıfının duyarlılığı %34,87, kesinliği yalnız %6,63'tür. F sınıfı tanınmadı. Q sınıfı pacing ve sınıflandırılamayan atımları da içeren bir gruptur; Q artışı tek bir aritmi için klinik başarı anlamına gelmez. Tüm ayrıntılar teslim ZIP'indeki `biomed_project/artifacts/comparison_improved.json` ve [GitHub'daki karşılaştırma dosyasında](https://github.com/eminylmz7140/eem4011-ekg-aritmi/blob/main/comparison_improved.json) bulunur.

## Şekiller

`09_make_figures.py` gerçek kayıttan ve kayıtlı sonuçlardan iki şekil üretir: `ekg_kayit100.png` ilk sekiz saniyelik MLII sinyalini ve referans anotasyonlarını gösterir; `sinif_f1_karsilastirma.png` aynı test bölümündeki beş sınıfın ilk ve yeni F1 değerlerini gösterir. EKG üzerindeki işaretler otomatik R-tepe bulma sonucu değildir. Grafikler proje için üretilmiştir; kaynak veri dosyaları sunumla veya GitHub ile paylaşılmaz.

## Sınırlar ve devam planı

Önceden raporlanan aynı test grubu karşılaştırmada yeniden kullanıldı; yeni ve bağımsız dış veri ile doğrulama yapılmadı. İki iç doğrulama bölmesi küçük azınlık sınıfları için belirsizliği ortadan kaldırmaz. R-tepe konumları hazır anotasyondan geldiği için otomatik tespit değerlendirilmedi. Sonraki RR özelliği gelecek atımın görülmesini gerektirir; yöntem çevrimdışıdır. Lead farkları ve pacing kayıtları sonucu etkileyebilir. F için 16 test atımı vardır. Klinik tanı iddiası kurulamaz.

Bir sonraki deneyde S ve F sınıflarındaki yanlış tahminler kişi bazında incelenmeli; yalnız geçmiş RR kullanan seçenek denenmeli; daha fazla hasta gruplu tekrar ve uygun bağımsız veriyle doğrulama yapılmalıdır. Bunlar mevcut sonuç değil, çalışma önerileridir. Dersin vize öncesi beklentisi sinyal işleme ise EKG görselleştirme ve basit ölçümler ön plana alınmalı; makine öğrenmesi sonucu dönem sonu geliştirmesi olarak sunulmalıdır.

## Haftalık plan ve teslim durumu

| Aşama | Gerçek durum | Kalan iş |
|---|---|---|
| Veri ve ilk kod | 48 kayıt indirildi; sekiz aşama çalıştı | Kaynak bağlantısını formda belirtmek |
| İlk sonuç ve şekil | Metrikler doğrulandı; iki grafik üretildi | Öğrencinin kendi sözleriyle üç cümlelik yorum yazması |
| Literatür ve gap | Üç yayıncı bağlantısı incelendi; genel gap iddiası daraltıldı | Hocaya sunulacak son proje sorusunu formdaki önceki cevaplarla eşlemek |
| Kod paylaşımı | [GitHub deposuna](https://github.com/eminylmz7140/eem4011-ekg-aritmi) kod, rapor, grafikler ve tam teslim ZIP'i yüklendi; 26 dosya listesi doğrulandı | ZIP içindeki klasör yapısını koruyarak indirme ve çalıştırma |
| Form | Bu belgeden kopyalanabilecek gerçek bilgiler hazır | Kişisel alanlar, sohbet paylaşım bağlantısı ve gönderim öğrencice tamamlanmalı |

Paylaşılan ders takvimi geçerliyse 14–18 Ekim arasında şekil ve ilk sonucu Aşama 2 formuna koyup kendi üç cümleni yaz; 19–25 Ekim arasında S/F hata örneklerini incele ve yöntem sınırlarını gözden geçir; 26 Ekim–1 Kasım arasında son sonuç, CV cümlesi ve başvuru paketini öğretmenin Aşama 3 yönergesine göre tamamla. Bu gelecek adımlar yapılmış deney gibi raporlanmamalıdır.

## CV cümlesi

“PhysioNet MIT-BIH veri kümesindeki 48 EKG kaydında, kişi bazlı ayrımla kNN sınıflandırmasını yeniden ürettim; dalga şekli ve RR özellikleriyle Macro-F1'i 0,3043'ten 0,4261'e çıkardım ve doğruluktaki düşüş ile azınlık sınıfı hatalarını raporladım.”

## Kaynakça

1. [Q. Qin, J. Li, L. Zhang, Y. Yue ve C. Liu, “Combining Low-dimensional Wavelet Features and Support Vector Machine for Arrhythmia Beat Classification,” *Scientific Reports*, 7, 6067, 2017](https://doi.org/10.1038/s41598-017-06596-z).
2. [J. Zhang ve ark., “Interpatient ECG Heartbeat Classification with an Adversarial Convolutional Neural Network,” *Journal of Healthcare Engineering*, 2021](https://doi.org/10.1155/2021/9946596).
3. [N. Melek, “Machine learning–enabled ECG arrhythmia classification: a systematic and educational study from signal processing to decision support,” *Scientific Reports*, 16, 26300, 2026](https://doi.org/10.1038/s41598-026-56828-4).
4. [G. Moody ve R. Mark, “MIT-BIH Arrhythmia Database,” PhysioNet, v1.0.0, 2005, DOI: 10.13026/C2F305](https://physionet.org/content/mitdb/1.0.0/).
5. [G. B. Moody ve R. G. Mark, “The impact of the MIT-BIH Arrhythmia Database,” *IEEE Engineering in Medicine and Biology Magazine*, 20(3), 45–50, 2001](https://doi.org/10.1109/51.932724).

## AI günlüğü ve beyan taslağı

- **Sordum:** EKG üzerinde veri seti bulunan, programlama ve modelleme dersine uygun bir proje geliştirme yardımı istedim.
- **Aldım:** Science AI Journal'ın gap önerileri, Python kodu, metrik raporu, literatür bağlantıları ve görseller için yardım aldım.
- **Doğruladım:** Codex, PhysioNet ve üç yayıncı bağlantısını açtı; kodun bölmelerini ve kaydedilen metriklerini kontrol etti. Öğrencinin kaynakları ve kendi bilgisayarındaki yeniden çalıştırmayı ayrıca gözden geçirmesi gerekir.
- **Değiştirdim:** İlk geniş gap iddiası, mevcut deneyin gerçekten ölçtüğü kNN özellik karşılaştırmasına daraltıldı; doğruluk düşüşü ve F sınıfı başarısızlığı açıkça yazıldı.

**Beyan taslağı:** “Fikir taraması için Science AI Journal'ı; kod, veri analizi ve belge taslağı için Codex'i kullandım. AI önerilerini PhysioNet veri sayfası, yayıncı kaynakları ve koddan yeniden hesaplanan sonuçlarla kontrol ettim. Projeyi, sonuçların sınırlarını ve son teslim metnini kendi değerlendirmemle gözden geçirdim.” Son cümleyi yalnız gerçekten yaptıktan sonra kullanın; hocanın istediği AIAS kademesini ders tanımına göre doğrulamadan sayı yazmayın.

## Form için doğruluk notu

“Gap doğrulandı mı?” sorusunda mevcut kanıtlarla “Evet, açık bir soru” şıkkı uygun değildir. Kaynaklara bakınca benzer hasta bazlı ve özellik temelli çalışmalar vardır; “Kısmen: bir kısmı çalışılmış” daha savunulabilir. “Kendi cümlelerinle üç cümle” alanını öğrenci yazmalıdır: (1) Kod hangi veriyi okuyor? (2) İlk sayıyı hangi yöntem üretiyor? (3) EKG veya F1 şekli ne gösteriyor? Bu alan için hazır cümle verilmez.

## Henüz doğrulanmamış teslim öğeleri

- Aşama 1'de istenen belirli gündem olayı ve tarihli kaynak.
- Science AI Journal'dan indirilen özgün CSV, RIS ve öneri dosyalarının saklanması; mevcut sayfa metinleri bu dosyaların yerini tutmaz.
- Kişisel Google formunun son gönderim durumu ve sohbetin paylaşım bağlantısı. GitHub URL'si doğrulandı: https://github.com/eminylmz7140/eem4011-ekg-aritmi.
- Google Colab'da bu tam akışın ayrıca çalıştırıldığının kanıtı. Yerel bilgisayarda tam çalıştırma doğrulandı.
