---
title: 教學主張交叉索引 Claims Cross-Reference
description: C1–C13 教學主張的來源論文、信心、是否需人工確認、與用在哪幾頁；並標跨論文一致與需確認者。
---

# 教學主張交叉索引 Claims Cross-Reference

本站每一個關鍵教學主張（claim）都編號 **C1–C13**，並標明：出自哪篇論文、信心多高、
是否需要人工對照 PDF（`Verify?`）、以及**哪幾頁**用到它。資料取自
`extracted/extracted_claims.json`。

> **怎麼用這頁**：寫頁面或複習時，先看一個結論屬於哪個 C 編號，就能一路追到來源論文與
> 信心等級。**信心**分三級：`high (read from text)` / `high (equation verified)` /
> `medium`。`Verify?` 標 ⚠️ 者表示 `manual_verification_needed = true`，常數或確切形式
> 仍需人工對照原始 PDF。

## C1–C13 一覽

| Claim | Source Paper | Confidence | Verify? | 哪幾頁用到 |
|---|---|---|---|---|
| **C1** 所有振盪器對 noise 是 **LTV** 而非 LTI：同一 impulse 在週期不同時刻注入，造成的相位偏移不同。 | [P1] (paper_001) Sec. III | high (read from text) | No | [lti_vs_ltv](/02_foundations/lti_vs_ltv)、[isf_definition](/03_isf_core_theory/isf_definition)、[lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep) |
| **C2** 振幅擾動會被拉回 limit cycle（穩定振盪需恢復機制），但**相位**擾動永久殘留並累積。 | [P1] Sec. III-A；[P4] (APF/衰減函數) | high | No | [oscillator_phase](/02_foundations/oscillator_phase)、[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)、[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) |
| **C3** phase noise $\propto\Gamma_{rms}^2/q_{max}^2$：拉大訊號電荷擺幅 $q_{max}$、壓低 rms ISF 以降 $1/f^2$ phase noise。 | [P1] Eq.(21) | high (equation verified) | No | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)、[rms_isf](/03_isf_core_theory/rms_isf)、[lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise)、[lc_vs_ring](/06_design_insights/lc_vs_ring) |
| **C4** $1/f$ device noise **只**透過 ISF 的 DC 項 $c_0$ 上轉成 close-in $1/f^3$；rise/fall 對稱（小 $c_0$）→ 低 $1/f^3$。 | [P1] Eqs (23),(24)；[P2] 對稱性節與 Fig. 17 | high | No | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)、[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)、[symmetry](/06_design_insights/symmetry)、[lab_07](/04_simulation_labs/lab_07_flicker_noise_upconversion) |
| **C5** $1/f^3$ corner **不等於** device 的 $1/f$ corner：$\Delta\omega_{1/f^3}=\omega_{1/f}\,c_0^2/(2\Gamma_{rms}^2)$，故對稱性可把它壓到 device corner 以下。 | [P1] Eq.(24) | high (equation verified) | No | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)、[symmetry](/06_design_insights/symmetry)、[equation_index](/01_paper_map/equation_index) |
| **C6** 自由振盪器累積 jitter 隨量測區間開根號成長 $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$——無絕對時間參考的隨機漫步特徵。 | [P2] (paper_002) Eq.(8), p.792 | high | No | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter)、[lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model)、[serdes_clocking_connection](/06_design_insights/serdes_clocking_connection) |
| **C7** 固定中心頻率與功率耗損下，單端 ring 的 phase noise／jitter 基本上**與級數 $N$ 無關**。 | [P2] Sec. V, Eq.(23)/(25), p.796 | high (equation verified)（$N$ 無關已核實；唯 FOM 前置係數 $8/(3\eta)$ 屬細節） | No | [lc_vs_ring](/06_design_insights/lc_vs_ring)、[lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| **C8** 單端 ring 的 rms ISF 約 $\Gamma_{rms}\propto N^{-3/4}$。 | [P2] Eq.(16), p.794 | high (equation verified) | No | [rms_isf](/03_isf_core_theory/rms_isf)、[lc_vs_ring](/06_design_insights/lc_vs_ring)、[lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| **C9** ISF 框架把既有 phase-noise 模型（如 Leeson）納為特例，並透過 effective ISF $\Gamma_{eff}=\Gamma\cdot\alpha$ 自然容納 cyclostationary noise。 | [P1] Abstract 與 cyclostationary 節 | high | No | [effective_isf](/03_isf_core_theory/effective_isf)、[paper_summary_table](/01_paper_map/paper_summary_table)、[equation_index](/01_paper_map/equation_index) |
| **C10** 決定 phase noise 的同一個 ISF 也決定 injection locking/pulling；單一一階（廣義 Adler）方程預測 lock range、locked phase、穩定性。 | [P3] (Hong Part I, 2019) Eq.(30), p.2113／Eq.(35), p.2114 | high (equation verified) | No | [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1)、[equation_index](/01_paper_map/equation_index) |
| **C11** 注入下的振幅效應由 **APF**（amplitude perturbation function，ISF 的振幅版類比，單位 $\mathrm{A^{-1}}$）描述；理想 LC 中 ISF 與 APF **正交**。 | [P4] (Hong Part II, 2019) Fig.5, p.2126；正交性 Eq.(26), p.2128 | high (equation verified) | No | [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2)、[phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) |
| **C12** cross-coupled-inverter sense amplifier 論文**與 ISF／phase noise 無關**；唯一概念連結是與 latch/LC 共通的 cross-coupled-pair regeneration／正回授機制。 | [P5] (Hajimiri–Heald, ISCAS 1998) | high（依標題/摘要明顯離題） | No | [paper_005_sense_amplifier](/05_paper_deep_dives/paper_005_cross_coupled_sense_amp)、[paper_summary_table](/01_paper_map/paper_summary_table)、[build_report](/00_overview/build_report) |
| **C13** PPV／adjoint／Floquet 是 ISF 嚴謹的數學基礎，出自更廣文獻（Demir 2000 DOI 10.1109/81.847872、Kärtner 1990 DOI 10.1002/cta.4490180505），**不在這 5 篇 PDF 內**；citation 卷期/頁碼/DOI 已查證。 | external（**不在來源資料夾**） | high（sourcing 聲明） | ✓ citation | [effective_isf](/03_isf_core_theory/effective_isf)、[equation_index](/01_paper_map/equation_index)、[references](/99_appendix/references) |

## 跨論文一致的主張（互相印證，信心高）

這些 claim **不只一篇支持**，或在不同論文以不同形式重現，彼此印證：

- **C2（相位殘留／振幅衰減）**：[P1] 從 limit cycle 論述「相位無恢復力」；[P4] 用
  **APF 與振幅衰減函數**從振幅側佐證「振幅擾動會被拉回」。同一物理，兩個角度。
- **C3 ↔ C6（$\Gamma_{rms}^2/q_{max}^2$）**：[P1] Eq.(21) 的 phase noise 與 [P2] 的
  jitter 比例常數 $\kappa^2$ **共用同一個 $\Gamma_{rms}^2/q_{max}^2$ 比例**——phase noise
  與累積 jitter 是同一物理在頻域／時域的兩面。
- **C4/C5（對稱性壓 $1/f^3$）**：[P1] 由 Eq.(23)(24) **理論導出**；[P2] 的 Fig. 17
  **量測佐證**（phase noise 在對稱控制電壓處最小）。理論 + 實驗雙重支持。
- **C1（LTV）與 C10（injection）**：同一個 $\Gamma$ 既決定 noise→phase（[P1]），
  也決定 injection→phase（[P3]）；LTV 觀點貫穿兩篇。

## 需要人工確認的主張（標 ⚠️）

下列 claim 的**敘述方向可信**，但**確切常數／方程形式**仍應對照原始 PDF；本站在用到之處
一律保留 `TODO:` 字樣：

- **C7**：「ring phase noise 與 $N$ 無關」此結論成立於**固定功率、固定頻率**與特定 noise
  模型下，已對照 [P2] Sec. V、Eq.(23)/(25)、p.796 核實。FOM 前置係數為
  $\frac{8}{3\eta}\,\frac{V_{DD}}{V_{char}}\,\frac{kT}{P}$（$\eta$ 為級延遲比例常數 Eq.(14)，$\approx1$；$\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入）。
  唯一仍需逐字確認者僅此前置係數本身；$N$ 無關的結論已穩固核實。
- **C8**：$\Gamma_{rms}\propto N^{-3/4}$ 的 scaling 與前置係數均已核實：[P2] Eq.(16), p.794 給出
  $\Gamma_{rms}=\sqrt{\dfrac{2\pi^2}{3\eta^3}}\,N^{-3/4}$（$\eta\approx1$）。已對照原始 PDF 核實。
- **C10**：廣義 Adler 方程已對照 [P3] 核實：時間平均式 $d\theta/dt=\omega_0-\omega_{inj}+\frac{1}{T_{inj}}\int\tilde\Gamma(\omega_{inj}t+\theta)\,i_{inj}\,dt$ = Eq.(30), p.2113（原文為 **加號**），鎖定範圍 $\omega_L=\tfrac12 I_{inj}\vert\tilde\Gamma_1\vert$ = Eq.(35), p.2114。
  （若站內某些頁面平均項前寫 **減號**，係本站 $\Gamma$ 取與 [P3] 相反的符號慣例，數值等價。）
- **C11**：APF 已對照 [P4] 核實：分解 $D(\tau,\phi)=\tilde\Lambda(\phi)\,d(\tau,\phi)$ = Eq.(18)、定義 $\Delta(\phi):=\int_0^\infty D\,d\tau$（單位 $\mathrm{A^{-1}}$）= Eq.(19)，皆於 p.2126；ISF／APF 正交於理想 LC = Eq.(26), p.2128。
- **C13**：這是 **sourcing 聲明**本身——重點是誠實標明 PPV/adjoint/Floquet 屬**外部文獻**，
  **不在 5 篇 PDF 內**；citation 卷期/頁碼/DOI 已用網路查證（見 references [E2]–[E4]）。

> **信心 vs Verify 的差別**：`high (equation verified)`（如 C3、C5、以及 v3 已逐字核實的
> C7／C8／C10／C11）表示公式 LaTeX 已對照渲染頁與原始 PDF。C13 標 ✓ citation，是提醒
> 「外部引用需自行查證」，並非站內敘述有誤。

## 重點回顧

- 13 個教學主張全部建檔到來源論文與信心等級；C1–C12 信心高（C7/C8/C10/C11 已於 v3 逐字核實），僅 C13 標 ✓ citation（外部文獻自行查證）。
- **跨論文一致**：C2（[P1]+[P4]）、C3↔C6（[P1]+[P2] 同比例）、C4/C5（[P1] 理論 + [P2] 量測）。
- **已逐字核實**：ring 的常數（C7/C8，[P2] Eq.(16)/(23)）、injection/APF 形式（C10 [P3] Eq.(30)/(35)、C11 [P4] Eq.(18)/(19)/(26)）；外部文獻 sourcing（C13）需自行查證。
- PPV/adjoint/Floquet（C13）**不在 5 篇 PDF 內**——屬外部文獻，誠實標註。

## 延伸閱讀

- 論文分工與「沒有專屬 PPV/PSS 論文」說明：[paper_summary_table](/01_paper_map/paper_summary_table)
- 公式 → 推導頁 → 來源：[equation_index](/01_paper_map/equation_index)
- 每張圖的來源與 toy 標記：[figure_index](/01_paper_map/figure_index)
- 外部文獻（Demir、Leeson、Adler）：[references](/99_appendix/references)
