from pathlib import Path
from importlib.metadata import version
import time

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

DATASET = Path("original/sports datasets.csv")
REPORT = Path("notes/xgboost_10pair_reproduction.md")
CSV_OUT = Path("reproduction/results/xgboost_10pair_results.csv")

TARGET = "sports types"
TEST_SIZE = 0.20
RANDOM_STATE = 42

XGB_PARAMS = dict(
    n_estimators=147,
    max_depth=8,
    max_features=0.353969,
    n_jobs=-1,
    random_state=RANDOM_STATE,
    eval_metric="logloss",
    verbosity=0,
)

PAIRS = [
    ("track & field", "football", 86.70, 0.84, 0.86),
    ("track & field", "baseball", 89.04, 0.93, 0.89),
    ("track & field", "swimming", 92.16, 0.89, 0.87),
    ("track & field", "badminton", 93.55, 0.79, 0.86),
    ("football", "baseball", 87.28, 0.88, 0.87),
    ("football", "swimming", 91.47, 0.92, 0.86),
    ("football", "badminton", 90.00, 0.73, 0.76),
    ("baseball", "swimming", 91.95, 0.94, 0.98),
    ("baseball", "badminton", 91.03, 0.91, 0.82),
    ("swimming", "badminton", 88.28, 0.74, 0.80),
]

PAPER_REPORTED_SPLIT = {
    "track & field": (322, 80),
    "football": (429, 108),
    "baseball": (262, 60),
    "swimming": (84, 21),
    "badminton": (50, 12),
}

if not DATASET.exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET}")

df = pd.read_csv(DATASET)
feature_columns = [c for c in df.columns if c != TARGET]
X_all = df[feature_columns].copy()
y_all = df[TARGET].copy()

X_global_train, X_global_test, y_global_train, y_global_test = train_test_split(
    X_all,
    y_all,
    test_size=TEST_SIZE,
    stratify=y_all,
    random_state=RANDOM_STATE,
)

def binary_encode(labels, negative_class, positive_class):
    mapping = {negative_class: 0, positive_class: 1}
    return labels.map(mapping).astype(int)

def evaluate_pair(train_X, test_X, train_y_text, test_y_text, sport_a, sport_b, scaler):
    y_train = binary_encode(train_y_text, sport_a, sport_b)
    y_test = binary_encode(test_y_text, sport_a, sport_b)

    X_train_scaled = scaler.fit_transform(train_X)
    X_test_scaled = scaler.transform(test_X)

    smote = SMOTE(random_state=RANDOM_STATE)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

    model = XGBClassifier(**XGB_PARAMS)

    start = time.perf_counter()
    model.fit(X_train_smote, y_train_smote)
    train_seconds = time.perf_counter() - start

    pred = model.predict(X_test_scaled)
    prob = model.predict_proba(X_test_scaled)[:, 1]

    acc = accuracy_score(y_test, pred)
    f1 = f1_score(y_test, pred, pos_label=1, zero_division=0)
    auc = roc_auc_score(y_test, prob)
    cm = confusion_matrix(y_test, pred, labels=[0, 1])

    return {
        "accuracy": acc,
        "f1_second_sport_positive": f1,
        "auroc_second_sport_positive": auc,
        "train_rows_before_smote": len(train_X),
        "train_rows_after_smote": len(X_train_smote),
        "test_rows": len(test_X),
        "train_seconds": train_seconds,
        "cm": cm,
    }

rows = []
cms = {}

for sport_a, sport_b, paper_acc_pct, paper_auc, paper_f1 in PAIRS:
    pair_name = f"{sport_a} vs {sport_b}"

    train_mask = y_global_train.isin([sport_a, sport_b])
    test_mask = y_global_test.isin([sport_a, sport_b])

    paper_result = evaluate_pair(
        X_global_train.loc[train_mask],
        X_global_test.loc[test_mask],
        y_global_train.loc[train_mask],
        y_global_test.loc[test_mask],
        sport_a,
        sport_b,
        MinMaxScaler(feature_range=(-1, 1)),
    )

    pair_df = df[df[TARGET].isin([sport_a, sport_b])].copy()
    pair_X = pair_df[feature_columns]
    pair_y = pair_df[TARGET]

    nb_X_train, nb_X_test, nb_y_train, nb_y_test = train_test_split(
        pair_X,
        pair_y,
        test_size=TEST_SIZE,
        stratify=pair_y,
        random_state=RANDOM_STATE,
    )

    notebook_result = evaluate_pair(
        nb_X_train,
        nb_X_test,
        nb_y_train,
        nb_y_test,
        sport_a,
        sport_b,
        StandardScaler(),
    )

    rows.append({
        "pair": pair_name,
        "sport_a": sport_a,
        "sport_b": sport_b,
        "paper_reported_accuracy_pct": paper_acc_pct,
        "paper_reported_auroc": paper_auc,
        "paper_reported_f1": paper_f1,
        "paper_protocol_accuracy_pct": paper_result["accuracy"] * 100,
        "paper_protocol_auroc": paper_result["auroc_second_sport_positive"],
        "paper_protocol_f1": paper_result["f1_second_sport_positive"],
        "paper_protocol_gap_pp": paper_result["accuracy"] * 100 - paper_acc_pct,
        "paper_protocol_train_rows": paper_result["train_rows_before_smote"],
        "paper_protocol_train_rows_after_smote": paper_result["train_rows_after_smote"],
        "paper_protocol_test_rows": paper_result["test_rows"],
        "notebook_protocol_accuracy_pct": notebook_result["accuracy"] * 100,
        "notebook_protocol_auroc": notebook_result["auroc_second_sport_positive"],
        "notebook_protocol_f1": notebook_result["f1_second_sport_positive"],
        "notebook_protocol_gap_pp": notebook_result["accuracy"] * 100 - paper_acc_pct,
        "notebook_protocol_train_rows": notebook_result["train_rows_before_smote"],
        "notebook_protocol_train_rows_after_smote": notebook_result["train_rows_after_smote"],
        "notebook_protocol_test_rows": notebook_result["test_rows"],
    })

    cms[(pair_name, "Paper-description")] = paper_result["cm"]
    cms[(pair_name, "Public-notebook")] = notebook_result["cm"]

