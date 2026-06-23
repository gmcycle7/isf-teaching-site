# ISF 教學網站 — 改善計劃 v1（數學深度 / 數值例題 / 模擬）

> 依據對全站 48 頁的量化 review。目標：把「引用結果式」升級為「逐步推導」、
> 把數值例題從集中在 5 頁擴散到每一頁、把模擬從 14 張基本機制圖擴充到涵蓋
> SerDes / PLL / cyclostationary / 非線性 / 設計掃描。

## 0. 現況快照（data-driven，2026-06）

| 指標 | 數量 | 觀察 |
|---|---|---|
| 頁數 / 總行數 | 48 / 9201 | 結構完整、build 綠燈、4616 個公式正確渲染 |
| 顯示公式 (display eq) | 246 | 分佈不均：white_noise 18、math_identities 20，但 device_noise_mapping 只有 2 |
| 數值例題行 | 117 | **集中**：psd 15、numerical_feeling 12、lab_08 11；但 fourier=0、lab_05=0、lc_vs_ring=0、device_noise_mapping=0 |
| 模擬腳本 / 圖 | 8 / 14 | 皆為基本機制；缺 SerDes/PLL/MC/cyclostationary/非線性/掃描 |

## 1. 三大缺口（已用原始碼確認）

**G1 數學不夠詳細**：推導常「引用 [P1] Eq.(n) 然後跳到結果」，中間代數省略。確認的具體跳步：
- `white_noise_to_phase_noise`：Eq.(16/17) 的 down-conversion 積分（$\int I_0\cos((n\omega_0\pm\Delta\omega)\tau)\cos(n\omega_0\tau+\theta_n)d\tau$ → product-to-sum → 只剩慢項 $\sin(\Delta\omega t)/\Delta\omega$）未展開；Eq.(18)→(19) 的「$I_0^2/2\to\overline{i_n^2}/\Delta f$、雙邊帶、對 $n$ 求和、factor 8 從哪來」一句帶過。
- `L\approx\tfrac12 S_\phi`：全站使用但未從 narrowband angle modulation（小角／Bessel $J_0,J_1$）推。
- `fourier_series_of_isf`：頻率搬移只給直覺，未明算 $\cos\!\cdot\!\cos$ 卷積。
- `psd_phase_noise_jitter`：period / cycle-to-cycle jitter 由 $S_\phi$ 換算的高通核 $|1-e^{-j2\pi fT}|^2$ 仍是 TODO。
- ring：$f_0=1/(2N\tau_D)$、$\Gamma_{rms}\propto N^{-3/2}$ 只引用未推。
- Floquet / adjoint / PPV 嚴格基礎只有一段；Leeson↔ISF 對照缺。

**G2 數值例題不夠多**：~20 頁只有 0–1 題。缺題的核心頁：fourier、isf_definition（可再加）、convolution、rms_isf（可再加）、effective_isf、lab_05、以及 06 章多數設計頁。

**G3 模擬不夠多**：缺 8 類有教學價值的模擬（見 C）。

## 2. 改善計劃（分波、可並行 workflow 執行）

### Wave A — 數學深度（P0）
- **A1 逐步展開 6 條關鍵推導**（在既有頁內插入「逐步代數」框，每步註明用到的恆等式與單位）：
  1. down-conversion 積分（white_noise / fourier）
  2. Eq.(18)→(19) factor-8 求和（white_noise）
  3. $L\approx\tfrac12 S_\phi$ 由小角 PM（psd_phase_noise_jitter）
  4. period / c2c / accumulated jitter 的三個權重核（psd_phase_noise_jitter，清 TODO）
  5. ring $f_0$ 與 $\Gamma_{rms}\propto N^{-3/2}$（lc_vs_ring / rms_isf）
  6. flicker 1/f³ corner Eq.(23)→(24) 的代數（flicker page）
- **A2 新增 2 個推導附錄頁**：
  - `99_appendix/derivation_floquet_ppv.md`：從 Floquet theory → 第一主向量 $v_1(t)$ → adjoint/PPV → 證明 ISF 是 PPV 的投影（明標外部文獻 Demir 2000、Kärtner）。
  - `99_appendix/derivation_leeson.md`：Leeson 模型推導，並與 ISF 結果逐項對照（$Q$、$F$、$1/f^3$ corner）。
