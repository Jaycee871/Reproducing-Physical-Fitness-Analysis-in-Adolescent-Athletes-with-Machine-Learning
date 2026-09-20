from pathlib import Path
from importlib.metadata import version
import warnings

import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE

DATASET = Path("original/sports datasets.csv")
OUTPUT = Path("notes/logistic_regression_baseline.md")

TARGET = "sports types"
TEST_SIZE = 0.20
RANDOM_STATE = 42
LR_C = 36.380497
LR_MAX_ITER = 11

if not DATASET.exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET}")

df = pd.read_csv(DATASET)
feature_columns = [c for c in df.columns if c != TARGET]

X = df[feature_columns].copy()
y = df[TARGET].copy()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    stratify=y,
    random_state=RANDOM_STATE,
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

smote = SMOTE(random_state=RANDOM_STATE)
X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

base_lr = LogisticRegression(
    C=LR_C,
    max_iter=LR_MAX_ITER,
    random_state=RANDOM_STATE,
    solver="lbfgs",
)
model = OneVsRestClassifier(base_lr, n_jobs=-1)

caught_warnings = []
with warnings.catch_warnings(record=True) as records:
    warnings.simplefilter("always")
    model.fit(X_train_smote, y_train_smote)
    caught_warnings = [
        str(w.message)
        for w in records
        if issubclass(w.category, ConvergenceWarning)
    ]

y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
macro_f1 = f1_score(y_test, y_pred, average="macro")
weighted_f1 = f1_score(y_test, y_pred, average="weighted")

labels = list(model.classes_)
cm = confusion_matrix(y_test, y_pred, labels=labels)
report = classification_report(
    y_test,
    y_pred,
    labels=labels,
    target_names=labels,
    output_dict=True,
    zero_division=0,
)

lines = []
lines.append("# Logistic Regression Baseline")
lines.append("")
lines.append("This is the first model run in the reproduction workflow.")
lines.append("")
lines.append("The model is trained only after the dataset, paper-code-data consistency, and preprocessing reconstruction audits were completed.")
lines.append("")

lines.append("## 1. Data pipeline")
lines.append("")
lines.append("- Source: original/sports datasets.csv")
lines.append(f"- Samples: **{len(df)}**")
lines.append(f"- Features: **{len(feature_columns)}**")
lines.append(f"- Target: {TARGET}")
lines.append(f"- Train/test split: **80/20**, stratified, random_state={RANDOM_STATE}")
lines.append("- StandardScaler: fitted on training data only")
lines.append(f"- SMOTE: training data only, random_state={RANDOM_STATE}")
lines.append(f"- Training rows after SMOTE: **{len(X_train_smote)}**")
lines.append(f"- Test rows: **{len(X_test_scaled)}**")
lines.append("")

lines.append("## 2. Logistic Regression configuration")
lines.append("")
lines.append("The public notebook's final Logistic Regression configuration visibly uses:")
lines.append("")
lines.append(f"- C = **{LR_C}**")
lines.append(f"- max_iter = **{LR_MAX_ITER}**")
lines.append("- multi_class = ovr in the original notebook")
lines.append("")
lines.append("Compatibility reconstruction used here:")
lines.append("")
lines.append("- OneVsRestClassifier(LogisticRegression(...))")
lines.append("- Solver: lbfgs")
lines.append("- Original sport-name labels are retained because the notebook does not publish the original numeric class mapping.")
lines.append("")

lines.append("## 3. Test-set performance")
lines.append("")
lines.append(f"- Accuracy: **{accuracy:.4f}** ({accuracy*100:.2f}%)")
lines.append(f"- Macro F1: **{macro_f1:.4f}**")
lines.append(f"- Weighted F1: **{weighted_f1:.4f}**")
lines.append("")

lines.append("## 4. Per-class metrics")
lines.append("")
lines.append("| Class | Precision | Recall | F1-score | Support |")
lines.append("|---|---:|---:|---:|---:|")
for label in labels:
    row = report[label]
    lines.append(
        f"| {label} | {row['precision']:.4f} | {row['recall']:.4f} | "
        f"{row['f1-score']:.4f} | {int(row['support'])} |"
    )
lines.append("")

lines.append("## 5. Confusion matrix")
lines.append("")
header = "| Actual / Predicted | " + " | ".join(labels) + " |"
separator = "|---|" + "---:|" * len(labels)
lines.append(header)
lines.append(separator)
for i, label in enumerate(labels):
    lines.append("| " + label + " | " + " | ".join(str(int(v)) for v in cm[i]) + " |")
lines.append("")

lines.append("## 6. Convergence note")
lines.append("")
if caught_warnings:
    lines.append(f"- Convergence warnings observed: **{len(caught_warnings)}**")
    lines.append("- This is retained as a reproduction finding because the public notebook uses max_iter=11.")
    for warning_text in sorted(set(caught_warnings)):
        lines.append(f"- Warning: {warning_text}")
else:
    lines.append("- No Logistic Regression convergence warning was observed in this run.")
lines.append("")

lines.append("## 7. Reproducibility boundary")
lines.append("")
lines.append("- No original file was modified.")
lines.append("- The numeric class-ID mapping from the original notebook remains unrecovered.")
lines.append("- The one-vs-rest strategy is reconstructed explicitly for compatibility with the current scikit-learn API.")
lines.append("- This run should be treated as a documented reproduction baseline, not as proof that the unpublished original preprocessing was identical.")
lines.append("")

lines.append("## 8. Environment")
lines.append("")
for package in ["pandas", "scikit-learn", "imbalanced-learn"]:
    lines.append(f"- {package}: {version(package)}")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Report written to {OUTPUT}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Macro F1: {macro_f1:.4f}")
print(f"Weighted F1: {weighted_f1:.4f}")
print("Labels:", labels)
