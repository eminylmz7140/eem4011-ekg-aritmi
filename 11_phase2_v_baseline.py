"""Aşama 2: DS1'de seçilen eğitimsiz şablon-korelasyon eşiğiyle V atımı.

MIT-BIH Arrhythmia Database v1.0.0 kayıtları DATA dizininde olmalıdır.
Pacemaker kayıtları ve 201 ile aynı kişiye ait 202 dışarıda tutulur.
"""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import wfdb

from common import DATA


DS1 = "101 106 108 109 112 114 115 116 118 119 122 124 201 203 205 207 208 209 215 220 223 230".split()
DS2 = "100 103 105 111 113 117 121 123 200 210 212 213 214 219 221 222 228 231 232 233 234".split()
ELIGIBLE = set("N L R e j A a J S V E".split())
ALL_BEATS = ELIGIBLE | set("F / f Q".split())
POSITIVE = {"V", "E"}
NONSUPRAVENTRICULAR = set("N L R e j A a J S".split())
FS = 360
BEFORE = 36
AFTER = 54
THRESHOLDS = np.round(np.arange(0.30, 0.951, 0.05), 2)


def read_record(name):
    path = DATA / name
    for ext in ("hea", "dat", "atr"):
        if not path.with_suffix("." + ext).is_file():
            raise FileNotFoundError(path.with_suffix("." + ext))
    header = wfdb.rdheader(str(path))
    indices = [i for i, label in enumerate(header.sig_name) if label.strip().upper() == "MLII"]
    if len(indices) != 1:
        raise ValueError(f"{name}: tek MLII kanalı bekleniyor, bulunan: {header.sig_name}")
    rec = wfdb.rdrecord(str(path), channels=indices)
    if int(rec.fs) != FS:
        raise ValueError(f"{name}: örnekleme frekansı {rec.fs}, beklenen {FS}")
    ann = wfdb.rdann(str(path), "atr")
    idx = [i for i, symbol in enumerate(ann.symbol) if symbol in ALL_BEATS]
    positions = np.asarray(ann.sample, dtype=np.int64)[idx]
    symbols = np.asarray(ann.symbol, dtype="U1")[idx]
    return rec.p_signal[:, 0], positions, symbols


def features(signal, positions, symbols):
    windows = np.full((len(positions), BEFORE + AFTER), np.nan, dtype=np.float64)
    fits = (positions >= BEFORE) & (positions + AFTER <= len(signal))
    for row in np.flatnonzero(fits):
        p = positions[row]
        windows[row] = signal[p - BEFORE : p + AFTER]
    template = np.nanmedian(windows, axis=0)
    if not np.isfinite(template).all():
        raise ValueError("Şablon tamamen oluşturulamadı")
    valid_count = np.sum(np.isfinite(windows), axis=1, keepdims=True)
    row_mean = np.divide(
        np.nansum(windows, axis=1, keepdims=True),
        valid_count,
        out=np.zeros((len(windows), 1)),
        where=valid_count > 0,
    )
    w = windows - row_mean
    t = template - template.mean()
    denom = np.sqrt(np.nansum(w * w, axis=1) * np.sum(t * t))
    corr = np.divide(np.nansum(w * t, axis=1), denom, out=np.full(len(w), np.nan), where=denom > 0)
    rr = np.diff(positions) / FS
    rr_before = np.r_[np.nan, rr]
    rr_after = np.r_[rr, np.nan]
    eligible = np.isin(symbols, list(ELIGIBLE)) & fits & np.isfinite(corr)
    eligible[0] = False
    eligible[-1] = False
    eligible &= np.isfinite(rr_before) & np.isfinite(rr_after)
    return {
        "windows": windows,
        "template": template,
        "corr": corr,
        "rr_before": rr_before,
        "rr_after": rr_after,
        "eligible": eligible,
        "label": np.isin(symbols, list(POSITIVE)),
    }


def score(label, prediction):
    tp = int(np.sum(label & prediction))
    fp = int(np.sum(~label & prediction))
    fn = int(np.sum(label & ~prediction))
    sensitivity = tp / (tp + fn) if tp + fn else 0.0
    ppv = tp / (tp + fp) if tp + fp else 0.0
    f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0
    return {"TP": tp, "FP": fp, "FN": fn, "Se": sensitivity, "PPV": ppv, "F1": f1}


