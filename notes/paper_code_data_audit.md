# Paper–Code–Data Consistency Audit

This report compares claims in the published paper, the public implementation notebook, and the preserved public dataset.

No original files were modified and no machine-learning model was trained.

## 1. Paper claims

- Published paper: https://doi.org/10.1371/journal.pone.0298870
- Abstract reports **1,489** male adolescent athletes.
- Materials and Methods, Subjects reports **1,434** male adolescents.
- The paper describes five sports: track & field, football, baseball, swimming, and badminton.

## 2. Public dataset

- File: `original/sports datasets.csv`
- Rows: **1,434**
- Columns: **16**

| Sport | Count |
|---|---:|
| football | 537 |
| track & field | 402 |
| baseball | 328 |
| swimming | 105 |
| badminton | 62 |

## 3. Public notebook

- File: `original/implementation.ipynb`
- The notebook references `X = teen_running_soccer` and `y = teen_runsoc_target`.
- Definition of `teen_running_soccer` found in the public notebook: **No**
- Definition of `teen_runsoc_target` found in the public notebook: **No**

Stored output associated with the X/y selection reports:

| Encoded class | Count |
|---:|---:|
| 0 | 938 |
| 1 | 714 |
| 2 | 368 |
| 3 | 228 |
| 4 | 179 |
| **Total** | **2,427** |

The notebook's visible split configuration includes:
- Test size: **0.20**
- Stratification: **y**
- Random state: **42**
- StandardScaler detected: **Yes**
- SMOTE detected: **Yes**
- SMOTE random state: **42**

## 4. Consistency checks

| Check | Source value | Public dataset value | Match? |
|---|---:|---:|---|
| Paper abstract sample size vs public dataset | 1,489 | 1,434 | **No** |
| Paper Methods sample size vs public dataset | 1,434 | 1,434 | **Yes** |
| Stored notebook class-count total vs public dataset | 2,427 | 1,434 | **No** |

## 5. Reproduction findings

- The abstract sample size (**1,489**) does not match the public dataset (**1,434**).
- The Materials and Methods sample size (**1,434**) matches the public dataset exactly.
- The stored notebook class-count output totals **2,427**, which does not match the public dataset (**1,434**).
- The public notebook references `teen_running_soccer` and `teen_runsoc_target` without a definition found elsewhere in the notebook.

These observations are recorded as reproducibility findings. They do not by themselves establish why the discrepancies occurred.

## 6. Next reproducibility decision

Before reproducing model performance, the reproduction should explicitly reconstruct how the public CSV maps to the notebook's X and y variables, class encoding, train/test split, scaling, and SMOTE steps.

The original files in `original/` remain unchanged.
