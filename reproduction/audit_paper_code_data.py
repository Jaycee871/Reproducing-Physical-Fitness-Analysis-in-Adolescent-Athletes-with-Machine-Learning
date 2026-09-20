from pathlib import Path
import json
import re
import pandas as pd

DATASET = Path("original/sports datasets.csv")
NOTEBOOK = Path("original/implementation.ipynb")
OUTPUT = Path("notes/paper_code_data_audit.md")

PAPER_URL = "https://doi.org/10.1371/journal.pone.0298870"
PAPER_ABSTRACT_N = 1489
PAPER_METHODS_N = 1434

if not DATASET.exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET}")
if not NOTEBOOK.exists():
    raise FileNotFoundError(f"Notebook not found: {NOTEBOOK}")

df = pd.read_csv(DATASET)
nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

dataset_n = len(df)
dataset_classes = {}
if "sports types" in df.columns:
    dataset_classes = df["sports types"].value_counts().to_dict()

code_cells = [
    "".join(cell.get("source", []))
    for cell in nb.get("cells", [])
    if cell.get("cell_type") == "code"
]
all_code = "\n".join(code_cells)

def has_assignment(var_name: str) -> bool:
    pattern = rf"(?m)^\s*{re.escape(var_name)}\s*="
    return re.search(pattern, all_code) is not None

x_alias = "teen_running_soccer"
y_alias = "teen_runsoc_target"

x_alias_defined = has_assignment(x_alias)
y_alias_defined = has_assignment(y_alias)

xy_reference_cell = None
notebook_class_counts = []
for cell in nb.get("cells", []):
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))
    if f"X = {x_alias}" in src and f"y = {y_alias}" in src:
        xy_reference_cell = src
        for output in cell.get("outputs", []):
            text = "".join(output.get("text", []))
            for label, count in re.findall(r"(?m)^\s*(\d+)\s+(\d+)\s*$", text):
                notebook_class_counts.append((int(label), int(count)))
        break

notebook_output_total = sum(count for _, count in notebook_class_counts) if notebook_class_counts else None

split_match = re.search(
    r"train_test_split\([^\n]*test_size\s*=\s*([0-9.]+)[^\n]*stratify\s*=\s*([^,\)]+)[^\n]*random_state\s*=\s*(\d+)",
    all_code,
)
split_summary = None
if split_match:
    split_summary = {
        "test_size": split_match.group(1),
        "stratify": split_match.group(2).strip(),
        "random_state": split_match.group(3),
    }

uses_scaler = "StandardScaler()" in all_code
smote_match = re.search(r"SMOTE\(random_state\s*=\s*(\d+)\)", all_code)
uses_smote = smote_match is not None
smote_random_state = smote_match.group(1) if smote_match else None

checks = [
    ("Paper abstract sample size vs public dataset", PAPER_ABSTRACT_N, dataset_n),
    ("Paper Methods sample size vs public dataset", PAPER_METHODS_N, dataset_n),
]
if notebook_output_total is not None:
    checks.append(("Stored notebook class-count total vs public dataset", notebook_output_total, dataset_n))

lines = []
lines.append("# Paper–Code–Data Consistency Audit")
lines.append("")
lines.append("This report compares claims in the published paper, the public implementation notebook, and the preserved public dataset.")
lines.append("")
lines.append("No original files were modified and no machine-learning model was trained.")
lines.append("")

lines.append("## 1. Paper claims")
lines.append("")
lines.append(f"- Published paper: {PAPER_URL}")
lines.append(f"- Abstract reports **{PAPER_ABSTRACT_N:,}** male adolescent athletes.")
lines.append(f"- Materials and Methods, Subjects reports **{PAPER_METHODS_N:,}** male adolescents.")
lines.append("- The paper describes five sports: track & field, football, baseball, swimming, and badminton.")
lines.append("")

