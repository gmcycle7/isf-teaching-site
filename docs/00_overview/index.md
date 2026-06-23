---
title: ISF 與振盪器相位雜訊
description: 從論文到設計直覺 — Impulse Sensitivity Function 教學網站首頁。
slug: /
---

# ISF and Oscillator Phase Noise: From Paper to Design Intuition

> 從論文到設計直覺。本站把 Hajimiri–Lee 的 **Impulse Sensitivity Function（ISF，
> 脈衝敏感度函數）** 理論，從第一原理一路推到 SerDes clock jitter 的設計手感。
> **每條公式逐步推導、標單位、給數值、附 Python 與圖、標明論文來源。**

## 這個網站為誰而寫（Who this site is for）

假設你是**電機系大學畢業生**：懂電路學、電子學、訊號與系統、隨機程序、傅立葉轉換、
基本 DSP，但**還沒有**真正掌握 oscillator phase noise（相位雜訊）、timing jitter
（時間抖動）、ISF、cyclostationary noise（週期穩態雜訊）、LTV oscillator model
（線性時變振盪器模型）。讀完本站，你應該能：

- 看懂並**自己重推** [P1] Hajimiri–Lee 1998 的核心公式；
- 解釋「為什麼振盪器對 noise 是 LTV 而非 LTI」；
- 從 ISF 算出 phase noise、把 phase noise 換成 rms jitter；
- 說出降低 1/f² 與 1/f³ phase noise 的**設計旋鈕**；
- 把這些連到 **SerDes clocking**（LC-VCO / ring-VCO / PLL / CDR）的實務直覺。

## 從你的目標開始（Start from your goal）

完整的 9 步循序路徑見 [循序學習路徑 Learning Path](/00_overview/learning_path)；
但如果你心裡已經有一個具體目標，直接從下面三張「入口卡」挑一張切進去比較快。

### 我要從零學懂 ISF

不趕時間、想把 oscillator phase noise（相位雜訊，振盪訊號相位的隨機抖動）的來龍去脈
弄清楚。先建立「振盪器的相位到底是什麼」的物理直覺，再沿著規劃好的路徑往下走。

- [Oscillator phase 是什麼？](/02_foundations/oscillator_phase) — 從 limit cycle 看相位 vs 振幅
- [循序學習路徑 Learning Path](/00_overview/learning_path) — 9 步、由淺入深的完整路線

### 我手上有 phase-noise 圖、要算 jitter

已經拿到一張量測或 spec 上的 $\mathcal{L}(\Delta f)$ 曲線，想知道怎麼把它換成 rms timing
jitter（時間抖動，edge 相對理想時刻的偏差），以及這對 SerDes 鏈路代表什麼。

- [Phase Noise → Jitter](/02_foundations/psd_phase_noise_jitter) — PSD、$\mathcal{L}(f)$、各種 jitter 的定義與換算
- [從 ISF 到 SerDes clocking](/06_design_insights/serdes_clocking_connection) — jitter 如何收斂到 eye / BER
- [Lab 08 — 從 L(f) 積分得 rms jitter](/04_simulation_labs/lab_08_jitter_integration) — 動手把 $\mathcal{L}(f)$ 積分出 $\sigma_t$

### 我在讀 Hajimiri 論文

正坐在某一篇 paper 前面，想對照「這條式子在本站哪裡有逐步推導」。

- [逐篇精讀導覽 Paper Deep Dives](/05_paper_deep_dives) — 五篇來源論文逐篇精讀
- [公式推導索引 Equation Index](/01_paper_map/equation_index) — 由 [Px] Eq.(n) 反查本站推導

### 隨手查（Quick reference）

不想讀整頁、只要查一個符號、一個詞、或一條式子：

- [速查表 Cheat Sheet](/00_overview/cheat_sheet) — 招牌公式與數值手感一頁打包
- [統一符號表 Notation](/00_overview/notation) — 全站一致的符號、意義、單位
- [中英對照詞彙表 Glossary](/99_appendix/glossary) — 英文術語的中文直覺解釋
- [公式推導索引 Equation Index](/01_paper_map/equation_index) — 公式 ↔ 論文出處 ↔ 推導頁

## 必備背景（Required background）

線性系統與卷積、傅立葉級數／轉換、隨機程序與 PSD（功率譜密度）、基本電路（RLC、電容
$q=Cv$）、一點 Python/NumPy。**不需要**先懂振盪器雜訊——那正是本站要教的。

## 怎麼跑模擬（How to run simulations）

```bash
# 安裝網站相依套件
npm install
# 啟動本機網站（http://localhost:3000）
npm run start
# 一鍵重跑所有模擬、產生 static/figures/ 下所有圖
python scripts/run_all_sims.py
```

所有圖都可追溯到 [figure_index](/01_paper_map/figure_index) 裡的 script 與公式。

## 怎麼讀公式（How to read equations）

公式用 KaTeX 顯示。每條重要公式都會：標 **[Px] Eq.(n) page** 來源、解釋**物理意義**、
列**單位**、給**數值例子**、說明**適用與失效條件**。看到 `TODO:` 表示該處仍需人工對照
原始 PDF。看到「toy model」表示那是教學用簡化模型，不代表 transistor-level 精度。

## 參考文獻（References）

五篇來源論文與外部補充見 [references](/99_appendix/references)；逐篇精讀見
[paper deep dives](/05_paper_deep_dives/)；論文地圖見 [paper_summary_table](/01_paper_map/paper_summary_table)。

> **誠實聲明**：來源資料夾共 5 個 PDF，其中 4 篇是 Hajimiri 系列的 oscillator
> phase noise / injection 論文，**1 篇（`Hajimiri_ISCS_98.pdf`）其實是 cross-coupled
> sense amplifier 論文、與 ISF 無關**，本站誠實標註並只當邊角註解。詳見
> [build_report](/00_overview/build_report)。
