# Classical Model Reproduction Comparison

This report compares four classical models using the same reconstructed preprocessing pipeline.

The comparison is based on the public dataset and visible final-model hyperparameters in the public notebook.

## 1. Shared preprocessing

- Dataset rows: **1434**
- Features: **15**
- Train/test split: **80/20**, stratified, random_state=42
- StandardScaler fitted on training data only
- SMOTE applied to training data only, random_state=42
- Training rows after SMOTE: **2145**
- Test rows: **287**

## 2. Reconstructed class encoding

The public notebook does not publish the original numeric class-ID mapping. A deterministic LabelEncoder mapping is therefore used only as a compatibility convention for this reconstruction:

| Numeric ID | Sport |
|---:|---|
| 0 | badminton |
| 1 | baseball |
| 2 | football |
| 3 | swimming |
| 4 | track & field |

This mapping is not presented as the unrecovered original encoding.

## 3. Model configurations

- Logistic Regression: C=36.380497, max_iter=11, reconstructed one-vs-rest strategy
- SVM: C=39.689206, gamma=0.551907
- Random Forest: n_estimators=124, max_depth=11, max_features=0.356285, min_samples_split=3, min_samples_leaf=3
- XGBoost: n_estimators=147, max_depth=8, max_features=0.353969

## 4. Test-set comparison

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Train time (s) |
|---|---:|---:|---:|---:|---:|---:|
| XGBoost | 0.6690 | 0.6221 | 0.6009 | 0.6074 | 0.6668 | 0.328 |
| SVM | 0.6063 | 0.6463 | 0.4501 | 0.4739 | 0.5856 | 0.117 |
| Random Forest | 0.6063 | 0.5469 | 0.5899 | 0.5602 | 0.6109 | 0.207 |
| Logistic Regression | 0.4948 | 0.4728 | 0.5639 | 0.4742 | 0.4844 | 1.098 |

## 5. Observed comparison

- Highest reconstructed test accuracy: **XGBoost**, 0.6690.
- Highest reconstructed Macro F1: **XGBoost**, 0.6074.
- These are results of the reconstructed public-data pipeline, not claims about the unpublished original preprocessing.

## 6. Confusion matrices

### Logistic Regression

| Actual / Predicted | badminton | baseball | football | swimming | track & field |
|---|---:|---:|---:|---:|---:|
| badminton | 7 | 0 | 2 | 0 | 3 |
| baseball | 3 | 45 | 6 | 5 | 7 |
| football | 16 | 24 | 30 | 6 | 32 |
| swimming | 0 | 5 | 1 | 15 | 0 |
| track & field | 5 | 17 | 4 | 9 | 45 |

### SVM

| Actual / Predicted | badminton | baseball | football | swimming | track & field |
|---|---:|---:|---:|---:|---:|
| badminton | 2 | 0 | 7 | 0 | 3 |
| baseball | 1 | 33 | 22 | 0 | 10 |
| football | 0 | 12 | 80 | 0 | 16 |
| swimming | 0 | 4 | 9 | 3 | 5 |
| track & field | 0 | 6 | 17 | 1 | 56 |

### Random Forest

| Actual / Predicted | badminton | baseball | football | swimming | track & field |
|---|---:|---:|---:|---:|---:|
| badminton | 5 | 0 | 5 | 0 | 2 |
| baseball | 2 | 44 | 12 | 1 | 7 |
| football | 12 | 14 | 58 | 5 | 19 |
| swimming | 0 | 3 | 2 | 14 | 2 |
| track & field | 3 | 12 | 8 | 4 | 53 |

### XGBoost

| Actual / Predicted | badminton | baseball | football | swimming | track & field |
|---|---:|---:|---:|---:|---:|
| badminton | 4 | 0 | 5 | 0 | 3 |
| baseball | 1 | 49 | 10 | 0 | 6 |
| football | 3 | 15 | 71 | 3 | 16 |
| swimming | 0 | 4 | 2 | 12 | 3 |
| track & field | 0 | 6 | 12 | 6 | 56 |

## 7. Runtime warnings

### SVM

- The `probability` parameter was deprecated in 1.9 and will be removed in version 1.11. Use `CalibratedClassifierCV(SVC(), ensemble=False)` instead of `SVC(probability=True)`

## 8. Reproducibility boundary

- The original files in original/ were not modified.
- The class-ID encoding is a documented reconstruction convention.
- The public notebook's missing X/y definitions and its 2,427-row stored output remain unresolved.
- XGBoost compatibility warnings, if any, are retained above rather than silently removed.

## 9. Environment

- pandas: 3.0.6
- scikit-learn: 1.9.1
- imbalanced-learn: 0.14.2
- xgboost: 3.2.0
