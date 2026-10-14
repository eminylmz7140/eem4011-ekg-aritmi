"""Create two publication-style figures from the actual MIT-BIH recording and saved metrics."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import wfdb


LABELS = ["N", "S", "V", "F", "Q"]


def draw_signal(data: Path, output: Path):
    record = wfdb.rdrecord(str(data / "100"))
    ann = wfdb.rdann(str(data / "100"), "atr")
    fs = float(record.fs)
    assert fs == 360, fs
    lead = next((i for i, name in enumerate(record.sig_name) if name.upper() == "MLII"), 0)
    end = int(8 * fs)
    t = np.arange(end) / fs
    signal = record.p_signal[:end, lead]
    assert len(signal) == end and np.isfinite(signal).all()
    selected = [(int(s), symbol) for s, symbol in zip(ann.sample, ann.symbol)
                if s < end and symbol in {"N", "A", "V"}]
    assert any(symbol == "A" for _, symbol in selected)
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.plot(t, signal, color="#18374b", lw=1.05)
    for sample, symbol in selected:
        color = "#d3542e" if symbol != "N" else "#16827e"
        ax.plot(sample / fs, signal[sample], "o", ms=5, color=color)
        if symbol != "N":
            ax.annotate("A anotasyonu (S sınıfı)", (sample / fs, signal[sample]),
                        xytext=(sample / fs + .18, signal[sample] + .65),
                        arrowprops={"arrowstyle": "->", "color": color}, color=color)
    ax.set(xlabel="Zaman (s)", ylabel="Genlik (mV)",
           title="MIT-BIH kayıt 100: ilk 8 saniye, MLII kanalı")
    ax.grid(alpha=.25)
    fig.text(.01, .015, "Kaynak: PhysioNet MIT-BIH v1.0.0. Noktalar referans anotasyonlarıdır; otomatik tespit sonucu değildir.", fontsize=9)
    fig.tight_layout(rect=(0, .05, 1, 1))
    fig.savefig(output, dpi=180)
    plt.close(fig)


def draw_metrics(report: dict, output: Path):
    before = [report["original"]["classification_report"][c]["f1-score"] for c in LABELS]
    after = [report["improved"]["classification_report"][c]["f1-score"] for c in LABELS]
    support = [int(report["improved"]["classification_report"][c]["support"]) for c in LABELS]
    x = np.arange(len(LABELS))
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.bar(x - .18, before, width=.34, label="İlk kNN", color="#8da7b4")
    ax.bar(x + .18, after, width=.34, label="Geliştirilmiş kNN", color="#087f83")
    ax.set_xticks(x, [f"{c}\n(n={n:,})".replace(",", ".") for c, n in zip(LABELS, support)])
    ax.set_ylim(0, 1.04)
    ax.set_ylabel("F1 skoru")
    ax.set_title("Aynı hasta bazlı test bölümünde sınıf bazlı F1")
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=.25)
    ax.set_axisbelow(True)
    def tr(value, digits):
        return f"{value:.{digits}f}".replace(".", ",")
    caption = (
        f"Test: {report['test_beats']:,} atım. "
        f"Macro-F1: {tr(report['original']['macro_f1'], 4)} → {tr(report['improved']['macro_f1'], 4)}; "
        f"doğruluk: %{tr(100 * report['original']['accuracy'], 2)} → "
        f"%{tr(100 * report['improved']['accuracy'], 2)}. "
        f"F desteği: {support[3]} atım."
    ).replace(f"{report['test_beats']:,}", f"{report['test_beats']:,}".replace(",", "."))
    fig.text(.01, .015, caption, fontsize=9)
    fig.tight_layout(rect=(0, .05, 1, 1))
    fig.savefig(output, dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--comparison", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = json.loads(args.comparison.read_text(encoding="utf-8"))
    draw_signal(args.data, args.output / "ekg_kayit100.png")
    draw_metrics(report, args.output / "sinif_f1_karsilastirma.png")
    print("Hazır:", args.output / "ekg_kayit100.png")
    print("Hazır:", args.output / "sinif_f1_karsilastirma.png")


if __name__ == "__main__":
    main()
