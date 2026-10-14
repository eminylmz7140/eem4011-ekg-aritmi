import importlib.util, sys
required = ["numpy", "pandas", "wfdb", "sklearn", "joblib"]
missing = [p for p in required if importlib.util.find_spec(p) is None]
if missing:
    print("Eksik paketler:", ", ".join(missing))
    print("Colab: !pip -q install wfdb scikit-learn pandas numpy")
    sys.exit(1)
import numpy, pandas, wfdb, sklearn
print("Ortam hazır")
print("numpy", numpy.__version__, "pandas", pandas.__version__, "wfdb", wfdb.__version__, "sklearn", sklearn.__version__)
