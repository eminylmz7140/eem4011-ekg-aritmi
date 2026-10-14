import argparse
from pathlib import Path
import pandas as pd, wfdb
import json
from common import DATA, ARTIFACTS, AAMI

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--records", nargs="+", default=None); args=ap.parse_args(); rows=[]
    records=args.records
    if records is None:
        manifest=json.loads((ARTIFACTS/"download_manifest.json").read_text(encoding="utf-8"))
        records=manifest["records_downloaded"]
    for rec in records:
        try:
            base=DATA/str(rec); ann=wfdb.rdann(str(base), "atr")
            for i,sample in enumerate(ann.sample):
                symbol=ann.symbol[i]
                if symbol not in AAMI: continue
                rows.append({"record":str(rec),"sample":int(sample),"symbol":symbol,"label":AAMI[symbol]})
            print("Okundu", rec, "anotasyon", len(ann.sample))
        except Exception as e: print(f"Atlandı {rec}: {type(e).__name__}: {e}")
    if not rows: raise RuntimeError("Okunabilir anotasyon bulunamadı.")
    out=ARTIFACTS/"beats.csv"; pd.DataFrame(rows).to_csv(out,index=False); print("Yazıldı",out)

if __name__ == "__main__": main()
