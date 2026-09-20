# Preprocessing Reconstruction Audit

This report reconstructs the visible preprocessing sequence in the public notebook using the preserved public CSV.

No model is trained in this step, and the original files in original/ are not modified.

## 1. Reconstruction basis

- Public dataset: original/sports datasets.csv
- Candidate target: sports types
- Reconstructed X: the 15 numeric columns other than sports types.
- Evidence for the 15-feature reconstruction: the public notebook's PCA section lists 15 physical-fitness feature labels corresponding to the 15 non-target columns in the CSV.
- The public notebook does not define the numeric mapping used for teen_runsoc_target; therefore this audit preserves the original sport names as class labels instead of inventing an encoding.

## 2. Reconstructed X and y

- X shape before splitting: **1434 x 15**
- y length: **1434**

| Feature # | Reconstructed X column |
|---:|---|
| 1 | body fat(%FAT) |
| 2 | weight(kg) |
| 3 | BMI |
| 4 | grip strength (L) |
| 5 | grip strength (R) |
| 6 | grip strength (avg) |
| 7 | back muscle strength |
| 8 | push up |
| 9 | sit up |
| 10 | standing long jump |
| 11 | sargent jump |
| 12 | side step |
| 13 | backward flexion |
| 14 | sit and reach |
| 15 | eye hand coordination |

Full-dataset class distribution:

| Class | Count | Percentage |
|---|---:|---:|
| football | 537 | 37.45% |
| track & field | 402 | 28.03% |
| baseball | 328 | 22.87% |
| swimming | 105 | 7.32% |
| badminton | 62 | 4.32% |

## 3. Train/test split

The public notebook visibly uses:

- test_size = 0.20
- stratify = y
- random_state = 42

- Reconstructed training rows: **1147**
- Reconstructed test rows: **287**

Training class distribution:

| Class | Count | Percentage |
|---|---:|---:|
| football | 429 | 37.40% |
| track & field | 322 | 28.07% |
| baseball | 262 | 22.84% |
| swimming | 84 | 7.32% |
| badminton | 50 | 4.36% |

Test class distribution:

| Class | Count | Percentage |
|---|---:|---:|
| football | 108 | 37.63% |
| track & field | 80 | 27.87% |
| baseball | 66 | 23.00% |
| swimming | 21 | 7.32% |
| badminton | 12 | 4.18% |

## 4. Standardization

The public notebook fits StandardScaler on X_train, then transforms both training and test features.

- Scaler fitted on training data only: **Yes**
- Scaled training shape: **1147 x 15**
- Scaled test shape: **287 x 15**
- Test data were not used to fit the scaler.

## 5. SMOTE reconstruction

The public notebook uses SMOTE(random_state=42) after scaling the training data.

- SMOTE applied to training data only: **Yes**
- Training rows before SMOTE: **1147**
- Training rows after SMOTE: **2145**

Class distribution after SMOTE:

| Class | Count | Percentage |
|---|---:|---:|
| football | 429 | 20.00% |
| track & field | 429 | 20.00% |
| baseball | 429 | 20.00% |
| badminton | 429 | 20.00% |
| swimming | 429 | 20.00% |

## 6. Leakage safeguards

- Split occurs before scaling.
- StandardScaler is fit only on X_train.
- SMOTE is applied only to the scaled training set.
- The test set is neither oversampled nor used to fit the scaler.

## 7. Unresolved reproducibility gap

- The public notebook references teen_running_soccer and teen_runsoc_target, but does not define them.
- The notebook does not provide the mapping from sport names to numeric class IDs.
- The stored notebook class counts total 2,427, while the preserved public dataset contains 1,434 rows.
- Because the original numeric target encoding is not recoverable from the public notebook, this audit intentionally does not invent one.

## 8. Environment

- pandas: 3.0.6
- scikit-learn: 1.9.1
- imbalanced-learn: 0.14.2

## 9. Reproduction decision

The visible preprocessing order can be reconstructed as:

public CSV -> X/y separation -> stratified 80/20 split -> StandardScaler fitted on training data -> SMOTE on scaled training data

This reconstructed pipeline is suitable for the next baseline-model step, provided that any numeric class encoding required by a model is explicitly documented as a reconstruction convention rather than presented as the unrecovered original encoding.
