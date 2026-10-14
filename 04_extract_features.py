import argparse
import numpy as np, pandas as pd
from common import DATA, ARTIFACTS, load_primary_lead

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--window",type=int,default=90); args=ap.parse_args(); beats=pd.read_csv(ARTIFACTS/"beats.csv"); rows=[]; cache={}
    for rec, group in beats.groupby("record"):
        rec = str(rec)
        try:
            cache[rec], lead = load_primary_lead(DATA/rec)
            print("Kanal", rec, lead)
        except Exception as e: print("Kayıt atlandı",rec,e); continue
        x=cache[rec]
        for r in group.itertuples(index=False):
            i=int(r.sample); w=x[i-args.window:i+args.window]
            if len(w)!=2*args.window: continue
            rows.append({"record":rec,"sample":i,"label":r.label,"mean":w.mean(),"std":w.std(),"min":w.min(),"max":w.max(),"ptp":np.ptp(w),"rms":np.sqrt(np.mean(w*w))})
    if not rows: raise RuntimeError("Özellik çıkarılamadı.")
    pd.DataFrame(rows).to_csv(ARTIFACTS/"features.csv",index=False); print("Özellik tablosu hazır",len(rows))

if __name__ == "__main__": main()
