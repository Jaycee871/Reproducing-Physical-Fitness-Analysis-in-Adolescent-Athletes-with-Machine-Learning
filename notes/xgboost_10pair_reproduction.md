# 10-Pair Binary XGBoost Reproduction

This report reconstructs the paper's ten pairwise binary XGBoost tasks using the preserved public dataset.

Two reconstruction protocols are run side by side because the paper text and public notebook describe different scaling procedures.

## 1. Published protocol being reproduced

- Five sports produce 10 unique two-sport combinations.
- The paper describes an 80/20 train/test split with class ratios maintained.
- The paper describes feature scaling to the range -1 to 1.
- The paper describes SMOTE balancing of the minority class to the majority class at 1:1.
- The paper reports XGBoost pairwise Accuracy, AUROC, and F1-score.

## 2. Important scope boundary

The paper states that hyperparameters were optimized by random search over 1,000 epochs. The public notebook does not provide a complete recoverable set of optimized XGBoost parameters for all ten pairs.

For this time-bounded reproduction, all ten pairs use the final XGBoost configuration visibly present in the public notebook:

- n_estimators = 147
- max_depth = 8
- max_features = 0.353969
- random_state = 42

The notebook max_features argument is preserved as written and is not silently reinterpreted as colsample_bytree.
Therefore this is a fixed-public-configuration pairwise reproduction, not a full reproduction of the unpublished 1,000-epoch search history.

## 3. Split-count audit

| Sport | Public dataset total | Reconstructed train | Reconstructed test | Paper-reported train | Paper-reported test | Match? |
|---|---:|---:|---:|---:|---:|---|
| track & field | 402 | 322 | 80 | 322 | 80 | Yes |
| football | 537 | 429 | 108 | 429 | 108 | Yes |
| baseball | 328 | 262 | 66 | 262 | 60 | No |
| swimming | 105 | 84 | 21 | 84 | 21 | Yes |
| badminton | 62 | 50 | 12 | 50 | 12 | Yes |

This audit preserves any count discrepancy instead of adjusting the public dataset to force agreement.

## 4. Reconstruction protocols

### A. Paper-description reconstruction

public CSV -> one five-class stratified 80/20 split -> select each sport pair -> MinMaxScaler(-1, 1) fit on pair training data -> SMOTE on pair training data -> fixed XGBoost configuration

### B. Public-notebook reconstruction

public CSV -> select each sport pair -> pair-specific stratified 80/20 split -> StandardScaler fit on pair training data -> SMOTE on pair training data -> fixed XGBoost configuration

For both protocols, the second sport named in each pair is encoded as class 1 only so that AUROC/F1 can be computed consistently. This is a reconstruction convention, not a claim about the original class-ID mapping.

## 5. Ten-pair accuracy comparison

| Pair | Paper reported | Paper-description | Gap (pp) | Public-notebook | Gap (pp) |
|---|---:|---:|---:|---:|---:|
| track & field vs football | 86.70% | 81.91% | -4.79 | 83.51% | -3.19 |
| track & field vs baseball | 89.04% | 85.62% | -3.42 | 89.73% | +0.69 |
| track & field vs swimming | 92.16% | 84.16% | -8.00 | 87.25% | -4.91 |
| track & field vs badminton | 93.55% | 94.57% | +1.02 | 95.70% | +2.15 |
| football vs baseball | 87.28% | 79.89% | -7.39 | 84.97% | -2.31 |
| football vs swimming | 91.47% | 91.47% | +0.00 | 93.02% | +1.55 |
| football vs badminton | 90.00% | 91.67% | +1.67 | 87.50% | -2.50 |
| baseball vs swimming | 91.95% | 89.66% | -2.29 | 91.95% | +0.00 |
| baseball vs badminton | 91.03% | 88.46% | -2.57 | 87.18% | -3.85 |
| swimming vs badminton | 88.28% | 84.85% | -3.43 | 91.18% | +2.90 |

- Published mean accuracy across 10 pairs: **90.15%**
- Paper-description reconstruction mean accuracy: **87.22%**
- Public-notebook reconstruction mean accuracy: **89.20%**
- Mean absolute accuracy gap, paper-description protocol: **3.46 percentage points**
- Mean absolute accuracy gap, public-notebook protocol: **2.40 percentage points**

## 6. Reconstructed AUROC and F1

The values below use the second sport in each pair as the positive class. Because the original numeric class encoding is not public, these values should not be treated as a label-identical replication of the published AUROC/F1.