lines.append("## 2. Public dataset")
lines.append("")
lines.append(f"- File: `{DATASET.as_posix()}`")
lines.append(f"- Rows: **{dataset_n:,}**")
lines.append(f"- Columns: **{df.shape[1]}**")
if dataset_classes:
    lines.append("")
    lines.append("| Sport | Count |")
    lines.append("|---|---:|")
    for sport, count in dataset_classes.items():
        lines.append(f"| {sport} | {int(count)} |")
lines.append("")

lines.append("## 3. Public notebook")
lines.append("")
lines.append(f"- File: `{NOTEBOOK.as_posix()}`")
lines.append(f"- The notebook references `X = {x_alias}` and `y = {y_alias}`.")
lines.append(f"- Definition of `{x_alias}` found in the public notebook: **{'Yes' if x_alias_defined else 'No'}**")
lines.append(f"- Definition of `{y_alias}` found in the public notebook: **{'Yes' if y_alias_defined else 'No'}**")
if notebook_class_counts:
    lines.append("")
    lines.append("Stored output associated with the X/y selection reports:")
    lines.append("")
    lines.append("| Encoded class | Count |")
    lines.append("|---:|---:|")
    for label, count in notebook_class_counts:
        lines.append(f"| {label} | {count} |")
    lines.append(f"| **Total** | **{notebook_output_total:,}** |")
if split_summary:
    lines.append("")
    lines.append("The notebook's visible split configuration includes:")
    lines.append(f"- Test size: **{split_summary['test_size']}**")
    lines.append(f"- Stratification: **{split_summary['stratify']}**")
    lines.append(f"- Random state: **{split_summary['random_state']}**")
lines.append(f"- StandardScaler detected: **{'Yes' if uses_scaler else 'No'}**")
lines.append(f"- SMOTE detected: **{'Yes' if uses_smote else 'No'}**")
if uses_smote:
    lines.append(f"- SMOTE random state: **{smote_random_state}**")
lines.append("")

lines.append("## 4. Consistency checks")
lines.append("")
lines.append("| Check | Source value | Public dataset value | Match? |")
lines.append("|---|---:|---:|---|")
for label, source_value, data_value in checks:
    match = "Yes" if source_value == data_value else "No"
    lines.append(f"| {label} | {source_value:,} | {data_value:,} | **{match}** |")
lines.append("")

lines.append("## 5. Reproduction findings")
lines.append("")
if PAPER_ABSTRACT_N != dataset_n:
    lines.append(f"- The abstract sample size (**{PAPER_ABSTRACT_N:,}**) does not match the public dataset (**{dataset_n:,}**).")
if PAPER_METHODS_N == dataset_n:
    lines.append(f"- The Materials and Methods sample size (**{PAPER_METHODS_N:,}**) matches the public dataset exactly.")
if notebook_output_total is not None and notebook_output_total != dataset_n:
    lines.append(f"- The stored notebook class-count output totals **{notebook_output_total:,}**, which does not match the public dataset (**{dataset_n:,}**).")
if not x_alias_defined or not y_alias_defined:
    missing = []
    if not x_alias_defined:
        missing.append(f"`{x_alias}`")
    if not y_alias_defined:
        missing.append(f"`{y_alias}`")
    lines.append("- The public notebook references " + " and ".join(missing) + " without a definition found elsewhere in the notebook.")
lines.append("")
lines.append("These observations are recorded as reproducibility findings. They do not by themselves establish why the discrepancies occurred.")
lines.append("")

lines.append("## 6. Next reproducibility decision")
lines.append("")
lines.append("Before reproducing model performance, the reproduction should explicitly reconstruct how the public CSV maps to the notebook's X and y variables, class encoding, train/test split, scaling, and SMOTE steps.")
lines.append("")
lines.append("The original files in `original/` remain unchanged.")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Audit written to {OUTPUT}")
print(f"Paper abstract N: {PAPER_ABSTRACT_N}")
print(f"Paper methods N: {PAPER_METHODS_N}")
print(f"Public dataset N: {dataset_n}")
print(f"Notebook stored-output total: {notebook_output_total}")
print(f"{x_alias} defined: {x_alias_defined}")
print(f"{y_alias} defined: {y_alias_defined}")
