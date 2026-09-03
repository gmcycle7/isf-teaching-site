---
title: Build Report 建置報告
description: 這次自動建置讀了哪些 PDF、產生了什麼、哪些成功、哪些仍需人工確認。
---

# Build Report 建置報告

本頁誠實記錄建置結果與限制（**目前狀態**）。可用 `python scripts/check_site_quality.py` 隨時重新檢查。
（注意：本頁刻意不在內文放裸的數學錢字號，以免被 Markdown 當公式處理。）

> **想看逐版演進歷史？** 完整 v1→v8 版本紀錄（含每次稽核、修正事件、部署備註的詳細過程）
> 已搬到獨立頁面 → **[Changelog 版本歷史](/00_overview/changelog)**。本頁只保留「現在的答案」。

## 1. 總共讀到幾篇 PDF？

來源資料夾共 **5 個 PDF**（`scripts/extract_papers.py` 全部掃描、dump 純文字）。

## 2. 每篇 paper 的 title / author / year

| id | 檔名 | Title | Authors | Year | 與 ISF 關係 |
|---|---|---|---|---|---|
| paper_001 | `general.pdf` | A General Theory of Phase Noise in Electrical Oscillators | A. Hajimiri, T. H. Lee | 1998 | **核心基礎** |
| paper_002 | `jitter_ring.pdf` | Jitter and Phase Noise in Ring Oscillators | A. Hajimiri, S. Limotyrakis, T. H. Lee | 1999 | **ring 延伸** |
| paper_003 | `BHongGenTheor-I_JSSC2019_Postprint.pdf` | Injection Locking and Pulling…Part I | B. Hong, A. Hajimiri | 2019 | 進階（injection） |
| paper_004 | `BHongGenTheor-II_JSSC2019_Postprint.pdf` | Injection Locking and Pulling…Part II | B. Hong, A. Hajimiri | 2019 | 進階（APF） |
| paper_005 | `Hajimiri_ISCS_98.pdf` | Design Issues in Cross-Coupled Inverter Sense Amplifier | A. Hajimiri, R. Heald | 1998 | **與 ISF 無關**（誠實標註） |

> **重要誠實聲明**：`Hajimiri_ISCS_98.pdf` 檔名像 ISF 論文，內容其實是 cross-coupled
> sense amplifier 設計，與 oscillator phase noise / ISF **無關**。僅在
> [paper_005 deep-dive](/05_paper_deep_dives/paper_005_cross_coupled_sense_amp) 誠實說明，
> 只當作「regeneration / 正回授」的概念橋樑。

## 3. 哪些公式成功轉成 LaTeX？

[P1]（general.pdf）的核心方程式 **Eq.(1),(9),(10),(11),(12),(13),(15)–(24)** 全部由
**高解析度渲染頁面 → 人工逐條對照**轉成 LaTeX，逐字用於教學頁與 `extracted/*.json`；
另有逐步代數展開（down-conversion 積分、factor-8 求和、L≈½S_φ 小角 PM、jitter 高通核、
flicker 1/f³ corner、Parseval 三類項）與兩個推導附錄（Floquet/PPV、Leeson↔ISF）。
歷次擴充的細節見 [changelog](/00_overview/changelog)（v1、v2 條目）。

## 4. 哪些公式現在的狀態是什麼（已核實 / 仍 TODO）？

**[P2] ring 常數**（Eq.16 Γrms 的 N-scaling、Eq.23 FOM 前置係數）與 **[P3]/[P4] injection & APF**
公式（廣義 Adler Eq.(30)/(35)、APF Fig.5/Eq.(18)–(22)）**皆已對照原始 PDF 逐字核實**，目前站上
的權威版本：

- Eq.(16)：$\Gamma_{rms}=\sqrt{2\pi^2/(3\eta^3)}\cdot\dfrac{1}{N^{1.5}}$ ⇒ $\Gamma_{rms}\propto N^{-3/2}$（$\Gamma_{rms}^2\propto N^{-3}$；根號只蓋常數 $2\pi^2/(3\eta^3)$，$N^{-1.5}$ 在根號外）。[P2] Eq.(16), p.794。
- Eq.(23) FOM：$\mathcal{L}\approx\frac{8}{3\eta}\frac{kT}{P}\frac{V_{DD}}{V_{char}}(f_0/\Delta f)^2$。前置係數是 $8/(3\eta)$（$\eta$ 為級延遲比例常數 Eq.(14)，$\approx 1$）；$\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入；$V_T=0$ 下限 Eq.(25) $\frac{16\gamma}{3\eta}$。
- Eq.(8)/(11)/(12)：$\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$（Eq.8）、$\kappa=(\Gamma_{rms}/q_{max})\sqrt{(\overline{i_n^2}/\Delta f)/2}$（Eq.12）。
- Eq.(17)/(18) 每級雜訊 $4kT\gamma\mu C_{ox}(W/L)\Delta V$、Eq.(21) 功率 $P=2\eta N V_{DD}q_{max}f_0$。
- **[P3]** Eq.(26) $\tilde\Gamma=\Gamma/q_{max}$；廣義 Adler Eq.(30),(33)；lock range Eq.(35) $\omega_L=\frac12 I_{inj}|\tilde\Gamma_1|$。
- **[P4]** amplitude decay $\tau_0=2Q/\omega_{osc}$；Eq.(26) ideal-LC 基波 quadrature；Eq.(27) amplitude-corrected Adler。

