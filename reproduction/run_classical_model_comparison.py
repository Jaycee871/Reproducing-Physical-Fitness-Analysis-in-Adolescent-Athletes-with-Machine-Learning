from pathlib import Path
from importlib.metadata import version
import time
import warnings

import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

DATASET = Path("original/sports datasets.csv")
REPORT = Path("notes/classical_model_comparison.md")
CSV_OUT = Path("reproduction/results/classical_model_metrics.csv")

TARGET = "sports types"
TEST_SIZE = 0.20
RANDOM_STATE = 42

if not DATASET.exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET}")

df = pd.read_csv(DATASET)
feature_columns = [c for c in df.columns if c != TARGET]
X = df[feature_columns].copy()
y_text = df[TARGET].copy()

# Keep human-readable labels through the split, then fit the encoder only on
# the training labels. This numeric mapping is a reconstruction convention
# needed for XGBoost compatibility; it is not claimed to be the unpublished
# class-ID mapping used by the original authors.
X_train, X_test, y_train_text, y_test_text = train_test_split(
    X,
    y_text,
    test_size=TEST_SIZE,
    stratify=y_text,
    random_state=RANDOM_STATE,
)

encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train_text)
y_test = encoder.transform(y_test_text)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

smote = SMOTE(random_state=RANDOM_STATE)
X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

label_names = list(encoder.classes_)
label_ids = list(range(len(label_names)))

models = {
    "Logistic Regression": OneVsRestClassifier(
        LogisticRegression(
            C=36.380497,
            max_iter=11,
            random_state=RANDOM_STATE,
            solver="lbfgs",
        ),
        n_jobs=-1,
    ),
    "SVM": SVC(
        C=39.689206,
        gamma=0.551907,
        probability=False,
        random_state=RANDOM_STATE,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=124,
        max_depth=11,
        max_features=0.356285,
        min_samples_split=3,
        min_samples_leaf=3,
        n_jobs=-1,
        random_state=RANDOM_STATE,
    ),
    "XGBoost": XGBClassifier(
        n_estimators=147,
        max_depth=8,
        max_features=0.353969,
        n_jobs=-1,
        random_state=RANDOM_STATE,
        eval_metric="mlogloss",
        verbosity=0,
    ),
}

rows = []
confusion_matrices = {}
warning_log = {}

for name, model in models.items():
    caught = []
    start = time.perf_counter()

    with warnings.catch_warnings(record=True) as records:
        warnings.simplefilter("always")
        model.fit(X_train_smote, y_train_smote)
        caught = [str(w.message) for w in records]

    train_seconds = time.perf_counter() - start

    pred = model.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, pred)
    macro_f1 = f1_score(y_test, pred, average="macro", zero_division=0)
    weighted_f1 = f1_score(y_test, pred, average="weighted", zero_division=0)
    macro_precision = precision_score(y_test, pred, average="macro", zero_division=0)
    macro_recall = recall_score(y_test, pred, average="macro", zero_division=0)

    rows.append({
        "model": name,
        "accuracy": accuracy,
        "macro_precision": macro_precision,
        "macro_recall": macro_recall,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "train_seconds": train_seconds,
    })

    confusion_matrices[name] = confusion_matrix(y_test, pred, labels=label_ids)
    warning_log[name] = sorted(set(caught))

results = pd.DataFrame(rows).sort_values("accuracy", ascending=False).reset_index(drop=True)

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
results.to_csv(CSV_OUT, index=False)

lines = []
lines.append("# Classical Model Reproduction Comparison")
lines.append("")
lines.append("This report compares four classical models using the same reconstructed preprocessing pipeline.")
lines.append("")
lines.append("The comparison is based on the public dataset and visible final-model hyperparameters in the public notebook.")
lines.append("")

lines.append("## 1. Shared preprocessing")
lines.append("")
lines.append(f"- Dataset rows: **{len(df)}**")
lines.append(f"- Features: **{len(feature_columns)}**")
lines.append(f"- Train/test split: **80/20**, stratified, random_state={RANDOM_STATE}")
lines.append("- StandardScaler fitted on training data only")
lines.append(f"- SMOTE applied to training data only, random_state={RANDOM_STATE}")
lines.append(f"- Training rows after SMOTE: **{len(X_train_smote)}**")
lines.append(f"- Test rows: **{len(X_test_scaled)}**")
lines.append("")

