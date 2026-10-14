"""Offline ECG feature improvement, selected only on training-patient validation."""
import argparse
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import wfdb
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import AAMI, DATA, load_primary_lead

LABELS = ["N", "S", "V", "F", "Q"]
BASIC = ["mean", "std", "min", "max", "ptp", "rms"]


def group_id(record):
    return "201_202" if str(record) in {"201", "202"} else str(record)


def build_features(baseline):
    result = baseline.copy()
    extra = []
    for record, rows in baseline.groupby("record", sort=True):
        signal, lead = load_primary_lead(DATA / str(record))
        header = wfdb.rdheader(str(DATA / str(record)))
        fs = float(header.fs)
        if fs != 360:
            raise ValueError(f"Expected MIT-BIH 360 Hz; {record} has {fs} Hz")
        # Use all mapped beat timings, including edge beats omitted from windows.
        ann = wfdb.rdann(str(DATA / str(record)), "atr")
        samples = np.array([s for s, symbol in zip(ann.sample, ann.symbol) if symbol in AAMI])
        for row in rows.itertuples():
            pos = int(np.searchsorted(samples, row.sample))
            assert samples[pos] == row.sample
            previous = (samples[pos] - samples[pos - 1]) / fs if pos else np.nan
            following = (samples[pos + 1] - samples[pos]) / fs if pos + 1 < len(samples) else np.nan
            history = np.diff(samples[max(0, pos - 10):pos + 1]) / fs
            local_rr = float(np.median(history)) if len(history) else 1.0
            previous = float(previous) if np.isfinite(previous) else local_rr
            following = float(following) if np.isfinite(following) else local_rr
            window = signal[int(row.sample) - 90:int(row.sample) + 90]
            assert len(window) == 180 and np.isfinite(window).all()
            centered = window - np.median(window)
            amplitude = max(float(np.ptp(centered)), 1e-6)
            morphology = np.interp(np.linspace(0, 179, 24), np.arange(180), centered / amplitude)
            values = {"row": row.Index, "rr_previous": previous, "rr_next": following,
                      "rr_local": local_rr, "rr_previous_relative": previous / max(local_rr, 1e-6),
                      "rr_next_relative": following / max(local_rr, 1e-6),
                      "rr_change": following - previous}
            values.update({f"shape_{i:02d}": float(v) for i, v in enumerate(morphology)})
            extra.append(values)
        print(f"Features: {record} ({lead})", flush=True)
    extra = pd.DataFrame(extra).set_index("row").reindex(result.index)
    assert not extra.isna().any().any()
    return pd.concat([result, extra], axis=1)


def capped_indices(df, indices, cap):
    if cap is None:
        return np.asarray(indices)
    rng = np.random.default_rng(42)
    selected = []
    for label in LABELS:
        members = np.asarray(indices)[df.iloc[indices].label.to_numpy() == label]
        selected.extend(rng.choice(members, min(len(members), cap), replace=False).tolist())
    return np.asarray(sorted(selected))


