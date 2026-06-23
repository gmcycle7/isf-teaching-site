# ISF 教學網站 — 深化計劃 v2（讓內容「研究所等級」完整）

> 第二輪「不夠詳細」review。結論：**現有核心推導其實夠紮實**（isf_definition 有親手推 Γ=−sin、
> Floquet 附錄有 6 步嚴格推導、white_noise 有 down-conversion 明算）。真正缺的是
> **(A) 幾個關鍵嚴格結果整個沒有**，以及 **(B) 整片進階主題沒涵蓋**。以下用實際 grep 證據列出。

## 0. Review 證據（grep 全站）

| 主題 | 現況 | 缺口 |
|---|---|---|
| **Lorentzian lineshape / 載波線寬** | **0 頁** | 振盪器真實頻譜是 Lorentzian、有限線寬；1/f² 只是近似且在 Δf→0 發散——**完全沒提** |
| **Allan variance / ADEV / 頻率穩定度** | **0 頁** | 時域頻率穩定度、L(f)↔ADEV、斜率對照表——**完全沒提** |
| 嚴格頻譜推導（cyclostationary 自相關→Wiener-Khinchin） | 只有 sum-of-tones 啟發式 | 缺嚴格的 LTV 輸出 PSD 推導 |
| PLL 完整雜訊預算（ref/CP/divider/VCO 加總） | 2 頁觸及、只有 transfer-function lab | 缺完整 budget 與最佳 loop BW 推導 |
| 量測技術（delay-line / cross-correlation / SA） | 1 頁一筆帶過 | 缺量測方法、spur vs PN、如何讀 PN 圖 |
| 真實拓樸 worked analysis（cross-coupled VCO、Colpitts） | 被「提到」7–9 次 | 從未真正**逐項分析**（noise source→ISF 諧波→L） |
| HTM / Zadeh 時變傳函（嚴格 LTV 框架） | 1 頁 | 缺 harmonic transfer matrix 嚴格框架 |
| 習題（problem set with solutions） | 3 頁有零星「練習」 | 缺每章成套習題與完整解答 |

現有核心頁深度（display-eq 數）其實不低：white_noise=29、fourier=19、rms_isf=17、
convolution=16、flicker=16、Floquet 附錄=20。所以**不是現有頁跳步**，是**廣度與幾個嚴格頂點缺**。

---

## TIER 1 — 缺掉的關鍵嚴格結果（最高優先，研究生一眼會發現的洞）

### T1.1 Lorentzian 線寬與有限載波寬度（新頁 03_isf_core_theory/lorentzian_linewidth.md）
- **要點**：相位做 random walk → $\langle\Delta\phi^2(t)\rangle$ 線性成長 → 載波自相關
  $R(\tau)=\frac{1}{2}e^{-|\tau|/\tau_c}$（指數）→ 頻譜是 **Lorentzian**，3-dB 線寬
  $\Delta f_{3dB}=\pi\,c$（$c$ = phase diffusion 常數）。
- **為何重要**：解決「[P1] Eq.(21) 的 $1/\Delta\omega^2$ 在 $\Delta\omega\to0$ 發散」這個學生一定會問的矛盾——
  真實頻譜在很靠近載波處轉平（Lorentzian peak），總功率守恆（積分=載波功率）。
- **逐步**：$\langle\Delta\phi^2\rangle=c|t|$ → $E[e^{j\Delta\phi}]=e^{-c|t|/2}$（高斯）→ Wiener-Khinchin → Lorentzian。
  連到 Demir 2000（[E2]，已查證 citation）的嚴格 phase-diffusion。
- **新 sim**：`lab_18_lorentzian.py` — 時域產生相位漫步載波、FFT、擬合 Lorentzian、量 3-dB 線寬，
  驗證 $\Delta f_{3dB}$ 與 $\Gamma_{rms}^2/q_{max}^2\cdot S_i$ 的關係。圖 `lorentzian_carrier_lineshape.png`。

### T1.2 嚴格頻譜推導：cyclostationary 自相關 → Wiener-Khinchin（深化 white_noise 或新頁）
- **要點**：把目前的「sum-of-tones」啟發式升級成嚴格版：LTV 系統 $\phi(t)=\int h_\phi(t,\tau)i(\tau)d\tau$
  的輸出，對 cyclostationary 輸入，用 time-averaged autocorrelation → harmonic PSD → $S_\phi$。
  證明 $\sum c_n^2=2\Gamma_{rms}^2$ 怎麼**自然從自相關出來**（不是用單音湊）。
- **逐步**：$R_\phi(t,t+\tau)$ → time-average over period → 用 ISF Fourier 係數展開 → $S_\phi(\omega)$。