這些常數的**演變過程**（含兩次被抓到的誤讀、誰在哪一版修正）記錄在
[changelog 的誠實三次誤讀事件摘要](#5-三次誤讀更正事件摘要)與
[changelog](/00_overview/changelog) 的 v3/v4/v7 條目。

以下仍標 ⚠️ / `TODO`（外部文獻或次要細節，非核心 ISF/injection 物理，刻意保留）：

- **外部文獻（不在 5 篇 PDF 內）**：Leeson 1966、Demir et al. 2000（PPV）、Kärtner 1990 的正式卷期／頁碼（卷期／頁碼／公式記號已查證；period/cycle-to-cycle jitter 核已在 [jitter_kernels](/02_foundations/jitter_kernels) 自行從第一性推導＋Monte-Carlo 驗證，不再依賴外部慣例）。
- **[P2]** Fig.17 對稱電壓圖的確切座標軸；**[P4]** dual-modulus prescaler 的級數分配細節（Sec. VIII）。
- **[P5]**（sense amplifier，與 ISF 無關，刻意未轉錄）。
- **[P4]** APF 的確切定義式與傅立葉展開（Sec. III-D, p.2127）；Fig. 3 子圖標題。

可用 `python scripts/check_site_quality.py` 掃出所有 `TODO:` 標記。

## 5. 三次誤讀更正事件摘要

本站曾發生 **3 次「稽核誤把已核實內容改錯、還誤標成已核實」的事件**，每次都靠回頭放大原始 PDF ×
數值錨 × 獨立代數三重交叉驗證才抓回來：

1. **ring FOM 前置係數**：v2 誤改 $8/(3\gamma)$（誤標「逐字核實」）→ v4 對照 PDF p.796 修回 $8/(3\eta)$。
2. **Lorentzian 線寬的 D 映射**：v3 把方差成長率 κ² 誤當擴散常數 D → v5 用 MC＋解析擬合裁決修回 $D=\kappa^2/2$。
3. **[P2] Eq.(16) Γrms 的 N-scaling**：v3 誤讀根號範圍、把 v1 原本正確的 $N^{-3/2}$「更正」成 $N^{-3/4}$ → v7 對照論文正文「$1/N^{1.5}$」用語、$\eta=0.75$ 數值錨、App.B 代數三重驗證後修回 $N^{-3/2}$。

完整事件細節（含每次錯在哪、怎麼發現、修正後全站哪些頁面連動更新）見
[changelog](/00_overview/changelog) 的 v2/v3、v4、v5、v7 條目。

## 6. 哪些圖是從 paper 重新產生的 conceptual simulation？

全部圖都是用 Python **重新產生的概念模擬**（非從 PDF 擷取點陣圖），重現 [P1]/[P2] 的機制。
對應關係見 [figure_index](/01_paper_map/figure_index)。

## 7. 哪些圖只是 toy model（非 transistor-level）？

絕大多數為 toy / 概念模型（明確標註非 transistor-level）。少數純數學圖（jitter 積分、
Leeson↔ISF 疊圖、設計掃描、PLL transfer、BER bathtub）為公式計算，與解析式一致。

## 8. 哪些章節已經完整？

全部 7 大章（00 導覽／01 論文地圖／02 基礎／03 ISF 核心理論／04 模擬實驗／05 逐篇精讀／
06 設計直覺／99 附錄）皆已完整，公式已驗證、含逐步推導、worked example、互動 widget、
習題（含完整解答）。內容範圍演進見 [changelog](/00_overview/changelog)。

## 9. 哪些章節仍有 TODO？

核心理論的 TODO 已全數關閉（見上方第 4 點）。剩下的 `TODO` 都是**刻意保留的「外部文獻範圍」
標註**（如 period-jitter kernel 慣例出處、標準 LC-VCO 設計常識）與 transistor-level 排除聲明
（見第 12 點 3–4），不影響核心理論正確性。可用 `python scripts/check_site_quality.py` 掃出所有
`TODO:`。

## 10. `npm run build` 是否成功？

**成功**（Docusaurus 3.10.1，雙語 zh+en）：**0 broken links、0 KaTeX 警告**。數學渲染逐頁掃描通過
（無殘留原始 LaTeX、無 KaTeX parse error；程式碼區塊內的 matplotlib 錢字號屬正常）。

歷史修正（渲染 bug 類）記錄在 [changelog](/00_overview/changelog) 的 v2 條目。

## 11. `python scripts/run_all_sims.py` 是否成功？

**成功**：**49 個模擬腳本全數通過**，產生 56 張圖到
`static/figures/`。關鍵驗證：Lorentzian 模擬頻譜吻合理論、近載波轉平；Allan deviation 三種
FM 斜率精準落在 −1/2、0、+1/2；PLL 最佳 loop BW≈6.9 MHz、σ_t≈259 fs；數值法萃取 ISF 與理論
−sinθ 最大誤差 ~0.001；白噪 S_φ 與 1/f² 線吻合約 3 個十倍頻；jitter 積分數值=解析（447.9 fs）。

## 12. 現在的站點規模與例題 QA

**站點規模：97 頁 × 2 語系、56 圖、49 個模擬、21 個互動元件。**

`scripts/verify_examples.py` 把 docs 內每個有「標準答案」(`# ->`) 的 Python 例題實際跑一遍對數值：
**160 個可驗證 block 中 147 個自動通過、0 個不符、0 個錯誤**；其餘為驗證器對註解裡的公式常數
（如 $2\Gamma_{rms}^2$ 的「2」）或對照用數字的誤判，經人工確認正確。`check_site_quality.py`
掃描：pages / figures present / required figs missing / content issues / soft warnings / open
TODOs 的最新數字見終端輸出。

演進細節（每一版新增了什麼、什麼時候修了什麼 bug）見 [changelog](/00_overview/changelog)。

## 誠實與 TODO 原則

- toy model 一律標明「這是 pedagogical toy model，非 transistor-level」。
- 來自外部文獻（PPV / adjoint / Floquet / Leeson / Demir）一律標「不在下載的 5 篇 PDF 內，
  以標準文獻補充」。
- 不確定的常數/figure/citation 一律寫 `TODO: manual verification needed ...`，不用猜的湊數字。
- [P5] 一律誠實說明它是 sense amplifier 論文、與 ISF 無關，只當邊角概念橋樑。
- 任何「稽核聲稱的更正」在套用到全站前，必須本人放大原始 PDF、比對數值錨、與獨立代數
  三重驗證——本站有 3 次真實發生過的反例（見上方第 5 點），此原則不是紙上談兵。
- 論文本身的印刷勘誤（如 [P2] Fig.16 的 ζ=2.5e5 應為 2.5e-5、[P1] p.191 的 "58.8 fF" 應為
  fC）也誠實標注，不悄悄「校正」掉不提。

## 下一步建議人工確認

1. ~~用原始 PDF 核對 [P2]/[P3]/[P4] 的確切常數與方程形式~~ → **已完成**（見上方第 4 點與
   [changelog](/00_overview/changelog) v3/v4/v7）。
2. ~~補外部文獻（Leeson、Demir PPV、Kärtner、Adler）的正式卷期／頁碼／DOI~~ → **已完成**
   （見 [changelog](/00_overview/changelog) v4）。
3. 若要 transistor-level 精度：用 Spectre PSS+PNoise/PXF 或 adjoint 法，從真實 LC-VCO /
   ring-VCO 萃取 ISF 與 cyclostationary α(x)，取代 toy 模型。（仍為刻意排除的範圍）
4. 校準互動計算器與各 toy 模型的絕對數值到實際製程。

## 部署上線

以 **GitHub Pages（project page）** 公開上線：

- 網站：`https://gmcycle7.github.io/isf-teaching-site/`
- 原始碼（public）：`https://github.com/gmcycle7/isf-teaching-site`
- `baseUrl` 設為 `/isf-teaching-site/`；KaTeX CSS／字型經 webpack 打包（baseUrl-safe、完全離線）。
- 部署機制：本機 `npm run build` 後將 `build/` 推到 `gh-pages` 分支（含 `.nojekyll`），Pages 由該
  分支供應；已封裝成一鍵腳本 **`./scripts/deploy.sh`**（只需 `repo` 權限，不需 `workflow` scope）。
- **版權處理**：5 篇論文**全文與 PDF 不入庫**（`.gitignore` 排除 `extracted/raw_text/` 與
  `*.pdf`）；footer 與各頁標註版權屬原作者，內容為教學用途。
- CI（選配）：`.github/workflows/deploy.yml` 已備；需 token `workflow` 權限
  （`gh auth refresh -s workflow`）才能推送 workflow 檔，啟用 push-to-deploy 自動部署。

部署過程中的個別事件（如大型部署卡住的排解方式）見 [changelog](/00_overview/changelog)。

---

> **完整版本歷史（v1→v8，含每次稽核與修正的詳細過程）** → **[Changelog 版本歷史](/00_overview/changelog)**
