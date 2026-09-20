from pathlib import Path
import pandas as pd

DATASET = Path("original/sports datasets.csv")
OUTPUT = Path("notes/dataset_inspection.md")

if not DATASET.exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET}")

df = pd.read_csv(DATASET)

lines = []
lines.append("# Dataset Inspection")
lines.append("")
lines.append("This report was generated automatically from the preserved original dataset:")
lines.append("")
lines.append(f"`{DATASET.as_posix()}`")
lines.append("")
lines.append("The original dataset was read only. No cleaning, transformation, imputation, or model training was performed.")
lines.append("")

lines.append("## 1. Dataset shape")
lines.append("")
lines.append(f"- Rows: **{df.shape[0]}**")
lines.append(f"- Columns: **{df.shape[1]}**")
lines.append("")

lines.append("## 2. Column names")
lines.append("")
for i, col in enumerate(df.columns, start=1):
    lines.append(f"{i}. `{col}`")
lines.append("")

lines.append("## 3. Data types")
lines.append("")
lines.append("| Column | pandas dtype |")
lines.append("|---|---|")
for col, dtype in df.dtypes.items():
    lines.append(f"| `{col}` | `{dtype}` |")
lines.append("")

lines.append("## 4. Missing values")
lines.append("")
missing = df.isna().sum()
lines.append(f"- Total missing values: **{int(missing.sum())}**")
lines.append("")
lines.append("| Column | Missing values | Missing rate |")
lines.append("|---|---:|---:|")
for col in df.columns:
    count = int(missing[col])
    rate = (count / len(df) * 100) if len(df) else 0
    lines.append(f"| `{col}` | {count} | {rate:.2f}% |")
lines.append("")

lines.append("## 5. Duplicate rows")
lines.append("")
duplicate_count = int(df.duplicated().sum())
lines.append(f"- Exact duplicate rows: **{duplicate_count}**")
lines.append("")

target = "sports types"
lines.append("## 6. Target / class distribution")
lines.append("")
if target in df.columns:
    counts = df[target].value_counts(dropna=False)
    lines.append(f"Candidate target column identified from the dataset: `{target}`")
    lines.append("")
    lines.append("| Class | Count | Percentage |")
    lines.append("|---|---:|---:|")
    for label, count in counts.items():
        pct = count / len(df) * 100 if len(df) else 0
        lines.append(f"| `{label}` | {int(count)} | {pct:.2f}% |")
else:
    lines.append(f"Expected target column `{target}` was not found.")
lines.append("")

lines.append("## 7. Numeric summary")
lines.append("")
numeric = df.select_dtypes(include="number")
if numeric.empty:
    lines.append("No numeric columns were detected.")
else:
    summary = numeric.describe().T
    lines.append("| Column | Count | Mean | Std | Min | Median | Max |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for col, row in summary.iterrows():
        median = numeric[col].median()
        lines.append(
            f"| `{col}` | {int(row['count'])} | {row['mean']:.3f} | "
            f"{row['std']:.3f} | {row['min']:.3f} | {median:.3f} | {row['max']:.3f} |"
        )
lines.append("")

lines.append("## 8. First five rows")
lines.append("")
preview = df.head(5).copy()
lines.append(preview.to_markdown(index=False))
lines.append("")

lines.append("## 9. Reproducibility note")
lines.append("")
lines.append("- Source dataset: `original/sports datasets.csv`")
lines.append("- The source file was not modified.")
lines.append("- This step performs inspection only.")
lines.append("- Data cleaning and model training remain out of scope for this step.")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Inspection report written to {OUTPUT}")
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Missing values: {int(df.isna().sum().sum())}")
print(f"Duplicate rows: {duplicate_count}")
