import argparse, joblib, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from common import ARTIFACTS

FEATURES=["mean","std","min","max","ptp","rms"]
def patient_group(record):
    # MIT-BIH records 201 and 202 come from the same subject.
    return "201_202" if str(record) in {"201", "202"} else str(record)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--test-size",type=float,default=.2); args=ap.parse_args(); df=pd.read_csv(ARTIFACTS/"features.csv")
    if df.record.nunique()<2: raise RuntimeError("Test ayrımı için en az iki kayıt gerekir.")
    groups=df.record.map(patient_group)
    tr,te=next(GroupShuffleSplit(n_splits=1,test_size=args.test_size,random_state=42).split(df,df.label,groups=groups))
    model=make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=5,weights="distance")); model.fit(df.iloc[tr][FEATURES],df.iloc[tr].label)
    joblib.dump({"model":model,"train_index":tr.tolist(),"test_index":te.tolist(),"features":FEATURES},ARTIFACTS/"model.joblib")
    pd.DataFrame({"index":te,"label":df.iloc[te].label.values}).to_csv(ARTIFACTS/"test_index.csv",index=False)
    print("Model hazır",len(tr),"eğitim",len(te),"test", "hasta grupları:", groups.iloc[tr].unique().tolist(), "|", groups.iloc[te].unique().tolist())

if __name__ == "__main__": main()
