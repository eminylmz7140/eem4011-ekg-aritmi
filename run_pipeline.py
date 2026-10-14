import argparse, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def run(script,*args):
    print("\n===",script,"==="); subprocess.run([sys.executable,str(ROOT/script),*args],check=True)
def main():
    ap=argparse.ArgumentParser(description="MIT-BIH EKG kNN pipeline"); ap.add_argument("--records",nargs="+",default=None,help="İsteğe bağlı küçük kayıt listesi. Varsayılan tüm veri setidir."); ap.add_argument("--local-only",action="store_true",help="Ağdan indirmeden data/ içindeki kayıtları kullan."); ap.add_argument("--improve",action="store_true",help="Hasta gruplu iç doğrulamayla geliştirilmiş kNN seç ve doğrula."); a=ap.parse_args()
    if a.local_only and a.records: ap.error("--local-only ile --records birlikte kullanılamaz")
    run("01_environment.py")
    download_args=("--local-only",) if a.local_only else (("--records",*a.records) if a.records else ())
    run("02_download_data.py",*download_args)
    read_args=("--records",*a.records) if a.records else ()
    run("03_read_records.py",*read_args)
    run("04_extract_features.py"); run("05_split_and_model.py"); run("06_evaluate.py")
    if a.improve:
        from common import ARTIFACTS
        run("07_improve_model.py", "--baseline", str(ARTIFACTS), "--output", str(ARTIFACTS / "improved"))
        run("08_verify_improvement.py", "--baseline", str(ARTIFACTS), "--output", str(ARTIFACTS / "improved"))
if __name__=="__main__": main()
