---
title: Build Report 建置報告
description: 這次自動建置讀了哪些 PDF、產生了什麼、哪些成功、哪些仍需人工確認。
---

# Build Report 建置報告

本頁誠實記錄建置結果與限制。可用 `python scripts/check_site_quality.py` 隨時重新檢查。
（注意：本頁刻意不在內文放裸的數學錢字號，以免被 Markdown 當公式處理。）

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
**高解析度渲染頁面 → 人工逐條對照**轉成 LaTeX，逐字用於教學頁與 `extracted/*.json`。
v2 另補上逐步代數展開（down-conversion 積分、factor-8 求和、L≈½S_φ 小角 PM、jitter 高通核、
flicker 1/f³ corner、Parseval 三類項），以及兩個推導附錄（Floquet/PPV、Leeson↔ISF）。

## 4. 哪些公式需要 manual verification？

**[P2] ring 常數已於 v3 對照原始 PDF（高解析度渲染）逐字核實並更正**：
- Eq.(16)：$\Gamma_{rms}=\sqrt{2\pi^2/(3\eta^3)\cdot N^{-1.5}}$ ⇒ $\Gamma_{rms}\propto N^{-3/4}$（$\Gamma_{rms}^2\propto N^{-3/2}$）。
  更正了先前誤寫的「$\Gamma_{rms}\propto N^{-3/2}$」與猜測常數「$2\pi/\sqrt3$」，並加註論文「公式 vs 文字」的不一致。
- Eq.(23) FOM：$\mathcal{L}\approx\frac{8}{3\eta}\frac{kT}{P}\frac{V_{DD}}{V_{char}}(f_0/\Delta f)^2$。
  前置係數是 $8/(3\eta)$（$\eta$ 為級延遲比例常數 Eq.(14)，$\approx 1$）；$\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入，並補回漏掉的 $V_{DD}/V_{char}$ 因子；$V_T=0$ 下限 Eq.(25) $\frac{16\gamma}{3\eta}$。
  （v2 曾誤改為 $8/(3\gamma)$ 並誤標「逐字核實」，v3 已對照原始 PDF p.796 更正。）
- Eq.(8)/(11)/(12)：$\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$（Eq.8，先前誤標 Eq.10）、$\kappa=(\Gamma_{rms}/q_{max})\sqrt{(\overline{i_n^2}/\Delta f)/2}$（Eq.12）。
- Eq.(17)/(18) 每級雜訊 $4kT\gamma\mu C_{ox}(W/L)\Delta V$、Eq.(21) 功率 $P=2\eta N V_{DD}q_{max}f_0$ 皆已核實。

**[P3]/[P4] injection & APF 公式也已於 v3 對照原始 PDF 逐字核實**：
- **[P3]** Eq.(26) $\tilde\Gamma=\Gamma/q_{max}$；廣義 Adler Eq.(30),(33) $\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$，
  $\Omega(\theta)=\frac{1}{T_{osc}}\int\tilde\Gamma(\omega_0 t+\theta)i_{inj}dt$；正弦退化 Eq.(34)、lock range Eq.(35) $\omega_L=\frac12 I_{inj}|\tilde\Gamma_1|$。
- **[P4]** Eq.(25) amplitude decay $d(t,\phi)=e^{-t/\tau_0}$、$\tau_0=2Q/\omega_{osc}$；Eq.(26) ideal-LC 基波
  $\tilde\Gamma_1=\frac{1}{q_{max}}\angle90°$、$\tilde\Lambda_1=\frac{\tau_0}{q_{max}}\angle0°$（quadrature）；Eq.(27) amplitude-corrected Adler。

以下仍標 ⚠️ / `TODO`（外部文獻或次要細節，非核心 ISF/injection 物理）：

- **外部文獻（不在 5 篇 PDF 內）**：Leeson 1966、Demir et al. 2000（PPV）、Kärtner 1990 的正式卷期／頁碼。
- **[P2]** Fig.17 對稱電壓圖的確切座標軸；**[P4]** dual-modulus prescaler 的級數分配細節（Sec. VIII）。
- **[P5]**（sense amplifier，與 ISF 無關，刻意未轉錄）。
- **[P4]** APF 的確切定義式與傅立葉展開（Sec. III-D, p.2127）；Fig. 3 子圖標題。
- **外部文獻（不在 5 篇 PDF 內）**：Leeson 1966、Demir et al. 2000（PPV）、Kärtner 1990 ——
  卷期／頁碼／公式記號待補正式 citation；period/cycle-to-cycle jitter 核的單邊/雙邊常數慣例。

**v3 audit corrections（對照原始 PDF 的稽核更正）**：ring FOM 前置係數重新訂正為 $8/(3\eta)$（min $16\gamma/(3\eta)$，見上）；**[P4]** ISF/APF 圖由 Fig. 3 更正為 Fig. 5（p.2126）；citation 頁碼更正：**[P2]** Fig.17（對稱電壓圖）p.802、**[P4]** Sec. VIII p.2135、**[P1]** Fig.4 p.181、$f_0=1/(2N\tau_D)$ 改引 Eq.(15)；TODO 關閉：**[P1]** cyclostationary $i_n(t)=i_{n0}(t)\alpha(\omega_0 t)$、$\Gamma_{eff}=\Gamma\cdot\alpha$（Sec. II-D, Eq.(25)–(27), p.186）與廣義 Adler（**[P3]** Eq.(30)/(35)）皆已核實；另修 2 個程式 bug：lab_05 的 Parseval DC 項應以 $(c_0/2)^2$ 計入、`accumulated_jitter_curve` 呼叫缺 `f0`/誤用 `max_lag` 已修正。

