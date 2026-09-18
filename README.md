# 青少年男性運動員體適能機器學習分析重現研究

本專案旨在重現 Lee et al. (2024) 發表於 *PLOS ONE* 的研究：

> **Essential elements of physical fitness analysis in male adolescent athletes using machine learning**

原研究以男性青少年運動員為研究對象，涵蓋田徑、足球、棒球、游泳與羽球五種運動，利用多種機器學習方法分析不同運動項目的體適能特徵，並比較模型的分類表現。研究亦使用 XGBoost 特徵重要性與 SHAP（SHapley Additive exPlanations）分析各項體適能指標對分類結果的影響。

原研究共分析 1,489 名男性青少年運動員，並比較六種機器學習方法。研究結果顯示，XGBoost 具有最佳整體表現，平均準確率為 90.14%，AUC 為 0.86，F1-score 為 0.87。

## 專案目的

本專案的主要目的不是提出新的預測模型，而是驗證原研究之機器學習流程與結果是否可以被重新建立，藉此練習並展示研究重現（reproducibility）的完整能力。

重現內容包含：

- 公開資料取得與整理
- 資料前處理與標準化
- 訓練集與測試集切分
- 類別不平衡處理
- 機器學習模型訓練
- 交叉驗證
- 模型效能比較
- 混淆矩陣分析
- 特徵重要性分析
- SHAP 解釋分析
- 原研究結果與重現結果比較

## 原研究機器學習模型

原研究比較以下六種方法：

1. Logistic Regression
2. Support Vector Machine（SVM）
3. Elastic Net
4. Artificial Neural Network（ANN）
5. Random Forest
6. XGBoost

## 評估指標

本重現研究將依據原研究所採用的評估方式，檢視模型表現，包括：

- Accuracy
- Precision
- Recall
- F1-score
- AUC
- Confusion Matrix

## 重現流程

```text
原始公開資料
      ↓
資料清理與前處理
      ↓
Train / Test Split
      ↓
Standardization
      ↓
類別不平衡處理
      ↓
模型訓練與交叉驗證
      ↓
模型效能評估
      ↓
Feature Importance / SHAP
      ↓
與原論文結果比較
```

## 本專案的研究問題

本重現研究主要回答以下問題：

1. 原研究公開的資料與程式碼是否足以重新建立其機器學習分析流程？
2. 各模型的重現結果是否與原論文報告之結果一致或接近？
3. 若重現結果存在差異，可能來自哪些資料處理、模型設定或執行環境因素？

## 目前狀態

目前正在進行原始程式碼、資料結構與執行環境的檢查，後續將逐步建立可重複執行的重現流程，並記錄每一項重現結果與原研究之差異。

## 原始研究

**Lee, Y.-H., Chang, J., Lee, J.-E., Jung, Y.-S., Lee, D., & Lee, H.-S. (2024).**  
*Essential elements of physical fitness analysis in male adolescent athletes using machine learning.*  
PLOS ONE, 19(4), e0298870.  
DOI: https://doi.org/10.1371/journal.pone.0298870

原論文：  
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0298870

原作者公開程式碼：  
https://github.com/YunhwanJacobLee/Essential-elements-of-physical-fitness-analysis

## 專案定位

本 Repository 為學術研究重現專案，目的在於學習與驗證機器學習研究之可重現性。所有原始研究內容與資料來源之著作權均屬原作者及其原始授權條款所有。
