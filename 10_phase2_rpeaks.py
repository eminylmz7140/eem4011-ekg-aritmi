"""Aşama 2: MIT-BIH üzerinde makine öğrenmesiz R-tepe tespiti."""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, find_peaks, sosfiltfilt
import wfdb

from common import AAMI, DATA, ARTIFACTS, load_primary_lead


def reference_samples(base):
    ann = wfdb.rdann(str(base), "atr")
    return np.asarray(
        [sample for sample, symbol in zip(ann.sample, ann.symbol) if symbol in AAMI],
        dtype=np.int64,
    )


def raw_detector(signal, fs):
    x = np.abs(signal - np.median(signal))
    low, high = np.percentile(x, [50, 95])
    threshold = low + 0.35 * (high - low)
    peaks, _ = find_peaks(x, height=threshold, distance=round(0.25 * fs))
    return peaks


def filtered_detector(signal, fs):
    sos = butter(2, [5, 15], btype="bandpass", fs=fs, output="sos")
    band = sosfiltfilt(sos, signal)
    energy = np.diff(band, prepend=band[0]) ** 2
    width = max(1, round(0.12 * fs))
    envelope = np.convolve(energy, np.ones(width) / width, mode="same")
    low, high = np.percentile(envelope, [50, 95])
    threshold = low + 0.35 * (high - low)
    candidates, _ = find_peaks(
        envelope, height=threshold, distance=round(0.25 * fs)
    )
    radius = round(0.10 * fs)
    corrected = []
    for candidate in candidates:
        left, right = max(0, candidate - radius), min(len(band), candidate + radius + 1)
        corrected.append(left + int(np.argmax(np.abs(band[left:right]))))
    return np.unique(corrected)


def counts(detected, reference, tolerance):
    """Sorted, one-to-one matching; each annotation can match one detection."""
    i = j = tp = 0
    while i < len(detected) and j < len(reference):
        delta = int(detected[i]) - int(reference[j])
        if abs(delta) <= tolerance:
            tp += 1
            i += 1
            j += 1
        elif delta < 0:
            i += 1
        else:
            j += 1
    return {"tp": tp, "fp": len(detected) - tp, "fn": len(reference) - tp}


def metrics(c):
    precision = c["tp"] / (c["tp"] + c["fp"]) if c["tp"] + c["fp"] else 0.0
    recall = c["tp"] / (c["tp"] + c["fn"]) if c["tp"] + c["fn"] else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {**c, "precision": precision, "recall": recall, "f1": f1}


def plot_example(signal, fs, reference, raw, filtered, destination):
    stop = min(len(signal), round(10 * fs))
    time = np.arange(stop) / fs
    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.plot(time, signal[:stop], lw=0.7, color="#405b80", label="EKG")
    for peaks, color, label, marker in (
        (reference, "#111111", "Uzman anotasyonu", "|"),
        (raw, "#c73b2d", "Ham eşik", "x"),
        (filtered, "#23834c", "Filtre + zarf", "+"),
    ):
        visible = peaks[peaks < stop]
        ax.scatter(visible / fs, signal[visible], color=color, marker=marker,
                   s=42, label=label, zorder=3)
    ax.set(xlabel="Zaman (s)", ylabel="Genlik (mV)", title="MIT-BIH kayıt 100: ilk 10 saniye")
    ax.legend(ncol=4, fontsize=8)
    fig.tight_layout()
    fig.savefig(destination, dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DATA)
    parser.add_argument("--output", type=Path, default=ARTIFACTS / "phase2")
    parser.add_argument("--records", nargs="+", default=None)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    records = args.records or sorted(path.stem for path in args.data.glob("*.hea"))
    if not records:
        raise RuntimeError("Veri klasöründe MIT-BIH kayıtları bulunamadı.")
    rows = []
    for record_id in records:
        base = args.data / str(record_id)
        if not all(base.with_suffix("." + ext).exists() for ext in ("hea", "dat", "atr")):
            raise FileNotFoundError(f"Eksik kayıt: {record_id}")
        signal, lead = load_primary_lead(base)
        fs = wfdb.rdheader(str(base)).fs
        reference = reference_samples(base)
        raw = raw_detector(signal, fs)
        filtered = filtered_detector(signal, fs)
        tolerance = round(0.15 * fs)
        row = {"record": record_id, "lead": lead, "fs": fs,
               "reference_count": len(reference),
               "raw": metrics(counts(raw, reference, tolerance)),
               "filtered": metrics(counts(filtered, reference, tolerance))}
        rows.append(row)
        print(f"{record_id}: ham F1={row['raw']['f1']:.4f}; filtreli F1={row['filtered']['f1']:.4f}", flush=True)
        if str(record_id) == "100":
            plot_example(signal, fs, reference, raw, filtered,
                         args.output / "rpeak_kayit100.png")
    totals = {}
    for method in ("raw", "filtered"):
        c = {key: sum(row[method][key] for row in rows) for key in ("tp", "fp", "fn")}
        totals[method] = metrics(c)
    result = {"dataset": "MIT-BIH Arrhythmia Database v1.0.0",
              "record_count": len(rows), "reference_beat_count": sum(r["reference_count"] for r in rows),
              "match_tolerance_seconds": 0.15, "methods": totals, "per_record": rows,
              "limitations": ["Referans konumları algoritmada kullanılmaz; yalnız değerlendirmede kullanılır.",
                              "Filtre ve eşik parametreleri sabittir; dış veri kümesinde doğrulama yapılmamıştır.",
                              "Bu çalışma klinik tanı aracı değildir."]}
    (args.output / "results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "per_record"},
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