| Pair | Paper AUROC | Paper-desc AUROC | Notebook AUROC | Paper F1 | Paper-desc F1 | Notebook F1 |
|---|---:|---:|---:|---:|---:|---:|
| track & field vs football | 0.84 | 0.885 | 0.917 | 0.86 | 0.844 | 0.858 |
| track & field vs baseball | 0.93 | 0.939 | 0.963 | 0.89 | 0.844 | 0.884 |
| track & field vs swimming | 0.89 | 0.888 | 0.936 | 0.87 | 0.636 | 0.711 |
| track & field vs badminton | 0.79 | 0.897 | 0.888 | 0.86 | 0.783 | 0.818 |
| football vs baseball | 0.88 | 0.881 | 0.924 | 0.87 | 0.745 | 0.800 |
| football vs swimming | 0.92 | 0.937 | 0.951 | 0.86 | 0.718 | 0.809 |
| football vs badminton | 0.73 | 0.804 | 0.779 | 0.76 | 0.500 | 0.444 |
| baseball vs swimming | 0.94 | 0.922 | 0.986 | 0.98 | 0.757 | 0.829 |
| baseball vs badminton | 0.91 | 0.967 | 0.956 | 0.82 | 0.690 | 0.643 |
| swimming vs badminton | 0.74 | 0.944 | 0.905 | 0.80 | 0.815 | 0.889 |

## 7. Confusion matrices

### track & field vs football — Paper-description

| Actual / Predicted | track & field | football |
|---|---:|---:|
| track & field | 62 | 18 |
| football | 16 | 92 |

### track & field vs football — Public-notebook

| Actual / Predicted | track & field | football |
|---|---:|---:|
| track & field | 63 | 17 |
| football | 14 | 94 |

### track & field vs baseball — Paper-description

| Actual / Predicted | track & field | baseball |
|---|---:|---:|
| track & field | 68 | 12 |
| baseball | 9 | 57 |

### track & field vs baseball — Public-notebook

| Actual / Predicted | track & field | baseball |
|---|---:|---:|
| track & field | 74 | 6 |
| baseball | 9 | 57 |

### track & field vs swimming — Paper-description

| Actual / Predicted | track & field | swimming |
|---|---:|---:|
| track & field | 71 | 9 |
| swimming | 7 | 14 |

### track & field vs swimming — Public-notebook

| Actual / Predicted | track & field | swimming |
|---|---:|---:|
| track & field | 73 | 8 |
| swimming | 5 | 16 |

### track & field vs badminton — Paper-description

| Actual / Predicted | track & field | badminton |
|---|---:|---:|
| track & field | 78 | 2 |
| badminton | 3 | 9 |

### track & field vs badminton — Public-notebook

| Actual / Predicted | track & field | badminton |
|---|---:|---:|
| track & field | 80 | 1 |
| badminton | 3 | 9 |

### football vs baseball — Paper-description

| Actual / Predicted | football | baseball |
|---|---:|---:|
| football | 88 | 20 |
| baseball | 15 | 51 |

### football vs baseball — Public-notebook

| Actual / Predicted | football | baseball |
|---|---:|---:|
| football | 95 | 12 |
| baseball | 14 | 52 |

### football vs swimming — Paper-description

| Actual / Predicted | football | swimming |
|---|---:|---:|
| football | 104 | 4 |
| swimming | 7 | 14 |

### football vs swimming — Public-notebook

| Actual / Predicted | football | swimming |
|---|---:|---:|
| football | 101 | 7 |
| swimming | 2 | 19 |

### football vs badminton — Paper-description

| Actual / Predicted | football | badminton |
|---|---:|---:|
| football | 105 | 3 |
| badminton | 7 | 5 |

### football vs badminton — Public-notebook

| Actual / Predicted | football | badminton |
|---|---:|---:|
| football | 99 | 9 |
| badminton | 6 | 6 |

### baseball vs swimming — Paper-description

| Actual / Predicted | baseball | swimming |
|---|---:|---:|
| baseball | 64 | 2 |
| swimming | 7 | 14 |

### baseball vs swimming — Public-notebook

| Actual / Predicted | baseball | swimming |
|---|---:|---:|
| baseball | 63 | 3 |
| swimming | 4 | 17 |

### baseball vs badminton — Paper-description

| Actual / Predicted | baseball | badminton |
|---|---:|---:|
| baseball | 59 | 7 |
| badminton | 2 | 10 |

### baseball vs badminton — Public-notebook

| Actual / Predicted | baseball | badminton |
|---|---:|---:|
| baseball | 59 | 7 |
| badminton | 3 | 9 |

### swimming vs badminton — Paper-description

| Actual / Predicted | swimming | badminton |
|---|---:|---:|
| swimming | 17 | 4 |
| badminton | 1 | 11 |

### swimming vs badminton — Public-notebook

| Actual / Predicted | swimming | badminton |
|---|---:|---:|
| swimming | 19 | 2 |
| badminton | 1 | 12 |

## 8. Reproducibility findings to retain

- The paper reports 1,434 subjects in Methods, while its abstract reports 1,489.
- The public CSV contains 1,434 rows.
- The paper's stated per-class split counts do not fully match the public CSV reconstruction; baseball is the visible discrepancy.
- The public notebook uses StandardScaler, whereas the paper describes scaling to -1 to 1.
- The public notebook does not define the original pairwise X/y construction or numeric target encoding.
- The public notebook's stored five-class counts total 2,427, which does not match the public CSV.
- The paper's complete 1,000-epoch pair-specific hyperparameter search cannot be exactly reconstructed from the public notebook alone.

## 9. Environment

- pandas: 3.0.6
- scikit-learn: 1.9.1
- imbalanced-learn: 0.14.2
- xgboost: 3.2.0