def fit_candidate(df, indices, spec):
    selected = capped_indices(df, indices, spec["cap"])
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(
        n_neighbors=spec["k"], weights="distance", n_jobs=1))
    model.fit(df.iloc[selected][spec["features"]], df.iloc[selected].label)
    return model, len(selected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    baseline = pd.read_csv(args.baseline / "features.csv")
    old = joblib.load(args.baseline / "model.joblib")
    train, test = np.array(old["train_index"]), np.array(old["test_index"])
    assert set(train).isdisjoint(test) and set(train) | set(test) == set(range(len(baseline)))
    groups = baseline.record.map(group_id)
    assert set(groups.iloc[train]).isdisjoint(groups.iloc[test])
    if groups.iloc[train].nunique() < 4:
        raise ValueError("İç doğrulama için eğitim kümesinde en az dört hasta grubu gerekir; tam veriyle çalıştırın.")
    df = build_features(baseline)
    df.to_csv(args.output / "features_improved.csv", index=False)
    engineered = BASIC + [c for c in df if c.startswith("rr_") or c.startswith("shape_")]
    assert np.isfinite(df[engineered].to_numpy()).all()
    specs = [
        {"name": "original_6_features", "features": BASIC, "k": 5, "cap": None},
        {"name": "shape_rr_knn5", "features": engineered, "k": 5, "cap": None},
        {"name": "shape_rr_knn5_cap2000", "features": engineered, "k": 5, "cap": 2000},
        {"name": "shape_rr_knn7_cap5000", "features": engineered, "k": 7, "cap": 5000},
    ]
    splits = []
    for seed in (17, 29):
        fit, val = next(GroupShuffleSplit(n_splits=1, test_size=.25, random_state=seed).split(
            df.iloc[train], groups=groups.iloc[train]))
        fit, val = train[fit], train[val]
        assert set(groups.iloc[fit]).isdisjoint(groups.iloc[val])
        assert set(test).isdisjoint(fit) and set(test).isdisjoint(val)
        splits.append((fit, val))
    validation = []
    for spec in specs:
        scores = []
        for fold, (fit, val) in enumerate(splits):
            model, count = fit_candidate(df, fit, spec)
            prediction = model.predict(df.iloc[val][spec["features"]])
            score = float(f1_score(df.iloc[val].label, prediction, labels=LABELS,
                                  average="macro", zero_division=0))
            scores.append(score)
            print(f"Validation {spec['name']} split {fold + 1}: macro-F1={score:.4f}, fit n={count}", flush=True)
        validation.append({"name": spec["name"], "scores": scores, "mean_macro_f1": float(np.mean(scores))})
    best = max(range(len(specs)), key=lambda i: validation[i]["mean_macro_f1"])
    spec = specs[best]
    # Candidate selection is complete before computing any new test prediction.
    (args.output / "selection.json").write_text(json.dumps({"selected": spec["name"],
        "validation": validation, "test_used_for_selection": False}, indent=2), encoding="utf-8")
    model, count = fit_candidate(df, train, spec)
    prediction = model.predict(df.iloc[test][spec["features"]])
    y = df.iloc[test].label
    original_prediction = old["model"].predict(baseline.iloc[test][old["features"]])
    def metrics(pred):
        return {"accuracy": float(accuracy_score(y, pred)),
                "macro_f1": float(f1_score(y, pred, labels=LABELS, average="macro", zero_division=0)),
                "classification_report": classification_report(y, pred, labels=LABELS, output_dict=True, zero_division=0),
                "confusion_matrix": confusion_matrix(y, pred, labels=LABELS).tolist()}
    majority_label = str(df.iloc[train].label.mode().iloc[0])
    report = {"selected_model": spec["name"], "validation": validation,
              "majority_label": majority_label,
              "majority_baseline": metrics(np.full(len(test), majority_label)),
              "baseline_sha256": hashlib.sha256((args.baseline / "features.csv").read_bytes()).hexdigest(),
              "validation_splits": [{"fit_groups": sorted(set(groups.iloc[fit])),
                  "validation_groups": sorted(set(groups.iloc[val])),
                  "validation_support": {label: int((df.iloc[val].label == label).sum()) for label in LABELS}}
                  for fit, val in splits],
              "original": metrics(original_prediction), "improved": metrics(prediction),
              "train_available": len(train), "train_used": count, "test_beats": len(test),
              "feature_count": len(spec["features"]),
              "test_records": sorted(df.iloc[test].record.astype(str).unique().tolist()),
              "limitations": ["Previously reported holdout reused for comparison; external validation still needed.",
                  "Reference beat locations supplied; this does not evaluate automatic R-peak detection.",
                  "Next-RR features require the following beat: offline analysis, not immediate prediction.",
                  "Paced records included; mixed leads (102/104 use V5); not strict EC57 benchmarking.",
                  "Only two internal grouped validation splits; minority-class estimates remain uncertain."]}
    (args.output / "comparison.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    pd.DataFrame({"record": df.iloc[test].record, "sample": df.iloc[test]["sample"],
                  "actual": y, "original": original_prediction, "improved": prediction}).to_csv(
                      args.output / "predictions.csv", index=False)
    joblib.dump({"model": model, "features": spec["features"], "train_index": train.tolist(),
                 "fit_index": capped_indices(df, train, spec["cap"]).tolist(),
                 "test_index": test.tolist(), "selected": spec}, args.output / "model_improved.joblib")
    lines = ["# EEM4011 — Geliştirilmiş kNN karşılaştırması", "",
        f"Aynı {df.record.nunique()} kayıt, {len(df)} atım ve aynı hasta bazlı test bölümü kullanıldı.",
        "Model, yalnızca eğitim hastaları içindeki iki doğrulama bölmesinin ortalama macro-F1 değerine göre seçildi.",
        "", f"Seçilen model: {spec['name']}; {len(spec['features'])} özellik; eğitimde kullanılan atım: {count}.",
        "", "| Ölçüt | Önce | Sonra |", "|---|---:|---:|",
        f"| Accuracy | {report['original']['accuracy']:.4f} | {report['improved']['accuracy']:.4f} |",
        f"| Macro-F1 | {report['original']['macro_f1']:.4f} | {report['improved']['macro_f1']:.4f} |",
        "", "| Sınıf | Önce F1 | Sonra F1 | Test desteği |", "|---|---:|---:|---:|"]
    for label in LABELS:
        before = report['original']['classification_report'][label]
        after = report['improved']['classification_report'][label]
        lines.append(f"| {label} | {before['f1-score']:.4f} | {after['f1-score']:.4f} | {int(after['support'])} |")
    lines += ["", "Adaylarda dalga şekli ve RR özellikleri değerlendirildi.",
        f"Seçilen modelin sınıf başına örnek sınırı: {spec['cap'] if spec['cap'] else 'sınır yok'}.",
        f"Karşılaştırma amacıyla hep eğitimdeki çoğunluk sınıfını ({majority_label}) tahmin eden model: "
        f"accuracy={report['majority_baseline']['accuracy']:.4f}, macro-F1={report['majority_baseline']['macro_f1']:.4f}.",
        "Macro-F1 ve accuracy değişimleri ayrı yorumlanmalıdır; sınıf bazlı sonuçlar yukarıdadır.",
        "", "Sınırlar: Önceden raporlanmış test grubu tekrar kullanıldı; sonuç dış doğrulama değildir. "
        "R tepe konumları referans anotasyonlardan alınır. Sonraki RR bilgisi kullanıldığından yöntem çevrimdışıdır. "
        "Pacing kayıtları ve farklı lead'ler dahil; katı EC57 karşılaştırması değildir. "
        f"F sınıfının testte {int(report['improved']['classification_report']['F']['support'])} örneği vardır."]
    (args.output / "results_improved.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"selected": spec["name"], "original_macro_f1": report["original"]["macro_f1"],
                      "new_macro_f1": report["improved"]["macro_f1"],
                      "new_accuracy": report["improved"]["accuracy"]}), flush=True)


if __name__ == "__main__":
    main()