- **A3 每條最終式加「來源＋每步用什麼」小框**，並更新 equation_index。

### Wave B — 數值例題（P0）
- **B1**：每個 03/06 頁補到 **≥2 worked examples**（不同數字、帶單位、帶 dimension check、附一行 Python 驗證）。具體題目：
  - isf_definition：算 $\Gamma$ 在 $\theta=0,\pi/4,\pi/2$ 的值與對應 $\Delta\phi$。
  - fourier：對給定 ISF 手算 $c_0,c_1,c_2$ 再用 `compute_fourier_coefficients` 對照。
  - rms_isf：算 $-\sin$ 的 $\Gamma_{rms}=0.707$、三角 ISF 的 $\Gamma_{rms}$、驗證 Parseval。
  - flicker：給 $c_0,c_1,\omega_{1/f}$ 算 1/f³ corner（兩組數字）。
  - effective_isf：給 duty/NMF 算 $\Gamma_{eff,rms}$ 與 PN 變化。
  - lc_vs_ring：給 $kT/P,\eta$ 算 ring $\mathcal{L}$；N=3/5/15 比較。
  - symmetry / waveform_slope / tank_swing / device_noise_mapping：各 1–2 題。
- **B2 新增例題庫頁** `04_simulation_labs/worked_examples.md`：~15 題分級（基礎換算 / ISF→PN / jitter 積分 / 設計反推），每題有解＋單位＋Python。
- **B3** 強化 `check_site_quality.py`：核心頁強制 ≥2 numeric example 行、≥1 dimension check。

### Wave C — 模擬（P1）：新增 8 個 lab + 圖
| 新 lab | 目的 | 模型 | 新圖 |
|---|---|---|---|
| lab_10 RF spectrum sidebands | phase noise → 實際 RF 頻譜裙帶（[P1] Fig.8） | 時域 PM → FFT | `rf_spectrum_phase_noise_sidebands.png` |
| lab_11 Monte-Carlo jitter | 時域抖動直方圖 ↔ 積分 phase noise（閉環驗證） | 多次 realization 統計 | `monte_carlo_jitter_histogram.png` |
| lab_12 SerDes eye + BER | jitter → eye 閉合 → BER bathtub | RJ 高斯 + 取樣 | `serdes_eye_ber_bathtub.png` |
| lab_13 PLL/CDR jitter transfer | loop BW 如何濾 VCO 相位雜訊 | VCO 高通 / CDR 低通 transfer | `pll_cdr_jitter_transfer.png` |
| lab_14 cyclostationary ISF | gated NMF $\alpha$ → $\Gamma_{eff}$ vs stationary | 週期 gating | `cyclostationary_effective_isf.png` |
| lab_15 nonlinear ISF | 強 van der Pol → ISF ≠ $-\sin$ | 大 $\mu$ 注入掃描 | `nonlinear_oscillator_isf.png` |
| lab_16 Leeson vs ISF | 兩模型疊圖（1/f³,1/f²,floor） | 公式疊圖 | `leeson_vs_isf_overlay.png` |
| lab_17 design sweep | PN/jitter vs $q_{max},\Gamma_{rms},N$ 設計曲線 | 參數掃描 | `design_tradeoff_sweeps.png` |
- 新增 `simulations/common/pll_utils.py`、`serdes_utils.py`；更新 `run_all_sims.py` 與 figure_index。

### Wave D — 跨頁／品質（P2）
- 互動式參數 widget（React/MDX）：拉桿調 $q_{max},\Gamma_{rms},\Delta f$ 即時看 $\mathcal{L}$ 與 $\sigma_t$（可選）。
- equation_index / figure_index 自動重建並納入新內容。

## 3. 執行方式與優先序
- **P0（先做，直接回應你的前兩個關切）**：Wave A1+A2、Wave B1+B2。
- **P1**：Wave C（8 個新模擬）。
- **P2**：Wave D。
- 執行採並行 workflow（如同先前 12-agent fan-out），每波結束跑 build + 數學渲染驗證 + quality check，維持綠燈。
- 全程遵守既有 `_AUTHORING_SPEC.md`（公式逐字、單位、引用、`$$` 圍欄獨立成行、表格內 `|`→`\vert`、數學內用 `>`/`<` 不用實體）。
