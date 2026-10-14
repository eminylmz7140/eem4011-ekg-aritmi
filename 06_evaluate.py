import json, joblib, pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, multilabel_confusion_matrix
from common import ARTIFACTS
def main():
    df=pd.read_csv(ARTIFACTS/"features.csv"); bundle=joblib.load(ARTIFACTS/"model.joblib"); idx=bundle["test_index"]; X=df.iloc[idx][bundle["features"]]; y=df.iloc[idx].label; pred=bundle["model"].predict(X)
    labels=["N","S","V","F","Q"]
    test_records=sorted(df.iloc[idx].record.astype(str).unique().tolist())
    class_cm=multilabel_confusion_matrix(y,pred,labels=labels)
    specificity={label:(float(cm[0,0]/(cm[0,0]+cm[0,1])) if (cm[0,0]+cm[0,1]) else 0.0) for label,cm in zip(labels,class_cm)}
    result={"evaluation_note":"AAMI-inspired five-class mapping; paced records are included, so this is not a strict EC57 benchmark. This is a single group holdout educational baseline, not clinical performance. Interpret metrics with class support and class imbalance.","accuracy":float(accuracy_score(y,pred)),"macro_f1":float(f1_score(y,pred,labels=labels,average="macro",zero_division=0)),"labels":labels,"test_records":test_records,"test_class_support":{label:int((y==label).sum()) for label in labels},"specificity_one_vs_rest":specificity,"classification_report":classification_report(y,pred,labels=labels,zero_division=0,output_dict=True),"confusion_matrix":confusion_matrix(y,pred,labels=labels).tolist()}
    (ARTIFACTS/"metrics.json").write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8"); print("accuracy",result["accuracy"],"macro_f1",result["macro_f1"]); print("one-vs-rest specificity",specificity); print(classification_report(y,pred,labels=labels,zero_division=0))
if __name__ == "__main__": main()