results = pd.DataFrame(rows)

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
results.to_csv(CSV_OUT, index=False)

paper_mean = results["paper_reported_accuracy_pct"].mean()
paper_protocol_mean = results["paper_protocol_accuracy_pct"].mean()
notebook_protocol_mean = results["notebook_protocol_accuracy_pct"].mean()
paper_protocol_mae = results["paper_protocol_gap_pp"].abs().mean()
notebook_protocol_mae = results["notebook_protocol_gap_pp"].abs().mean()

actual_split_counts = {}
for sport in y_all.value_counts().index:
    actual_split_counts[sport] = (
        int((y_global_train == sport).sum()),
        int((y_global_test == sport).sum()),
    )

lines = []
lines.append("# 10-Pair Binary XGBoost Reproduction")
lines.append("")
lines.append("This report reconstructs the paper's ten pairwise binary XGBoost tasks using the preserved public dataset.")
lines.append("")
lines.append("Two reconstruction protocols are run side by side because the paper text and public notebook describe different scaling procedures.")
lines.append("")

lines.append("## 1. Published protocol being reproduced")
lines.append("")
lines.append("- Five sports produce 10 unique two-sport combinations.")
lines.append("- The paper describes an 80/20 train/test split with class ratios maintained.")
lines.append("- The paper describes feature scaling to the range -1 to 1.")
lines.append("- The paper describes SMOTE balancing of the minority class to the majority class at 1:1.")
lines.append("- The paper reports XGBoost pairwise Accuracy, AUROC, and F1-score.")
lines.append("")

lines.append("## 2. Important scope boundary")
lines.append("")
lines.append("The paper states that hyperparameters were optimized by random search over 1,000 epochs. The public notebook does not provide a complete recoverable set of optimized XGBoost parameters for all ten pairs.")
lines.append("")
lines.append("For this time-bounded reproduction, all ten pairs use the final XGBoost configuration visibly present in the public notebook:")
lines.append("")
lines.append("- n_estimators = 147")
lines.append("- max_depth = 8")
lines.append("- max_features = 0.353969")
lines.append(f"- random_state = {RANDOM_STATE}")
lines.append("")
lines.append("The notebook max_features argument is preserved as written and is not silently reinterpreted as colsample_bytree.")
lines.append("Therefore this is a fixed-public-configuration pairwise reproduction, not a full reproduction of the unpublished 1,000-epoch search history.")
lines.append("")

lines.append("## 3. Split-count audit")
lines.append("")
lines.append("| Sport | Public dataset total | Reconstructed train | Reconstructed test | Paper-reported train | Paper-reported test | Match? |")
lines.append("|---|---:|---:|---:|---:|---:|---|")
for sport in ["track & field", "football", "baseball", "swimming", "badminton"]:
    total = int((y_all == sport).sum())
    train_n, test_n = actual_split_counts[sport]
    paper_train, paper_test = PAPER_REPORTED_SPLIT[sport]
    match = "Yes" if (train_n, test_n) == (paper_train, paper_test) else "No"
    lines.append(f"| {sport} | {total} | {train_n} | {test_n} | {paper_train} | {paper_test} | {match} |")
lines.append("")
lines.append("This audit preserves any count discrepancy instead of adjusting the public dataset to force agreement.")
lines.append("")