可用 `python scripts/check_site_quality.py` 掃出所有 `TODO:` 標記。

## 5. 哪些圖是從 paper 重新產生的 conceptual simulation？

全部圖都是用 Python **重新產生的概念模擬**（非從 PDF 擷取點陣圖），重現 [P1]/[P2] 的機制。
對應關係見 [figure_index](/01_paper_map/figure_index)。

## 6. 哪些圖只是 toy model（非 transistor-level）？

絕大多數為 toy / 概念模型（明確標註非 transistor-level）。少數純數學圖（jitter 積分、
Leeson↔ISF 疊圖、設計掃描、PLL transfer、BER bathtub）為公式計算，與解析式一致。

## 7. 哪些章節已經完整？

- **00 導覽 / 01 論文地圖 / 02 基礎 / 03 ISF 核心理論**（公式已驗證，v2 補逐步推導與例題）
- **04 模擬實驗**：numerical_feeling、worked_examples 例題庫、互動工具（3 widget）、lab_01–lab_17
- **05 逐篇精讀（5 篇）/ 06 設計直覺 / 99 附錄（含 Floquet-PPV、Leeson、HTM 推導）**

> **v3 深化（研究所等級）**：新增 **Lorentzian 線寬**（解 1/f² 在 Δf→0 發散矛盾）、
> **Allan variance / ADEV**（時域頻率穩定度）、**嚴格頻譜推導**（cyclostationary 自相關→Wiener-Khinchin）、
> **PLL 完整雜訊預算 + 最佳 loop BW**、**真實拓樸 ISF**（cross-coupled VCO tail 上轉、Colpitts、ring stage）、
> **量測與 spur**、**LTV/HTM** 附錄、**Capstone**（ideal LC 從 state equations 一路到 BER）、
> 以及 **02/03/06 三章成套習題（含完整解答）**。配 4 個新模擬（lab_18–21）。

## 8. 哪些章節仍有 TODO？

主要是 05 的 [P2]/[P3]/[P4] deep-dive 與用到 ring 常數的 06/03 頁（見第 4 點）。
這些 TODO 不影響核心 ISF 理論（[P1]）的正確性，只關乎進階論文的確切常數與外部文獻 citation。

## 9. `npm run build` 是否成功？

**成功**（Docusaurus 3.10.1）。最新數字（v2）見本頁最後的「自動檢查結果」一節與
`npm run build` 輸出：**0 broken links、0 KaTeX 警告**。數學渲染逐頁掃描通過
（無殘留原始 LaTeX、無 KaTeX parse error；程式碼區塊內的 matplotlib 錢字號屬正常）。

歷史修正：曾修兩類渲染 bug——(a) 多行 display math 的圍欄未獨立成行，導致 micromark 連鎖
吃掉後續公式（已用 normalizer 全站修正並設為固定流程）；(b) 數學內誤用 HTML 實體
（gt/lt entity）→ 已改回數學用的大於/小於符號。

## 10. `python scripts/run_all_sims.py` 是否成功？

**成功**：**20/20 labs 通過，產生 26 張圖**到 `static/figures/`（原 14 + v2 八 + v3 四）。關鍵驗證：
Lorentzian 模擬頻譜吻合理論、近載波轉平；Allan deviation 三種 FM 斜率精準落在 −1/2、0、+1/2；
PLL 最佳 loop BW≈6.9 MHz、σ_t≈259 fs。另：
數值法萃取 ISF 與理論 −sinθ 最大誤差 ~0.001；白噪 S_φ 與 1/f² 線吻合約 3 個十倍頻；
jitter 積分數值=解析（447.9 fs）。

## 11. `check_site_quality.py` 檢查結果

最新一次檢查的數字見終端輸出（pages / figures present / required figs missing /
content issues / soft warnings / open TODOs / build）。v2 後品質腳本新增：8 張新必備圖、
核心/設計頁「≥2 numeric example」軟性警告。

## 11b. 例題數值 QA（v3）

新增 `scripts/verify_examples.py`：把 docs 內每個有「標準答案」(`# ->`) 的 Python 例題實際跑一遍對數值。**80 個可驗證 block 中 65 個自動通過、0 個錯誤**；其餘 14 個經人工確認正確（驗證器對註解裡的公式常數如 $2\Gamma_{rms}^2$ 的「2」、或對照用數字如「遠小於 447.9 fs」誤判）。過程修了真實 bug：`np.trapz`→`np.trapezoid`（NumPy 2.0）×3、壞掉的 `import`（補 `simulations/__init__.py` 使套件可匯入）、2 個寫錯的例題數值（effective_isf 的 $c_2$、PLL 最佳 BW 的 $S_{ref}$）。並修了 **dark-mode 圖**：matplotlib PNG 在深色模式加白底卡片（`.markdown img` CSS）。

## 12. 下一步建議人工確認

1. 用原始 PDF 核對 [P2]/[P3]/[P4] 的確切常數與方程形式（第 4 點）。
2. 補外部文獻（Leeson、Demir PPV、Kärtner）的正式卷期／頁碼／公式記號。
3. 若要 transistor-level 精度：用 Spectre PSS+PNoise/PXF 或 adjoint 法，從真實 LC-VCO /
   ring-VCO 萃取 ISF 與 cyclostationary α(x)，取代 toy 模型。
4. 校準互動計算器與各 toy 模型的絕對數值到實際製程。
