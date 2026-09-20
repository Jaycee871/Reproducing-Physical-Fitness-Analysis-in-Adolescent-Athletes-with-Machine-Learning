# Logistic Regression Baseline

This is the first model run in the reproduction workflow.

The model is trained only after the dataset, paper-code-data consistency, and preprocessing reconstruction audits were completed.

## 1. Data pipeline

- Source: original/sports datasets.csv
- Samples: **1434**
- Features: **15**
- Target: sports types
- Train/test split: **80/20**, stratified, random_state=42
- StandardScaler: fitted on training data only
- SMOTE: training data only, random_state=42
- Training rows after SMOTE: **2145**
- Test rows: **287**

## 2. Logistic Regression configuration

The public notebook's final Logistic Regression configuration visibly uses:

- C = **36.380497**
- max_iter = **11**
- multi_class = ovr in the original notebook

Compatibility reconstruction used here:

- OneVsRestClassifier(LogisticRegression(...))
- Solver: lbfgs
- Original sport-name labels are retained because the notebook does not publish the original numeric class mapping.

## 3. Test-set performance

- Accuracy: **0.4948** (49.48%)
- Macro F1: **0.4742**
- Weighted F1: **0.4844**

## 4. Per-class metrics

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| badminton | 0.2258 | 0.5833 | 0.3256 | 12 |
| baseball | 0.4945 | 0.6818 | 0.5732 | 66 |
| football | 0.6977 | 0.2778 | 0.3974 | 108 |
| swimming | 0.4286 | 0.7143 | 0.5357 | 21 |
| track & field | 0.5172 | 0.5625 | 0.5389 | 80 |

## 5. Confusion matrix

| Actual / Predicted | badminton | baseball | football | swimming | track & field |
|---|---:|---:|---:|---:|---:|
| badminton | 7 | 0 | 2 | 0 | 3 |
| baseball | 3 | 45 | 6 | 5 | 7 |
| football | 16 | 24 | 30 | 6 | 32 |
| swimming | 0 | 5 | 1 | 15 | 0 |
| track & field | 5 | 17 | 4 | 9 | 45 |

## 6. Convergence note

- No Logistic Regression convergence warning was observed in this run.

## 7. Reproducibility boundary

- No original file was modified.
- The numeric class-ID mapping from the original notebook remains unrecovered.
- The one-vs-rest strategy is reconstructed explicitly for compatibility with the current scikit-learn API.
- This run should be treated as a documented reproduction baseline, not as proof that the unpublished original preprocessing was identical.

## 8. Environment

- pandas: 3.0.6
- scikit-learn: 1.9.1
- imbalanced-learn: 0.14.2