lines.append("## 4. Reconstruction protocols")
lines.append("")
lines.append("### A. Paper-description reconstruction")
lines.append("")
lines.append("public CSV -> one five-class stratified 80/20 split -> select each sport pair -> MinMaxScaler(-1, 1) fit on pair training data -> SMOTE on pair training data -> fixed XGBoost configuration")
lines.append("")
lines.append("### B. Public-notebook reconstruction")
lines.append("")
lines.append("public CSV -> select each sport pair -> pair-specific stratified 80/20 split -> StandardScaler fit on pair training data -> SMOTE on pair training data -> fixed XGBoost configuration")
lines.append("")
lines.append("For both protocols, the second sport named in each pair is encoded as class 1 only so that AUROC/F1 can be computed consistently. This is a reconstruction convention, not a claim about the original class-ID mapping.")
lines.append("")

lines.append("## 5. Ten-pair accuracy comparison")
lines.append("")
lines.append("| Pair | Paper reported | Paper-description | Gap (pp) | Public-notebook | Gap (pp) |")
lines.append("|---|---:|---:|---:|---:|---:|")
for _, row in results.iterrows():
    lines.append(
        f"| {row['pair']} | {row['paper_reported_accuracy_pct']:.2f}% | "
        f"{row['paper_protocol_accuracy_pct']:.2f}% | {row['paper_protocol_gap_pp']:+.2f} | "
        f"{row['notebook_protocol_accuracy_pct']:.2f}% | {row['notebook_protocol_gap_pp']:+.2f} |"
    )
lines.append("")
lines.append(f"- Published mean accuracy across 10 pairs: **{paper_mean:.2f}%**")
lines.append(f"- Paper-description reconstruction mean accuracy: **{paper_protocol_mean:.2f}%**")
lines.append(f"- Public-notebook reconstruction mean accuracy: **{notebook_protocol_mean:.2f}%**")
lines.append(f"- Mean absolute accuracy gap, paper-description protocol: **{paper_protocol_mae:.2f} percentage points**")
lines.append(f"- Mean absolute accuracy gap, public-notebook protocol: **{notebook_protocol_mae:.2f} percentage points**")
lines.append("")

lines.append("## 6. Reconstructed AUROC and F1")
lines.append("")
lines.append("The values below use the second sport in each pair as the positive class. Because the original numeric class encoding is not public, these values should not be treated as a label-identical replication of the published AUROC/F1.")
lines.append("")
lines.append("| Pair | Paper AUROC | Paper-desc AUROC | Notebook AUROC | Paper F1 | Paper-desc F1 | Notebook F1 |")
lines.append("|---|---:|---:|---:|---:|---:|---:|")
for _, row in results.iterrows():
    lines.append(
        f"| {row['pair']} | {row['paper_reported_auroc']:.2f} | "
        f"{row['paper_protocol_auroc']:.3f} | {row['notebook_protocol_auroc']:.3f} | "
        f"{row['paper_reported_f1']:.2f} | {row['paper_protocol_f1']:.3f} | "
        f"{row['notebook_protocol_f1']:.3f} |"
    )
lines.append("")

lines.append("## 7. Confusion matrices")
lines.append("")
for sport_a, sport_b, *_ in PAIRS:
    pair_name = f"{sport_a} vs {sport_b}"
    for protocol in ["Paper-description", "Public-notebook"]:
        cm = cms[(pair_name, protocol)]
        lines.append(f"### {pair_name} — {protocol}")
        lines.append("")
        lines.append(f"| Actual / Predicted | {sport_a} | {sport_b} |")
        lines.append("|---|---:|---:|")
        lines.append(f"| {sport_a} | {int(cm[0,0])} | {int(cm[0,1])} |")
        lines.append(f"| {sport_b} | {int(cm[1,0])} | {int(cm[1,1])} |")
        lines.append("")

lines.append("## 8. Reproducibility findings to retain")
lines.append("")
lines.append("- The paper reports 1,434 subjects in Methods, while its abstract reports 1,489.")
lines.append("- The public CSV contains 1,434 rows.")
lines.append("- The paper's stated per-class split counts do not fully match the public CSV reconstruction; baseball is the visible discrepancy.")
lines.append("- The public notebook uses StandardScaler, whereas the paper describes scaling to -1 to 1.")
lines.append("- The public notebook does not define the original pairwise X/y construction or numeric target encoding.")
lines.append("- The public notebook's stored five-class counts total 2,427, which does not match the public CSV.")
lines.append("- The paper's complete 1,000-epoch pair-specific hyperparameter search cannot be exactly reconstructed from the public notebook alone.")
lines.append("")

lines.append("## 9. Environment")
lines.append("")
for package in ["pandas", "scikit-learn", "imbalanced-learn", "xgboost"]:
    lines.append(f"- {package}: {version(package)}")

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(results[[
    "pair",
    "paper_reported_accuracy_pct",
    "paper_protocol_accuracy_pct",
    "notebook_protocol_accuracy_pct",
]].to_string(index=False))
print()
print(f"Published mean accuracy: {paper_mean:.2f}%")
print(f"Paper-description reconstruction mean: {paper_protocol_mean:.2f}%")
print(f"Public-notebook reconstruction mean: {notebook_protocol_mean:.2f}%")
print(f"Report written to {REPORT}")
print(f"CSV written to {CSV_OUT}")
