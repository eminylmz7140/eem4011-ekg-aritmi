"""Audit partitions, preprocessing and measured improvement against saved predictions."""
import argparse
import hashlib
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    original = pd.read_csv(args.baseline / "features.csv")
    df = pd.read_csv(args.output / "features_improved.csv")
    old = joblib.load(args.baseline / "model.joblib")
    new = joblib.load(args.output / "model_improved.joblib")
    report = json.loads((args.output / "comparison.json").read_text(encoding="utf-8"))
    prediction_file = pd.read_csv(args.output / "predictions.csv")
    groups = df.record.map(lambda r: "201_202" if str(r) in {"201", "202"} else str(r))
    assert original[["record", "sample", "label"]].equals(df[["record", "sample", "label"]])
    assert report["baseline_sha256"] == hashlib.sha256((args.baseline / "features.csv").read_bytes()).hexdigest()
    assert old["train_index"] == new["train_index"] and old["test_index"] == new["test_index"]
    train, test, fit = new["train_index"], new["test_index"], new["fit_index"]
    assert set(fit).issubset(train) and len(set(fit)) == len(fit)
    assert set(train).isdisjoint(test) and set(train) | set(test) == set(range(len(df)))
    test_groups = set(groups.iloc[test])
    assert not set(groups.iloc[train]) & test_groups
    for split in report["validation_splits"]:
        assert not set(split["fit_groups"]) & set(split["validation_groups"])
        assert not (set(split["fit_groups"]) | set(split["validation_groups"])) & test_groups
    assert not {"record", "sample", "label"} & set(new["features"])
    assert np.isfinite(df[new["features"]].to_numpy()).all()
    np.testing.assert_allclose(new["model"][0].mean_, df.iloc[fit][new["features"]].mean().to_numpy(), rtol=1e-10, atol=1e-10)
    assert new["model"][-1].n_samples_fit_ == len(fit) == report["train_used"]
    assert report["selected_model"] == max(report["validation"], key=lambda x: x["mean_macro_f1"])["name"]
    labels = ["N", "S", "V", "F", "Q"]
    y = df.iloc[test].label
    assert prediction_file.actual.tolist() == y.tolist()
    assert report['majority_label'] == df.iloc[train].label.mode().iloc[0]
    majority = np.full(len(test), report['majority_label'])
    assert abs(accuracy_score(y, majority) - report['majority_baseline']['accuracy']) < 1e-12
    for key, bundle, frame in [("original", old, original), ("improved", new, df)]:
        pred = bundle["model"].predict(frame.iloc[test][bundle["features"]])
        assert pred.tolist() == prediction_file[key].tolist()
        assert abs(accuracy_score(y, pred) - report[key]["accuracy"]) < 1e-12
        assert abs(f1_score(y, pred, labels=labels, average="macro", zero_division=0) - report[key]["macro_f1"]) < 1e-12
        assert confusion_matrix(y, pred, labels=labels).tolist() == report[key]["confusion_matrix"]
    print("PASS: same test samples; disjoint patients; train-only scaling/sampling/selection; saved predictions and metrics match.")


if __name__ == "__main__":
    main()
