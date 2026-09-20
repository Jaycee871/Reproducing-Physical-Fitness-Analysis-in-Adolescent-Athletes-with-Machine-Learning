from pathlib import Path
from collections import Counter
from importlib.metadata import version
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

DATASET = Path("original/sports datasets.csv")
OUTPUT = Path("notes/preprocessing_reconstruction.md")

TARGET = "sports types"
TEST_SIZE = 0.20
RANDOM_STATE = 42

if not DATASET.exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET}")

df = pd.read_csv(DATASET)

if TARGET not in df.columns:
    raise ValueError(f"Expected target column not found: {TARGET}")

# Reconstruction decision:
# The public notebook's PCA section supplies 15 feature labels, matching the
# 15 non-target columns in the public CSV. The notebook does not define its
# numeric class encoding, so this audit keeps y as the original string labels.
feature_columns = [c for c in df.columns if c != TARGET]
X = df[feature_columns].copy()
y = df[TARGET].copy()

non_numeric = X.select_dtypes(exclude="number").columns.tolist()
if non_numeric:
    raise TypeError(f"Unexpected non-numeric feature columns: {non_numeric}")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    stratify=y,
    random_state=RANDOM_STATE,
)

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

smote = SMOTE(random_state=RANDOM_STATE)
X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

def distribution(series):
    counts = pd.Series(series).value_counts()
    total = int(counts.sum())
    return [
        (str(label), int(count), (int(count) / total * 100 if total else 0.0))
        for label, count in counts.items()
    ]

full_dist = distribution(y)
train_dist = distribution(y_train)
test_dist = distribution(y_test)
smote_dist = distribution(y_train_smote)

lines = []
lines.append("# Preprocessing Reconstruction Audit")
lines.append("")
lines.append("This report reconstructs the visible preprocessing sequence in the public notebook using the preserved public CSV.")
lines.append("")
lines.append("No model is trained in this step, and the original files in original/ are not modified.")
lines.append("")

lines.append("## 1. Reconstruction basis")
lines.append("")
lines.append("- Public dataset: original/sports datasets.csv")
lines.append("- Candidate target: sports types")
lines.append("- Reconstructed X: the 15 numeric columns other than sports types.")
lines.append("- Evidence for the 15-feature reconstruction: the public notebook's PCA section lists 15 physical-fitness feature labels corresponding to the 15 non-target columns in the CSV.")
lines.append("- The public notebook does not define the numeric mapping used for teen_runsoc_target; therefore this audit preserves the original sport names as class labels instead of inventing an encoding.")
lines.append("")

lines.append("## 2. Reconstructed X and y")
lines.append("")
lines.append(f"- X shape before splitting: **{X.shape[0]} x {X.shape[1]}**")
lines.append(f"- y length: **{len(y)}**")
lines.append("")
lines.append("| Feature # | Reconstructed X column |")
lines.append("|---:|---|")
for i, col in enumerate(feature_columns, start=1):
    lines.append(f"| {i} | {col} |")
lines.append("")
lines.append("Full-dataset class distribution:")
lines.append("")
lines.append("| Class | Count | Percentage |")
lines.append("|---|---:|---:|")
for label, count, pct in full_dist:
    lines.append(f"| {label} | {count} | {pct:.2f}% |")
lines.append("")

lines.append("## 3. Train/test split")
lines.append("")
lines.append("The public notebook visibly uses:")
lines.append("")
lines.append(f"- test_size = {TEST_SIZE:.2f}")
lines.append("- stratify = y")
lines.append(f"- random_state = {RANDOM_STATE}")
lines.append("")
lines.append(f"- Reconstructed training rows: **{len(X_train)}**")
lines.append(f"- Reconstructed test rows: **{len(X_test)}**")
lines.append("")
lines.append("Training class distribution:")
lines.append("")
lines.append("| Class | Count | Percentage |")
lines.append("|---|---:|---:|")
for label, count, pct in train_dist:
    lines.append(f"| {label} | {count} | {pct:.2f}% |")
lines.append("")
lines.append("Test class distribution:")
lines.append("")
lines.append("| Class | Count | Percentage |")
lines.append("|---|---:|---:|")
for label, count, pct in test_dist:
    lines.append(f"| {label} | {count} | {pct:.2f}% |")
lines.append("")

lines.append("## 4. Standardization")
lines.append("")
lines.append("The public notebook fits StandardScaler on X_train, then transforms both training and test features.")
lines.append("")
lines.append("- Scaler fitted on training data only: **Yes**")
lines.append(f"- Scaled training shape: **{X_train_scaled.shape[0]} x {X_train_scaled.shape[1]}**")
lines.append(f"- Scaled test shape: **{X_test_scaled.shape[0]} x {X_test_scaled.shape[1]}**")
lines.append("- Test data were not used to fit the scaler.")
lines.append("")

lines.append("## 5. SMOTE reconstruction")
lines.append("")
lines.append(f"The public notebook uses SMOTE(random_state={RANDOM_STATE}) after scaling the training data.")
lines.append("")
lines.append("- SMOTE applied to training data only: **Yes**")
lines.append(f"- Training rows before SMOTE: **{len(X_train_scaled)}**")
lines.append(f"- Training rows after SMOTE: **{len(X_train_smote)}**")
lines.append("")
lines.append("Class distribution after SMOTE:")
lines.append("")
lines.append("| Class | Count | Percentage |")
lines.append("|---|---:|---:|")
for label, count, pct in smote_dist:
    lines.append(f"| {label} | {count} | {pct:.2f}% |")
lines.append("")

lines.append("## 6. Leakage safeguards")
lines.append("")
lines.append("- Split occurs before scaling.")
lines.append("- StandardScaler is fit only on X_train.")
lines.append("- SMOTE is applied only to the scaled training set.")
lines.append("- The test set is neither oversampled nor used to fit the scaler.")
lines.append("")

lines.append("## 7. Unresolved reproducibility gap")
lines.append("")
lines.append("- The public notebook references teen_running_soccer and teen_runsoc_target, but does not define them.")
lines.append("- The notebook does not provide the mapping from sport names to numeric class IDs.")
lines.append("- The stored notebook class counts total 2,427, while the preserved public dataset contains 1,434 rows.")
lines.append("- Because the original numeric target encoding is not recoverable from the public notebook, this audit intentionally does not invent one.")
lines.append("")

lines.append("## 8. Environment")
lines.append("")
for package in ["pandas", "scikit-learn", "imbalanced-learn"]:
    lines.append(f"- {package}: {version(package)}")
lines.append("")

lines.append("## 9. Reproduction decision")
lines.append("")
lines.append("The visible preprocessing order can be reconstructed as:")
lines.append("")
lines.append("public CSV -> X/y separation -> stratified 80/20 split -> StandardScaler fitted on training data -> SMOTE on scaled training data")
lines.append("")
lines.append("This reconstructed pipeline is suitable for the next baseline-model step, provided that any numeric class encoding required by a model is explicitly documented as a reconstruction convention rather than presented as the unrecovered original encoding.")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Report written to {OUTPUT}")
print(f"X: {X.shape}; y: {len(y)}")
print(f"Train: {X_train.shape}; Test: {X_test.shape}")
print(f"SMOTE train shape: {X_train_smote.shape}")
print("SMOTE distribution:", Counter(y_train_smote))
