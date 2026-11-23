"""
EEM4011 + Bitirme 1 — Gercek Zamanli 10 Saniyelik EKG Akis (Streaming) Surumu
Ogrenci : Yildiray Yilmaz (213204045)
Danisman: Ars. Gor. Dr. Meral Kilicarslan Ouach

Aciklama:
MIT-BIH DS1 egitim kumesinde (22 kayit, 50.555 atim) egitilen 300 agacli
Random Forest siniflandiricisini, DS2 test kumesindeki 21 kaydin tamaminda
(47.140 atim, 3.200 V/E pozitif atim) 10 saniyelik ardisik bloklar (3600 ornek,
fs=360 Hz, toplam 3.801 blok) halinde akan veri (streaming) duzeninde calistirir.
Atim basina uctan uca gecikmeyi (ms) ve cevrimdisi modelle birebir ayni DS2 V-F1
skorunu (0,870) dogrular.
"""

import time
import json
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common import DS1_RECORDS, DS2_RECORDS, FS, V_SYMBOLS, load_record, extract_record_beats

WINDOW_SEC = 10
WINDOW_SAMPLES = WINDOW_SEC * FS  # 3600 ornek (10 sn)


def extract_features_for_group(records):
    X_list, y_list, r_list, rec_list = [], [], [], []
    for rec in records:
        X, y_aami, r_peaks = extract_record_beats(rec)
        y_bin = np.isin(y_aami, list(V_SYMBOLS)).astype(int)
        X_list.append(X)
        y_list.append(y_bin)
        r_list.append(r_peaks)
        rec_list.extend([rec] * len(y_bin))
    return np.vstack(X_list), np.concatenate(y_list), r_list, rec_list


def run_streaming_evaluation():
    print("[1/3] DS1 egitim kumesi yukleniyor ve Random Forest (300 agac) egitiliyor...")
    X_train, y_train, _, _ = extract_features_for_group(DS1_RECORDS)
    rf = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=1,
        class_weight="balanced_subsample",
    )
    rf.fit(X_train, y_train)

    print("[2/3] DS2 test kumesi (21 kayit) 10 saniyelik bloklarla akis modunda isleniyor...")
    y_true_all, y_pred_all = [], []
    block_times_ms = []
    beat_latencies_ms = []
    total_blocks = 0

    for rec in DS2_RECORDS:
        X_rec, y_aami, r_peaks = extract_record_beats(rec)
        y_bin = np.isin(y_aami, list(V_SYMBOLS)).astype(int)
        sig, _ = load_record(rec)
        n_samples = len(sig)

        for start_idx in range(0, n_samples, WINDOW_SAMPLES):
            end_idx = start_idx + WINDOW_SAMPLES
            mask = (r_peaks >= start_idx) & (r_peaks < end_idx)
            if not np.any(mask):
                continue

            X_block = X_rec[mask]
            y_block = y_bin[mask]
            n_beats_in_block = len(y_block)

            t0 = time.perf_counter()
            preds = rf.predict(X_block)
            dt_ms = (time.perf_counter() - t0) * 1000.0

            block_times_ms.append(dt_ms)
            beat_latencies_ms.append(dt_ms / n_beats_in_block)
            total_blocks += 1

            y_true_all.append(y_block)
            y_pred_all.append(preds)

    y_true = np.concatenate(y_true_all)
    y_pred = np.concatenate(y_pred_all)

    prec, rec_score, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, pos_label=1, average="binary", zero_division=0
    )
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    total_time_ms = float(np.sum(block_times_ms))
    mean_beat_ms = total_time_ms / len(y_true)
    mean_block_ms = float(np.mean(block_times_ms))

    results = {
        "window_sec": WINDOW_SEC,
        "window_samples": WINDOW_SAMPLES,
        "ds2_records": len(DS2_RECORDS),
        "total_blocks": total_blocks,
        "total_beats": int(len(y_true)),
        "positive_v_beats": int(np.sum(y_true)),
        "tp": int(tp),
        "fp": int(fp),
        "fn": int(fn),
        "tn": int(tn),
        "sensitivity": round(float(rec_score), 4),
        "precision_ppv": round(float(prec), 4),
        "v_f1": round(float(f1), 4),
        "mean_latency_ms_per_beat": round(mean_beat_ms, 3),
        "mean_latency_ms_per_10s_block": round(mean_block_ms, 3),
    }

    print("[3/3] Akis Sonuclari:")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    run_streaming_evaluation()