lines.append("## 2. Reconstructed class encoding")
lines.append("")
lines.append("The public notebook does not publish the original numeric class-ID mapping. A deterministic LabelEncoder mapping is therefore used only as a compatibility convention for this reconstruction:")
lines.append("")
lines.append("| Numeric ID | Sport |")
lines.append("|---:|---|")
for idx, label in enumerate(label_names):
    lines.append(f"| {idx} | {label} |")
lines.append("")
lines.append("This mapping is not presented as the unrecovered original encoding.")
lines.append("")

lines.append("## 3. Model configurations")
lines.append("")
lines.append("- Logistic Regression: C=36.380497, max_iter=11, reconstructed one-vs-rest strategy")
lines.append("- SVM: C=39.689206, gamma=0.551907")
lines.append("- Random Forest: n_estimators=124, max_depth=11, max_features=0.356285, min_samples_split=3, min_samples_leaf=3")
lines.append("- XGBoost: n_estimators=147, max_depth=8, max_features=0.353969")
lines.append("")

lines.append("## 4. Test-set comparison")
lines.append("")
lines.append("| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Train time (s) |")
lines.append("|---|---:|---:|---:|---:|---:|---:|")
for _, row in results.iterrows():
    lines.append(
        f"| {row['model']} | {row['accuracy']:.4f} | {row['macro_precision']:.4f} | "
        f"{row['macro_recall']:.4f} | {row['macro_f1']:.4f} | "
        f"{row['weighted_f1']:.4f} | {row['train_seconds']:.3f} |"
    )
lines.append("")

best_accuracy = results.iloc[0]
best_macro_f1 = results.sort_values("macro_f1", ascending=False).iloc[0]
lines.append("## 5. Observed comparison")
lines.append("")
lines.append(f"- Highest reconstructed test accuracy: **{best_accuracy['model']}**, {best_accuracy['accuracy']:.4f}.")
lines.append(f"- Highest reconstructed Macro F1: **{best_macro_f1['model']}**, {best_macro_f1['macro_f1']:.4f}.")
lines.append("- These are results of the reconstructed public-data pipeline, not claims about the unpublished original preprocessing.")
lines.append("")

lines.append("## 6. Confusion matrices")
lines.append("")
for name in models:
    cm = confusion_matrices[name]
    lines.append(f"### {name}")
    lines.append("")
    lines.append("| Actual / Predicted | " + " | ".join(label_names) + " |")
    lines.append("|---|" + "---:|" * len(label_names))
    for i, actual in enumerate(label_names):
        lines.append("| " + actual + " | " + " | ".join(str(int(v)) for v in cm[i]) + " |")
    lines.append("")

lines.append("## 7. Runtime warnings")
lines.append("")
any_warning = False
for name, msgs in warning_log.items():
    if msgs:
        any_warning = True
        lines.append(f"### {name}")
        lines.append("")
        for msg in msgs:
            lines.append(f"- {msg}")
        lines.append("")
if not any_warning:
    lines.append("- No model emitted a runtime warning in this run.")
    lines.append("")

lines.append("## 8. Reproducibility boundary")
lines.append("")
lines.append("- The original files in original/ were not modified.")
lines.append("- The class-ID encoding is a documented reconstruction convention.")
lines.append("- The public notebook's missing X/y definitions and its 2,427-row stored output remain unresolved.")
lines.append("- XGBoost compatibility warnings, if any, are retained above rather than silently removed.")
lines.append("")

lines.append("## 9. Environment")
lines.append("")
for package in ["pandas", "scikit-learn", "imbalanced-learn", "xgboost"]:
    lines.append(f"- {package}: {version(package)}")

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(results.to_string(index=False))
print(f"Report written to {REPORT}")
print(f"Metrics CSV written to {CSV_OUT}")
