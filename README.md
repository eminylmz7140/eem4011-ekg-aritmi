# EEM4011 EKG Aritmi Projesi

MIT-BIH Arrhythmia Database üzerinde hastadan bağımsız EKG atımı sınıflandırması. Temel kNN ve dalga şekli + RR özellikli kNN karşılaştırılır.

**Colab’da çalıştır:** [Defteri aç](https://colab.research.google.com/github/eminylmz7140/eem4011-ekg-aritmi/blob/main/EEM4011_Colab.ipynb). Hücreleri sırayla çalıştırın. İlk hücre proje paketini GitHub’dan indirir; üçüncü hücre MIT-BIH verisini PhysioNet’ten indirip analizi yapar. Tam veri indirme ve analiz uzun sürebilir.

**Tam proje:** [`EEM4011_teslim_paketi.zip`](EEM4011_teslim_paketi.zip). ZIP, kaynak kodu, `proje.md`, Colab defteri, doğrulanmış sonuç özetleri, grafikler ve sunumu özgün klasör yapısıyla içerir. Veri ve eğitilmiş model dosyaları dahil değildir.

**Hızlı erişim:** [`proje.md`](proje.md) · [`EEM4011_Colab.ipynb`](EEM4011_Colab.ipynb) · [`sonuç karşılaştırması`](comparison_improved.json) · [`EKG grafiği`](ekg_kayit100.png) · [`sınıf bazlı F1`](sinif_f1_karsilastirma.png).

Yerel bilgisayarda çalıştırmak için arşivi çıkarıp `biomed_project/README.md` içindeki adımları izleyin. Tam veri kümesi PhysioNet’ten kod tarafından indirilir. Sonuçlar eğitim amaçlıdır; klinik tanı aracı değildir.
