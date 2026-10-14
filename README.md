# EEM4011 EKG Projesi

## Aşama 2 — Makine öğrenmesiz sinyal işleme

MIT-BIH veri kümesinin **48 EKG kaydında** R tepeleri iki yöntemle bulundu. Ham eşik için F1 **0,8306**; 5–15 Hz filtre ve enerji zarfıyla F1 **0,9805**. Bu sayılar tüm kayıtlar yeniden çalıştırılarak doğrulandı.

**[Aşama 2 Colab defterini aç](https://colab.research.google.com/github/eminylmz7140/eem4011-ekg-aritmi/blob/main/EEM4011_Asama2_Colab.ipynb)** · [Proje açıklaması](asama2_ekg_sinyal_isleme.md) · [Form için doğrulanmış bilgiler](asama2_form_hazirlik.md) · [Sonuçlar](phase2_results.json) · [EKG ve tepe grafiği](rpeak_kayit100.png)

Hücreleri sırayla çalıştırın. Veri arşivi PhysioNet’ten indirilir; bu işlem uzun sürebilir. Yerel çalıştırma: paketi açıp `biomed_project/README.md` dosyasındaki Aşama 2 adımlarını izleyin.

## Vize sonrası genişletme

[kNN ile aritmi sınıflandırması](proje.md) ve [ayrı Colab defteri](EEM4011_Colab.ipynb) vize sonrası içindir. Bu sonuçları Aşama 2 formunda kullanmayın.

[Tam teslim paketi](EEM4011_teslim_paketi.zip) kodu, belgeleri, sonuçları, grafikleri ve sunumu içerir. Ham EKG verisi ve eğitilmiş modeller pakete veya depoya yüklenmemiştir. Bu çalışma eğitim amaçlıdır; klinik tanı aracı değildir.