def plot_record_119(signal, positions, symbols, feats, target):
    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    sec = min(10 * FS, len(signal))
    axes[0].plot(np.arange(sec) / FS, signal[:sec], color="black", linewidth=0.75)
    for name, mask, color, marker in [
        ("N/S", np.isin(symbols, list(NONSUPRAVENTRICULAR)) & (positions < sec), "green", "o"),
        ("V", np.isin(symbols, list(POSITIVE)) & (positions < sec), "red", "x"),
    ]:
        axes[0].scatter(positions[mask] / FS, signal[positions[mask]], c=color, marker=marker, s=32, label=name)
    axes[0].set(xlabel="Zaman (s)", ylabel="mV", title="Kayıt 119 – ilk 10 saniye")
    axes[0].legend()
    times = np.arange(-BEFORE, AFTER) / FS * 1000
    axes[1].plot(times, feats["template"], color="black", linewidth=2.2, label="Medyan şablon")
    for name, mask, color in [
        ("N pencereleri", (symbols == "N") & feats["eligible"], "green"),
        ("V pencereleri", (symbols == "V") & feats["eligible"], "red"),
    ]:
        for j, row in enumerate(np.flatnonzero(mask)[:20]):
            axes[1].plot(times, feats["windows"][row], color=color, alpha=0.35, linewidth=0.8, label=name if j == 0 else None)
    axes[1].set(xlabel="R işaretine göre zaman (ms)", ylabel="mV", title="Kayıt 119 – şablon ve V atımları")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(target, dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/phase2_v"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if len(DS1) != 22 or len(DS2) != 21 or set(DS1) & set(DS2) or "202" in DS1 + DS2:
        raise AssertionError("DS1/DS2 ayrımı geçersiz")

    per_record = {}
    all_data = {"DS1": [], "DS2": []}
    for group, names in [("DS1", DS1), ("DS2", DS2)]:
        for name in names:
            signal, positions, symbols = read_record(name)
            feat = features(signal, positions, symbols)
            mask = feat["eligible"]
            all_data[group].append((feat["corr"][mask], feat["label"][mask], symbols[mask]))
            per_record[name] = {"group": group, "lead": "MLII", "eligible_beats": int(mask.sum()), "V_E": int(feat["label"][mask].sum())}
            if name == "119":
                plot_record_119(signal, positions, symbols, feat, args.output / "sekil1_sablon_119.png")
            print(group, name, per_record[name]["eligible_beats"], per_record[name]["V_E"], flush=True)

    combined = {}
    for group in ("DS1", "DS2"):
        combined[group] = tuple(np.concatenate([record[i] for record in all_data[group]]) for i in range(3))
    ds1_corr, ds1_label, ds1_symbols = combined["DS1"]
    ds2_corr, ds2_label, _ = combined["DS2"]
    check_ns = float(np.median(ds1_corr[np.isin(ds1_symbols, list(NONSUPRAVENTRICULAR))]))
    check_v = float(np.median(ds1_corr[np.isin(ds1_symbols, list(POSITIVE))]))
    if not check_ns > check_v:
        raise AssertionError(f"Sağlama başarısız: DS1 N/S medyanı {check_ns} <= V medyanı {check_v}")
    threshold_scores = [(float(t), score(ds1_label, ds1_corr < t)) for t in THRESHOLDS]
    selected_t, selected_ds1 = max(threshold_scores, key=lambda item: (item[1]["F1"], -item[0]))
    result = {
        "dataset": "MIT-BIH Arrhythmia Database v1.0.0",
        "groups": {"DS1": DS1, "DS2": DS2},
        "record_count": 43,
        "excluded_records": ["102", "104", "107", "202", "217"],
        "lead": "MLII",
        "reference_r_locations": "PhysioNet .atr annotations; not an automatic R detector",
        "eligible_beat_counts": {group: len(combined[group][0]) for group in combined},
        "positive_beat_counts": {group: int(combined[group][1].sum()) for group in combined},
        "ds1_corr_median_non_v": check_ns,
        "ds1_corr_median_v": check_v,
        "threshold_grid": [float(x) for x in THRESHOLDS],
        "selected_T_on_DS1": selected_t,
        "DS1_selected": selected_ds1,
        "DS2_baseline": score(ds2_label, ds2_corr < selected_t),
        "records": per_record,
    }
    path = args.output / "results.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Baseline DS2 V-F1 = %.3f (T = %.2f)" % (result["DS2_baseline"]["F1"], selected_t))
    print("Sonuçlar:", path)


if __name__ == "__main__":
    main()
