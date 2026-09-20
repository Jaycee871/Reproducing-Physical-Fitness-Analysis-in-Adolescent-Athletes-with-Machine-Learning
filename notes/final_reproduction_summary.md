# Final Reproduction Summary

## 1. 研究目標

本專案重現 Lee et al. (2024) 發表於 *PLOS ONE* 的研究：

**Essential elements of physical fitness analysis in male adolescent athletes using machine learning**

本次重現的核心目的，是確認公開論文、公開程式碼與公開資料是否足以重新建立原研究的主要機器學習流程與 XGBoost 成果。

---

## 2. 已完成的重現工作

本專案已完成以下步驟：

1. 保存原作者公開的 implementation notebook 與 dataset
2. 建立 SHA-256 checksum，保留原始材料完整性
3. Dataset inspection
4. Paper–Code–Data consistency audit
5. Preprocessing reconstruction
6. Logistic Regression baseline
7. Logistic Regression、SVM、Random Forest、XGBoost 四模型比較
8. 原論文 10 組 pairwise binary XGBoost 重現
9. 比較 paper-description 與 public-notebook 兩種 preprocessing protocol

所有主要步驟皆透過 GitHub Actions 執行，並自動留下執行紀錄與結果檔案。

---

## 3. 公開資料檢查結果

公開 dataset：

- 樣本數：**1,434**
- 欄位數：**16**
- 特徵數：**15**
- Target：**sports types**
- Missing values：**0**
- Exact duplicate rows：**0**

五種運動分布：

| Sport | Count |
|---|---:|
| football | 537 |
| track & field | 402 |
| baseball | 328 |
| swimming | 105 |
| badminton | 62 |

---

## 4. Paper–Code–Data Audit 主要發現

本次重現發現公開材料之間存在數個重要差異：

- 論文摘要報告 **1,489** 名運動員
- Materials and Methods 報告 **1,434** 名
- 公開 CSV 實際為 **1,434** 筆
- 公開 notebook 中保存的五類 class counts 總和為 **2,427**
- notebook 直接使用 `teen_running_soccer` 與 `teen_runsoc_target`
- 但公開 notebook 中找不到這兩個變數的建立過程
- notebook 未公開原始 numeric class-ID mapping
- 論文描述特徵縮放到 **-1 到 1**
- 公開 notebook 實際使用 **StandardScaler**

因此，本專案不將公開 notebook 視為可以完全原封不動執行的完整 reproduction package，而是將缺失部分明確標示為 reconstruction assumptions。

---

## 5. Preprocessing Reconstruction

依據公開 notebook 可見流程，本專案重建：

`public CSV -> X/y separation -> stratified 80/20 split -> StandardScaler -> SMOTE`

重建結果：

- 原始 X：**1,434 × 15**
- Training set：**1,147**
- Test set：**287**
- SMOTE 前 training rows：**1,147**
- SMOTE 後 training rows：**2,145**
- SMOTE 後五類各 **429** 筆

Scaler 僅在 training data 上 fit，SMOTE 也僅套用於 training data，以避免 test-set leakage。

---

## 6. Multiclass Diagnostic Baseline

四個 multiclass model 在相同 reconstructed preprocessing 下的結果：

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| XGBoost | **66.90%** | **0.6074** |
| SVM | 60.63% | 0.4739 |
| Random Forest | 60.63% | 0.5602 |
| Logistic Regression | 49.48% | 0.4742 |

此結果屬於 diagnostic multiclass baseline。

原論文的主要 XGBoost 結果來自 **10 組 pairwise binary classification**，因此這組 multiclass accuracy 不應直接與論文約 90% 的結果比較。

---

## 7. 10-Pair Binary XGBoost Reproduction

本專案依照五種運動兩兩配對，重建 10 個 binary classification tasks。

同時測試兩種 protocol：

### A. Paper-description protocol

`global stratified 80/20 split -> pair selection -> MinMaxScaler(-1,1) -> SMOTE -> XGBoost`

### B. Public-notebook protocol

`pair selection -> stratified 80/20 split -> StandardScaler -> SMOTE -> XGBoost`

為避免加入未公開假設，10 組皆使用公開 notebook 最後可見的固定 XGBoost 設定：

- n_estimators = 147
- max_depth = 8
- max_features = 0.353969
- random_state = 42

---

## 8. 10-Pair Accuracy 結果

| Pair | Paper reported | Paper-description | Public-notebook |
|---|---:|---:|---:|
| track & field vs football | 86.70% | 81.91% | 83.51% |
| track & field vs baseball | 89.04% | 85.62% | 89.73% |
| track & field vs swimming | 92.16% | 84.16% | 87.25% |
| track & field vs badminton | 93.55% | 94.57% | 95.70% |
| football vs baseball | 87.28% | 79.89% | 84.97% |
| football vs swimming | 91.47% | 91.47% | 93.02% |
| football vs badminton | 90.00% | 91.67% | 87.50% |
| baseball vs swimming | 91.95% | 89.66% | 91.95% |
| baseball vs badminton | 91.03% | 88.46% | 87.18% |
| swimming vs badminton | 88.28% | 84.85% | 91.18% |

平均 Accuracy：

- 論文表格數值平均：**90.15%**
- 論文文字報告：約 **90.14%**
- Paper-description reconstruction：**87.22%**
- Public-notebook reconstruction：**89.20%**

Mean absolute accuracy gap：

- Paper-description protocol：**3.46 percentage points**
- Public-notebook protocol：**2.40 percentage points**

在固定公開 XGBoost configuration 下，public-notebook protocol 的平均結果與論文報告較接近。

---

## 9. 可以重現到什麼程度

### 可重現部分

- 公開 dataset 可成功取得
- 主要特徵欄位與運動類別可重建
- 80/20 stratified split 可重建
- StandardScaler 與 SMOTE 流程可重建
- 四種 classical models 可執行
- 10 組 pairwise XGBoost tasks 可執行
- 重建後 XGBoost 平均 accuracy 可達 **89.20%**

### 無法完全重現部分

- 原始 `teen_running_soccer` 與 `teen_runsoc_target` 的建立方式未公開
- 原作者 numeric class mapping 未公開
- notebook 保存的 2,427 筆 class count 與公開 CSV 不一致
- 論文與 notebook 的 scaling 方法描述不一致
- 10 組 pairwise model 的完整最佳 hyperparameters 未公開
- 原論文提及的 1,000-epoch random search 無法從公開材料完整復原

---

## 10. 結論

本次重現顯示，原研究的主要 pairwise XGBoost classification 結果具有相當程度的可重建性。

在不修改公開原始資料、明確記錄 reconstruction assumptions，並使用公開 notebook 可見固定 XGBoost 設定的條件下，public-notebook protocol 的 10-pair 平均 accuracy 為 **89.20%**，與論文約 **90.14%** 的報告結果相差約 **0.94 percentage points**。

然而，由於公開 notebook 缺少 X/y 建立流程、numeric target mapping、完整 pair-specific hyperparameter search 結果，且 paper、code、data 之間存在 sample count 與 scaling 描述差異，因此本專案將結果定位為：

**a close reconstruction from publicly available materials, rather than an exact execution-level replication of the authors' original pipeline.**

---

## 11. 主要輸出檔案

- `notes/dataset_inspection.md`
- `notes/paper_code_data_audit.md`
- `notes/preprocessing_reconstruction.md`
- `notes/logistic_regression_baseline.md`
- `notes/classical_model_comparison.md`
- `notes/xgboost_10pair_reproduction.md`
- `reproduction/results/classical_model_metrics.csv`
- `reproduction/results/xgboost_10pair_results.csv`