### T1.3 Allan variance / 時域頻率穩定度（新頁 02_foundations/allan_variance.md）
- **要點**：$\sigma_y^2(\tau)$ 的定義、與 $S_\phi$/$S_y$ 的轉換積分、五種雜訊（white/flicker PM、
  white/flicker FM、random-walk FM）對應的 $\sigma_y(\tau)$ 斜率對照表，為何振盪器/時鐘界用 ADEV。
- **逐步**：$\sigma_y^2(\tau)=2\int S_y(f)\frac{\sin^4(\pi f\tau)}{(\pi f\tau)^2}df$（已知核），各雜訊型代入給斜率。
- **新 sim**：`lab_19_allan.py` — 由 L(f) 算 ADEV、畫 $\sigma_y(\tau)$ vs $\tau$、標各段斜率。圖 `allan_deviation.png`。

---

## TIER 2 — 整片缺的系統級主題（廣度）

### T2.1 PLL 完整相位雜訊預算（新頁 06_design_insights/pll_noise_budget.md，深化 lab_13）
- ref、PFD/charge-pump、loop filter、divider、VCO 五個來源各自的 transfer 與加總；in-band vs out-of-band；
  reference spur；**最佳 loop BW** 使積分 jitter 最小（對 BW 微分=0）。新 sim：budget 疊圖 + 最佳 BW 掃描。

### T2.2 真實拓樸 worked analysis（新頁 06_design_insights/real_oscillator_topologies.md，手算層級、非 Spectre）
- **cross-coupled LC VCO**：tail current source noise 的 **2× upconversion**、switching-pair 的 cyclostationary、
  ISF 形狀；**Colpitts**：為何 ISF 在特定相位窄；**CMOS inverter ring stage**：由 switching slope 推 ISF。
  每個把 device noise → ISF 諧波 → L 做完整一條鏈（手算 + 量級）。

### T2.3 量測與 spur（新頁 06_design_insights 或 99_appendix/measurement_and_spurs.md）
- 量 L(f) 的三法（SA 直接、PLL/delay-line discriminator、cross-correlation 降本底）；
  **spur（確定性邊帶）vs 隨機相位雜訊**怎麼分；如何讀真實 PN 圖（標記各段斜率、corner、floor、spur）。

---

## TIER 3 — 嚴格 LTV 框架（數學深化）

### T3.1 LTV 系統理論：Zadeh 時變傳函與 HTM（深化 lti_vs_ltv 或新附錄 99_appendix/ltv_htm.md）
- Zadeh $H(f,t)$、bifrequency function、**harmonic transfer matrix (HTM)**；證明 ISF 是相位輸出的 HTM 的
  第一列；連回讀者的訊號與系統背景。

### T3.2 cyclostationary 嚴格化（深化 effective_isf）
- 從 transistor bias-dependent 熱雜訊推 **NMF $\alpha(t)$**；white cyclostationary noise 的 folding；
  switching pair 的具體 worked example（$\Gamma_{eff}=\Gamma\alpha$ 的 $c_0$ 改變如何影響 1/f³）。

---

## TIER 4 — 教學完整性

### T4.1 每章成套習題 + 完整解答（新頁 ×3）
- `02_foundations/exercises.md`、`03_isf_core_theory/exercises.md`、`06_design_insights/exercises.md`，
  各 6–8 題（推導題 + 數值題 + 設計反推題），附**完整解答**與 Python 驗證。

### T4.2 Capstone：一顆 ideal LC 從頭到尾全嚴格（新頁 03_isf_core_theory/capstone_lc_end_to_end.md）
- 一條龍：state equations → 線性化/Floquet → $\Gamma=-\sin$ → $\Gamma_{rms}$ → $S_\phi(\Delta\omega)$ →
  **Lorentzian 線寬** → $\sigma_t$ → BER，每一步都嚴格、都帶數值。當作「只讀一頁就懂整套」的主脊。

---

## 範圍與優先序

- **新頁約 9–11**（含 sims `lab_18`/`lab_19` + PLL budget + topology + 3 習題 + capstone）；深化既有頁約 4。
- 新 sim/圖約 4–5（Lorentzian、ADEV、PLL budget、cross-coupled ISF、HTM 示意）。
- 建議順序：**Tier 1（嚴格頂點，最有感）→ Tier 2（系統廣度）→ Tier 4 capstone/習題 → Tier 3（數學深化）**。
- 全程維持 build 綠燈、數學渲染驗證、quality 0 issue（沿用既有 `_AUTHORING_SPEC.md` + 安全 fixer）。

## 我的最推薦（若要先做一塊）
**Tier 1 全部（T1.1 Lorentzian + T1.2 嚴格頻譜 + T1.3 Allan）**——這三個是「研究所等級」最明顯的洞，
且彼此相關（都圍繞「相位 random walk 的頻域/時域後果」），做完整體質感會跳一級。
