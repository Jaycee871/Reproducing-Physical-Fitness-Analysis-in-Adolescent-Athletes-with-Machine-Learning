# 中文研究重現海報

本資料夾包含一張 60 × 36 英吋橫式研究海報，採 ICML / NeurIPS 類型的 evidence-board 結構，內容以本 repository 已完成的 reproduction results 為基礎。

## 檔案

- `poster.html`：海報原始檔，可直接在瀏覽器預覽
- `render_poster.py`：使用 Playwright 將 HTML 輸出成 PDF 與 PNG
- `poster.pdf`：GitHub Actions 產生後的列印版
- `poster.png`：GitHub Actions 產生後的快速預覽圖

## 海報邏輯

1. Reproduction Target：要重現什麼
2. Audit & Reconstruction：Paper / Code / Data 核對與流程重建
3. Main Results：10 組 XGBoost 的主要結果
4. Reproducibility Findings：能重現什麼、哪些地方無法完全復原

## 現場使用

老師若要看執行結果，可先到 GitHub Actions 執行 `XGBoost 10-pair binary reproduction`，再回到本海報展示主要結論。
