from pathlib import Path
import json
import os
import wfdb

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get("EEM4011_DATA_DIR", ROOT / "data"))
ARTIFACTS = Path(os.environ.get("EEM4011_ARTIFACTS_DIR", ROOT / "artifacts"))
DATA.mkdir(parents=True, exist_ok=True)
ARTIFACTS.mkdir(parents=True, exist_ok=True)

AAMI = {"N":"N", "L":"N", "R":"N", "e":"N", "j":"N", "A":"S", "a":"S", "J":"S", "S":"S", "V":"V", "E":"V", "F":"F", "/":"Q", "f":"Q", "Q":"Q"}

def load_primary_lead(record_path):
    """Load a consistent lead where possible: MLII, then II, then first lead."""
    record = wfdb.rdrecord(str(record_path))
    names = [str(name).strip().upper() for name in record.sig_name]
    index = next((i for i, name in enumerate(names) if name == "MLII"), None)
    if index is None:
        index = next((i for i, name in enumerate(names) if name in {"II", "ECG II"}), 0)
    return record.p_signal[:, index], record.sig_name[index]

def save_json(name, value):
    path = ARTIFACTS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
