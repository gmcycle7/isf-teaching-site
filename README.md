# ISF Teaching Site — 振盪器相位雜訊與 Impulse Sensitivity Function 教學網站

一個可本機啟動的靜態教學網站，把 Hajimiri–Lee 的 **Impulse Sensitivity Function (ISF)**
相位雜訊理論，從第一原理逐步推導到 SerDes clocking 設計直覺。內容為**繁體中文**，
保留必要英文專業詞。每條公式逐步推導、標單位、給數值、附 Python 與圖、標明論文來源。

技術棧：**Docusaurus 3 + MDX + KaTeX**（數學）＋ **Mermaid**（方塊圖）＋ Python (NumPy/SciPy/Matplotlib) 模擬。

---

## 最簡單：雙擊開啟（macOS）

在 `isf-teaching-site` 的**上一層資料夾**有一個 **`Open-ISF-Site.command`**。
**直接雙擊它**即可：它會自動啟動本機網站並用瀏覽器打開（首次會自動安裝相依套件與建置）。
要關閉網站，把跳出來的終端機視窗關掉即可。

> 註：請勿用瀏覽器直接開 `build/index.html`（`file://`）。Docusaurus 是 SPA，
> 一定要透過本機伺服器（上面的啟動器或下面的 `npm run serve`）才能正常顯示。

## Setup（安裝，手動方式）

需求：Node.js ≥ 18、Python ≥ 3.10（建議 3.12）、`pip install numpy scipy matplotlib pymupdf`。

```bash
cd isf-teaching-site
npm install
```

## Run website（啟動本機網站）

```bash
npm run start          # 開發伺服器，預設 http://localhost:3000
```

## Run all simulations（重跑所有模擬、產生所有圖）

```bash
python scripts/run_all_sims.py
```

會執行 `simulations/lab_*.py`，把所有圖輸出到 `static/figures/`（共 14 張）。

## Build（產生靜態網站）

```bash
npm run build          # 輸出到 build/
npm run serve          # 本機預覽 build 結果
```

## Quality check（品質檢查）

```bash
python scripts/check_site_quality.py            # 靜態檢查（title/citation/figure/lab/TODO）
python scripts/check_site_quality.py --build     # 連同 npm run build 一起檢查
```

---

## Project structure（專案結構）

```
isf-teaching-site/
├── README.md
├── package.json / docusaurus.config.js / sidebars.js
├── src/css/custom.css
├── docs/                      # 教學內容（MDX）
│   ├── 00_overview/           # 導覽、學習路徑、notation、build report
│   ├── 01_paper_map/          # 論文地圖、公式/圖表索引、claims 交叉引用
│   ├── 02_foundations/        # 振盪器相位、LTI vs LTV、雜訊基礎、PSD↔jitter
│   ├── 03_isf_core_theory/    # ISF 定義、推導、Fourier、白噪/flicker、rms/effective ISF
│   ├── 04_simulation_labs/    # 9 個模擬實驗 + numerical_feeling
│   ├── 05_paper_deep_dives/   # 逐篇精讀（5 篇 PDF）
│   ├── 06_design_insights/    # symmetry/slope/swing/LC vs ring/SerDes
│   └── 99_appendix/           # 數學工具、Python 環境、glossary、references
├── extracted/                 # 結構化來源資料（JSON）+ 作者規範
│   ├── paper_metadata.json    # 5 篇論文的人工審閱 metadata（含已驗證公式）
│   ├── paper_metadata.auto.json  # extract_papers.py 自動產生的機械抽取
│   ├── extracted_equations.json / extracted_figures.json / extracted_claims.json
│   └── _AUTHORING_SPEC.md      # 撰寫規範（不會被 build）
├── simulations/
│   ├── common/                # signal/noise/oscillator/isf/plot 工具庫
│   └── lab_01..lab_08.py       # 各模擬腳本
├── static/figures/            # 由模擬產生的 PNG（網站以 /figures/x.png 引用）
└── scripts/
    ├── extract_papers.py       # 掃描 PDF、dump 純文字、產生 auto metadata
    ├── build_equation_index.py # 從 JSON 重建 docs/01_paper_map/equation_index.md
    ├── run_all_sims.py         # 一鍵跑全部模擬
    └── check_site_quality.py   # 品質檢查
```

---

## How papers were extracted（論文如何被抽取）

1. `scripts/extract_papers.py` 用 **PyMuPDF (fitz)** 掃描來源資料夾（本專案的上層目錄）內所有
   PDF，dump 純文字到 `extracted/raw_text/`，並產生 `paper_metadata.auto.json`。
2. PDF 的**敘述文字**抽取乾淨，但**數學符號**在純文字中會遺失（數學字型問題）。因此公式是把
   方程式密集的頁面**高解析度渲染成圖**後，由作者**逐條對照轉成 LaTeX**，存進人工審閱的
   `extracted/paper_metadata.json` 與 `extracted_equations.json`。
3. 凡無法確認的公式/figure/citation 一律標 `TODO: manual verification needed`。

來源資料夾共 5 個 PDF。其中 4 篇是 Hajimiri 系列 oscillator phase noise / injection 論文；
**1 篇（`Hajimiri_ISCS_98.pdf`）實際上是 cross-coupled sense amplifier 論文、與 ISF 無關**，
本站誠實標註並僅作邊角註解。詳見 `docs/00_overview/build_report.md`。

## How to add a new paper（如何新增論文）

1. 把 PDF 放進來源資料夾，執行 `python scripts/extract_papers.py`。
2. 在 `extracted/paper_metadata.json` 新增一筆（含已驗證公式；無法確認者標 TODO）。
3. 在 `extracted/extracted_equations.json` 補公式後跑 `python scripts/build_equation_index.py`。
4. 在 `docs/05_paper_deep_dives/` 新增一頁、更新 `sidebars.js`、`docs/01_paper_map/*`。

## Known limitations（已知限制）

- 所有模擬皆為 **pedagogical toy model**，重現的是 ISF 理論的**機制**，**非 transistor-level 精度**。
- KaTeX CSS 與字型已**自帶於 `static/katex/`**（離線可用）；無需網路。
- 部分 ring oscillator 常數、Hong 2019 injection 公式、APF 確切式標為 `TODO`，需人工對照原始 PDF。
- PPV / adjoint / Floquet / Leeson 等屬**外部文獻**（不在下載的 5 篇 PDF 內），以標準知識補充並標明。

## TODOs requiring manual verification

集中列於 `docs/00_overview/build_report.md`，並可用 `python scripts/check_site_quality.py`
即時掃出所有 `TODO:` 標記。
