# EEM4011 EKG Projesi

## Aşama 2 — Ana proje: hasta bazlı V atımı tespiti

MIT-BIH Arrhythmia Database v1.0.0'daki 43 kaydın MLII kanalında, anotasyonlu R konumlarından çıkarılan atım pencereleri bir şablonla karşılaştırıldı. Eşik yalnız 22 kayıtlı DS1'de seçildi, 21 kayıtlı DS2'de bir kez sınandı. Pacemaker kayıtları ve aynı hastaya ait 202 dışarıda bırakıldı.

Doğrulanmış başlangıç sonucu: **DS2 V-F1 = 0,702** (T = 0,90; TP 3.027, FP 2.398, FN 173; Se 0,946; PPV 0,558). Bu, eğitimsiz şablon-korelasyon kuralıdır. İyileştirme ve makine öğrenmesi sonuçları bu sayıya dahil değildir.

[Aşama 2 Colab defterini aç](https://colab.research.google.com/github/eminylmz7140/eem4011-ekg-aritmi/blob/main/EEM4011_Asama2_V_Colab.ipynb) · [Yöntem ve sınırlamalar](asama2_v_baseline.md) · [Kaynak kod](11_phase2_v_baseline.py) · [Doğrulanmış sonuç JSON](phase2_v_results.json) · [Şekil 1](sekil1_sablon_119.png)

Colab hücrelerini sırayla çalıştırın. Veri PhysioNet'ten indirilir ve veri arşivinin büyüklüğü nedeniyle uzun sürebilir. [Tam teslim paketi](EEM4011_teslim_paketi.zip) kaynak kodu ve raporları içerir; ham EKG verisi ve eğitilmiş model içermez.

## Ayrı deneyler ve vize sonrası genişletme

[48 kayıtlı R-tepesi sinyal işleme deneyi](asama2_ekg_sinyal_isleme.md) ayrı bir alıştırmadır; onun F1 değerleri ana projenin V-F1 alanında kullanılmaz. [kNN aritmi sınıflandırması](proje.md) vize sonrası genişletmedir. Klinik tanı aracı değildir.
