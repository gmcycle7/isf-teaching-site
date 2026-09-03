---
title: 循序學習路徑 Learning Path
description: 十二步循序學習路徑（九步主幹＋三步進階），每步含目標、要讀的頁、先備、預期收穫與自我檢查點；快速路線約九步主幹、完整路線十二步全走。
---

import ProgressChecklist from "@site/src/components/ProgressChecklist";

# 循序學習路徑 Learning Path

這頁把首頁的九個步驟展開成一條**可以照著走**的學習路徑，並在主幹之後擴編三個
進階步（第 10–12 步），共 **12 步**。每一步告訴你：

- **要達成什麼**（這步的學習目標）；
- **讀哪幾頁**（按順序）；
- **先備**（沒有這個會卡住）；
- **預期收穫**（讀完應該能做什麼）。

最後給兩條路線：**快速路線**（約九步主幹，一個下午抓到 ISF 主幹）與**完整路線**
（十二步全走：每條公式自己重推一遍、每個 lab 自己跑一遍）。

> **怎麼用這頁**：第一次學請走「完整路線」，每讀完一步就回來打勾。回頭複習時走
> 「快速路線」即可。看到 `TODO:` 表示該處仍需人工對照原始 PDF；看到「toy model」
> 表示那是**教學用簡化模型，非 transistor-level**。

<ProgressChecklist items={[
  {id: "step-1", label: "第 1 步：振盪器的「相位」到底是什麼", href: "/02_foundations/oscillator_phase"},
  {id: "step-2", label: "第 2 步：noise 是小擾動，振盪器對它是 LTV 而非 LTI", href: "/02_foundations/lti_vs_ltv"},
  {id: "step-3", label: "第 3 步：ISF 的操作型定義（impulse → phase）", href: "/03_isf_core_theory/impulse_to_phase_shift"},
  {id: "step-4", label: "第 4 步：從單一 impulse 到任意 noise（卷積）", href: "/03_isf_core_theory/convolution_derivation"},
  {id: "step-5", label: "第 5 步：白噪 → 1/f²，flicker → 1/f³", href: "/03_isf_core_theory/white_noise_to_phase_noise"},
  {id: "step-6", label: "第 6 步：ISF 的傅立葉觀點（c₀、cₙ、upconversion）", href: "/03_isf_core_theory/fourier_series_of_isf"},
  {id: "step-7", label: "第 7 步：模擬 lab，建立數值手感", href: "/04_simulation_labs/numerical_feeling"},
  {id: "step-8", label: "第 8 步：設計 takeaways（symmetry、swing、slope）", href: "/06_design_insights/symmetry"},
  {id: "step-9", label: "第 9 步：接到 SerDes clocking（jitter、eye、PLL/CDR）", href: "/02_foundations/psd_phase_noise_jitter"},
  {id: "step-10", label: "第 10 步：進階理論——從 κ 到線形", href: "/03_isf_core_theory/diffusion_dictionary"},
  {id: "step-11", label: "第 11 步：注入鎖定與頻率轉換", href: "/05_paper_deep_dives/paper_003_injection_locking_part1"},
  {id: "step-12", label: "第 12 步：系統整合與量測", href: "/06_design_insights/clock_chain_budget"}
]} />

## 先把這三頁當「字典」

開始之前，先把這三頁放在手邊，遇到不懂的符號或論文出處隨時回查：

- [notation](/00_overview/notation) — 統一符號表（全站符號、單位、各論文對照）。
- [paper_summary_table](/01_paper_map/paper_summary_table) — 五篇論文一頁速覽（誰負責什麼）。
- [equation_index](/01_paper_map/equation_index) — 每條公式 → 推導頁 → 來源。

**隨手查**（不確定符號／公式／英文術語時，照下表跳頁；卡關時優先回這四頁）：

| 想查什麼 | 去哪頁 |
|---|---|
| 公式一頁打包、canonical 數值例 A/B/C | [速查表 Cheat Sheet](/00_overview/cheat_sheet) |
| 某個符號的意義與單位（如 $\Gamma_{rms}$、$q_{max}$、$c_0$） | [統一符號表 Notation](/00_overview/notation) |
| 某個英文術語的中文直覺（如 ISF、cyclostationary、limit cycle） | [中英對照詞彙表 Glossary](/99_appendix/glossary) |
| 某條公式出自哪篇論文哪個 Eq.、在哪頁推導 | [公式推導索引 Equation Index](/01_paper_map/equation_index) |

---

## 第 1 步：振盪器的「相位」到底是什麼 {#step-1}

- **要達成什麼**：建立 limit cycle（極限環，振盪器穩態走的閉合軌跡）的幾何圖像，
  分清楚**相位**（沿環的切向，無恢復力）與**振幅**（離環的徑向，有恢復力）。
- **讀哪幾頁**：[oscillator_phase](/02_foundations/oscillator_phase) →
  [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise)。
- **先備**：二維狀態空間、相平面、RLC 振盪的基本圖像。
- **預期收穫**：能解釋「為什麼擾動沿切向會永久留下、沿徑向會被拉回」，這正是
  claim **C2**（見 [claims_cross_reference](/01_paper_map/claims_cross_reference)）。

## 第 2 步：noise 是小擾動，振盪器對它是 LTV 而非 LTI {#step-2}

- **要達成什麼**：理解振盪器對 noise 是 **LTV（linear time-variant，線性時變）**——
  同一顆 impulse 在不同相位注入，造成的相位偏移**不同**；不像 LTI 系統只看 $t-\tau$。
- **讀哪幾頁**：[lti_vs_ltv](/02_foundations/lti_vs_ltv)。
- **先備**：第 1 步；線性系統、脈衝響應、卷積。
- **預期收穫**：能畫出 LTI 的 $h(t-\tau)$ 與 LTV 的 $h_\phi(t,\tau)$ 之差別，
  對應圖 `lti_vs_ltv_impulse_response.png`。這就是 claim **C1**。

## 第 3 步：ISF 的操作型定義（impulse → phase） {#step-3}

- **要達成什麼**：從電容 $q=Cv$ 一路推到 ISF 的操作型定義
  $\Delta\phi=\Gamma(\omega_0\tau)\,\Delta q/q_{max}$（[P1] Eq.(9)–(11), p.182），
  並理解 $\Gamma$ 為何無因次、為何 $2\pi$ 週期。
- **讀哪幾頁**：[impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) →
  [isf_definition](/03_isf_core_theory/isf_definition)。
- **先備**：第 1、2 步；電容關係、單位換算。
- **預期收穫**：能做 canonical 例 A 的口算——$q_{max}=1$ pC、$\Delta q=1$ fC、
  $\Gamma=0.5$、$f_0=5$ GHz 時 $\Delta\phi=5\times10^{-4}$ rad、$\Delta t=15.9$ fs。

## 第 4 步：從單一 impulse 到任意 noise（卷積） {#step-4}

- **要達成什麼**：用疊加把單一相位步階推廣成 LTV 卷積
  $\phi(t)=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau$
  （[P1] Eq.(11), p.182），看懂積分上限 $t$（記憶）為何造成相位**累積**。
- **讀哪幾頁**：[convolution_derivation](/03_isf_core_theory/convolution_derivation)。
- **先備**：第 3 步；卷積、積分。
- **預期收穫**：能解釋「相位是 noise 的積分器」，為第 5 步的 $1/f^2$ 斜率鋪路。

## 第 5 步：白噪 → $1/f^2$，flicker → $1/f^3$ {#step-5}

- **要達成什麼**：推出招牌結果 $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$
  （[P1] Eq.(21), p.185，claim **C3**），以及 flicker 只透過 ISF 的 DC 項 $c_0$
  上轉成 $1/f^3$（[P1] Eq.(23)(24), claim **C4/C5**）。
- **讀哪幾頁**：[white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) →
  [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)。
- **先備**：第 4 步；PSD、Parseval。
- **預期收穫**：能做 canonical 例 B——同一組數值用 Eq.(21) 算出 $\mathcal{L}=-148.0$
  dBc/Hz；並理解 spec 第 3 節提到的**著名 factor-of-2** SSB 記帳爭議。

## 第 6 步：ISF 的傅立葉觀點（$c_0$、$c_n$、upconversion） {#step-6}

- **要達成什麼**：把 ISF 展開成傅立葉級數 $\Gamma=\frac{c_0}{2}+\sum c_n\cos(n\omega_0\tau+\theta_n)$
  （[P1] Eq.(12), p.183），理解每個 $c_n$ 把 $n\omega_0$ 附近的 noise「降頻」搬到 carrier，
  以及 $\sum c_n^2=2\Gamma_{rms}^2$（Parseval，[P1] Eq.(20)）。
- **讀哪幾頁**：[fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) →
  [rms_isf](/03_isf_core_theory/rms_isf)。
- **先備**：第 5 步；傅立葉級數。
- **預期收穫**：能說出「對稱波形 → $c_0\approx0$ → 抑制 $1/f^3$」這個設計鐵則的數學根據
  （從拓樸參數直接算 $c_0$ 與 corner 的閉式版，見第 10 步的
  [asymmetric_isf_closed_form](/03_isf_core_theory/asymmetric_isf_closed_form)）。

## 第 7 步：模擬 lab，建立數值手感 {#step-7}

- **要達成什麼**：把前面的公式**親手跑一遍**、看圖、對數字，把 rad、fs、dBc/Hz、
  jitter 之間的換算練成反射。
- **讀哪幾頁**：先 [numerical_feeling](/04_simulation_labs/numerical_feeling)（三個必做口算），
  再依序 [lab_01](/04_simulation_labs/lab_01_sinusoidal_oscillator)、
  [lab_02](/04_simulation_labs/lab_02_lc_oscillator_toy_model)、
  [lab_04](/04_simulation_labs/lab_04_impulse_injection_sweep)、
  [lab_05](/04_simulation_labs/lab_05_isf_fourier_coefficients)、
  [lab_06](/04_simulation_labs/lab_06_white_noise_phase_noise)、
  [lab_07](/04_simulation_labs/lab_07_flicker_noise_upconversion)、
  [lab_08](/04_simulation_labs/lab_08_jitter_integration)。
- **先備**：第 3–6 步；一點 Python/NumPy。
- **預期收穫**：能用 `simulations/common/` 的函式一行驗證 canonical 例 A/B/C；
  每張圖都能追溯到 [figure_index](/01_paper_map/figure_index) 的 script 與公式。

## 第 8 步：設計 takeaways（symmetry、swing、slope） {#step-8}

- **要達成什麼**：把公式翻成**設計旋鈕**——拉大 $q_{max}$、壓低 $\Gamma_{rms}$、
  強制波形對稱以壓 $c_0$；並理解 ring 的 $\Gamma_{rms}\propto N^{-3/2}$ 與
  「固定功率/頻率下 ring phase noise 幾乎與級數 $N$ 無關」（claim **C7/C8**）。
- **讀哪幾頁**：[symmetry](/06_design_insights/symmetry) →
  [lc_vs_ring](/06_design_insights/lc_vs_ring)。
- **先備**：第 5、6 步。
- **預期收穫**：拿到一顆振盪器規格，能說出「先動哪個旋鈕」
  （「離理論天花板還有幾 dB」的定量版，見第 12 步的
  [fom_limit](/06_design_insights/fom_limit)）。

## 第 9 步：接到 SerDes clocking（jitter、eye、PLL/CDR） {#step-9}

- **要達成什麼**：把 phase noise 積分成 rms jitter，連到 SerDes 的 eye 閉合與 BER。
- **讀哪幾頁**：[psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) →
  [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)。
- **先備**：第 5、7 步（尤其 lab_08）。
- **預期收穫**：能做 canonical 例 C——$f_0=5$ GHz、$\mathcal{L}(1\text{MHz})=-100$
  dBc/Hz、$1/f^2$、積 1→100 MHz $\Rightarrow\sigma_\phi=14.07$ mrad、$\sigma_t=447.9$ fs，
  並知道積分被**下限**主導（period／cycle-to-cycle 的嚴格核推導見第 10 步的
  [jitter_kernels](/02_foundations/jitter_kernels)；RJ/DJ 分解與 TJ@BER 見第 12 步的
  [dj_dual_dirac](/06_design_insights/dj_dual_dirac)）。

---

## 第 10–12 步（進階）：從理論深水區到系統整合

主幹（第 1–9 步）建立的是**單顆自由振盪器**的 ISF 機器。接下來三步把同一台機器推向
三個方向：**更深的理論**（第 10 步）、**被注入的振盪器**（第 11 步）、**整個時脈系統**
（第 12 步）。原「進階（選修）」段落的內容已擴編併入：
[paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1) 與
[paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2) 在第 11 步；
[effective_isf](/03_isf_core_theory/effective_isf)（cyclostationary 修正
$\Gamma_{eff}=\Gamma\cdot\alpha$，claim **C9**，及 PPV/adjoint/Floquet 的**外部**數學基礎，
claim **C13**，**不在這 5 篇 PDF 內**，以標準文獻補充）維持選修，建議在進入第 10 步前補讀。

## 第 10 步：進階理論——從 κ 到線形 {#step-10}

- **要達成什麼**：把「白噪相位擴散只有一個自由參數」講到底——同一個相位方差成長率
  $\kappa^2$ 換五件衣服（$\kappa$、$D$、線寬、ADEV、$1/f^2$ 係數）；三種 jitter
  （TIE／N-period／cycle-to-cycle）的嚴格頻域核；flicker FM 之下線形何時不再是
  Lorentzian；$c_0$ 與 $1/f^3$ corner 的閉式；以及從波形直接把 $\Gamma$ 算出來的三種方法。
- **讀哪幾頁（每頁一句為什麼）**：
  1. [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)——$\kappa$、$D$、
     線寬、ADEV、$1/f^2$ 係數是**同一個數字的五件衣服**，先拿到換算字典
     （canonical $\kappa^2=0.125$ rad²/s）。
  2. [jitter_kernels](/02_foundations/jitter_kernels)——三種 jitter 是 $\phi$ 的
     0／1／2 階差分，前置常數與每一個 2 都從第一原理推出來。
  3. [beyond_lorentzian](/03_isf_core_theory/beyond_lorentzian)——flicker FM 把線形從
     Lorentzian 變成近高斯，並嚴格回答「儀器到底量什麼」。
  4. [asymmetric_isf_closed_form](/03_isf_core_theory/asymmetric_isf_closed_form)——
     [P2] App. B 閉式：從級數 $N$ 與不對稱度 $A$ 直接算 $\Gamma_{rms}$、$c_0$ 與
     $1/f^3$ corner。
  5. [isf_from_waveform](/03_isf_core_theory/isf_from_waveform)——[P1] 附錄三法
     （打脈衝／closed form／一階導數），知道每砍一刀近似會在哪裡失準。
- **先備**：第 5、6、9 步；外加
  [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) 與
  [allan_variance](/02_foundations/allan_variance)（diffusion_dictionary 的直接先備，
  沒讀過先補）。
- **預期收穫**：你能把任何 jitter 規格換算成任何其他表示，並知道每個近似的失效點。
- **自我檢查點**：
  - canonical 數值（$\Gamma_{rms}=0.5$、$q_{max}=1$ pC、$S_i=10^{-24}$ A²/Hz）下
    $\kappa^2=0.125$ rad²/s；換成真・理想 LC（$\Gamma_{rms}=1/\sqrt2$）為什麼恰好是
    2 倍（$0.25$ rad²/s）？
  - 在「單邊 $S_\phi$、$\int_0^\infty$」慣例下，period-jitter 核的前置常數是
    $1/\omega_0^2$；把單邊譜塞進文獻常見的 $2/\omega_0^2$ 版本，變異數會多算 2 倍
    （jitter 多 $\sqrt2$）——那個 2 屬於哪個記帳慣例？
  - 同一個 $\mathcal{L}(10\,\text{kHz})$ 規格：white FM 線寬 50 Hz、flicker FM 約
    3.1 kHz——為什麼單一 offset 的 dBc/Hz 數字完全不決定線寬？

## 第 11 步：注入鎖定與頻率轉換 {#step-11}

- **要達成什麼**：把同一個 $\Gamma$ 從 phase noise 延伸到「被注入」的世界——廣義 Adler
  方程、鎖內雜訊整形與鎖外 pulling、捕獲暫態與 cycle slip、M:N 次諧波鎖定與 ILFD、
  互注入（QVCO），最後到把 divider 踢出迴路的 sub-sampling PLL。
- **讀哪幾頁（每頁一句為什麼）**：
  1. [paper_003](/05_paper_deep_dives/paper_003_injection_locking_part1)——廣義 Adler：
     一條用 ISF 寫成的一階方程，對任意拓樸、任意注入波形給出 lock range（claim **C10**）。
  2. [injection_locking_noise](/06_design_insights/injection_locking_noise)——鎖定的
     振盪器就是一顆一階 PLL：自身雜訊高通（corner $\omega_c$）、參考低通；鎖不住時的
     單邊 pulling 梳。
  3. [lab_36](/04_simulation_labs/lab_36_lock_acquisition)——補上暫態拼圖：捕獲的精確
     閉式解、鎖定邊緣的臨界慢化、noise-induced cycle slip。
  4. [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)——APF
     （振幅版 ISF，claim **C11**）與 M:N 次諧波鎖定／ILFD。
  5. [injection_locked_division](/06_design_insights/injection_locked_division)——把 M:N 鎖定的
     ÷N 方向獨立成一頁：lock range 騎在 ISF 第 $N$ 諧波、半波對稱鎖不住 ÷2。
  6. [subharmonic_injection](/06_design_insights/subharmonic_injection)——對偶的另一半：倍頻靠
     注入波形自己的第 $N$ 諧波，realignment factor $\beta$ 與離散時間雜訊整形。
  7. [lab_40](/04_simulation_labs/lab_40_subharmonic_injection)——次諧波注入的獨立數值驗證：
     lock range $\propto1/N$、$\beta$ 的 ODE 步階響應、輸出 jitter 閉式。
  8. [quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators)
     ——互注入＝兩條 Adler：QVCO 的耦合強度↔相位誤差↔phase noise 三角權衡與那個
     $\sim3$ dB。
  9. [sampling_pll](/06_design_insights/sampling_pll)——取樣過零點＝取樣 ISF 最敏感處：
     sub-sampling 讓 divider 雜訊消失、CP 雜訊不再 $\times N^2$。
- **先備**：第 6、8 步；建議先補 [effective_isf](/03_isf_core_theory/effective_isf)
  （cyclostationary 修正，見本節開頭）。
- **預期收穫**：廣義 Adler 一路到 ILFD／QVCO／sub-sampling 的雜訊整形——注入相關的
  鎖定、拉扯與頻率轉換，你都能沿同一個 $\Gamma$ 講完。
- **自我檢查點**：
  - 正弦注入＋ideal-LC ISF 下，廣義 Adler 退化成
    $\dot\theta=\Delta\omega-\omega_L\sin\theta$、$\omega_L=I_{inj}/(2q_{max})$；鎖定內
    自身雜訊被高通整形，corner $\omega_c=\sqrt{\omega_L^2-\Delta\omega^2}$
    （[P3] Eq.(40) 的 pull-in 頻率）——為什麼鎖定**邊緣**的雜訊抑制會消失？
  - 鎖不住時拍頻 $\omega_b=\sqrt{\Delta\omega^2-\omega_L^2}$（[P4] Eq.(34)），sideband
    梳只長在一邊；canonical 數字（$f_L=5$ MHz、true-LC 雜訊）$r=0.8$ 時 cycle-slip 率
    $\sim10^{-1.86\times10^7}$——為什麼說 thermal slip 是「懸崖」不是「斜坡」？
  - M:N 次諧波鎖定 $\omega_L=I_{inj}\lvert\tilde\Gamma_N\rvert/2$（[P4] Eq.(28)–(30)）：
    ÷2 ILFD 騎在哪個諧波上？sub-sampling PLL 的 in-band 地板由 $-118.9$ 掉到
    $-126.0$ dBc/Hz（示意例）——divider 那一項去哪了？

## 第 12 步：系統整合與量測 {#step-12}

- **要達成什麼**：站上系統層收官——把單顆振盪器的 $\mathcal{L}(f)$ 沿時脈鏈記帳到每個
  節點、對照 FOM 理論天花板、懂參考源在買什麼、算 ADC 的 SNR/ENOB、把 RJ/DJ 分開記帳到
  TJ@BER、看懂量測圖與 spur、避開 12 個地雷，最後用 capstone 一條龍驗收全站。
- **讀哪幾頁（每頁一句為什麼）**：
  1. [clock_chain_budget](/06_design_insights/clock_chain_budget)——四條記帳規則
     （×N／÷N／PLL／buffer）＋一條 100 MHz→5 GHz→2.5 GHz 的完整 worked chain。
  2. [fom_limit](/06_design_insights/fom_limit)——FOM 天花板
     $=173.8-10\log_{10}(F_{eff})$ dB（300 K）：知道你的設計離物理極限幾 dB。
  3. [reference_oscillators](/06_design_insights/reference_oscillators)——crystal 就是
     $Q$ 高到誇張的 LC tank：為什麼鏈上沒有東西能補救 reference 的 close-in 雜訊。
  4. [adc_aperture_jitter](/06_design_insights/adc_aperture_jitter)——取樣誤差＝斜率×
     時間誤差：時脈品質直接決定資料轉換器的有效位元數。
  5. [dj_dual_dirac](/06_design_insights/dj_dual_dirac)——RJ 無界、DJ 有界：dual-Dirac
     與 TJ@BER 的業界標準記帳。
  6. [measurement_and_spurs](/06_design_insights/measurement_and_spurs)——量
     $\mathcal{L}(f)$ 的三種方法、spur 與隨機雜訊的分辨、怎麼讀一張真實 PN 圖。
  7. [common_mistakes](/06_design_insights/common_mistakes)——12 個真實地雷：整套
     factor-of-2 紀律的總複習。
  8. [capstone_lc_end_to_end](/03_isf_core_theory/capstone_lc_end_to_end)——全站主脊
     一條龍：state equations → ISF → 譜 → 線寬 → jitter → BER，收官。
- **先備**：第 7–9 步；第 10 步（jitter 核與擴散字典會被反覆引用）；第 11 步讀過更佳
  （sampling_pll 已在第 11 步出現）。
- **預期收穫**：能開出並守住一份時鐘雜訊預算——從參考源到取樣器，每一級的
  $\mathcal{L}(f)$ 與最終 jitter 都有出處。
- **自我檢查點**：
  - worked chain（100 MHz → ×50 PLL → 5 GHz → ÷2 → 2.5 GHz → buffer）最終積分
    jitter 27.6 fs；理想 ×N／÷N 下，以**秒**計的 $\sigma_t$ 為什麼一顆 fs 都不變？
  - canonical $\sigma_t=447.9$ fs 的時脈餵 5 GHz 輸入：$\text{SNR}_{jitter}=37.0$ dB、
    ENOB $=5.86$ bit；要 10 ENOB @ 5 GHz 得把 $\sigma_t$ 壓到 $\le25.4$ fs——用的是
    哪條公式？（$\text{SNR}=-20\log_{10}(2\pi f_{in}\sigma_t)$）
  - $\text{TJ}(\text{BER})=\text{DJ}_{\delta\delta}+2Q\cdot\sigma$、$Q(10^{-12})=7.03$：
    為什麼 $\text{DJ}_{\delta\delta}\le\text{DJ}_{pp}$ 是「故意低報」？spur 的單位為什麼
    是 dBc 而**不是** dBc/Hz？

---

## 兩條路線

### 快速路線（約一個下午，抓主幹）

對應**第 1–9 步的主幹**（第 10–12 步不在快速路線內）。目標是「看懂 ISF 是什麼、
它如何決定 phase noise」。**不**自己重推、**不**自己跑模擬：

1. [oscillator_phase](/02_foundations/oscillator_phase)（只看 limit cycle 與相位／振幅圖像）
2. [lti_vs_ltv](/02_foundations/lti_vs_ltv)（看 LTV 的核心結論與圖）
3. [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift)（記住操作型定義 + 例 A）
4. [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise)（記住 Eq.(21) 與例 B）
5. [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf)（$c_0$ 抑制 $1/f^3$ 的直覺）
6. [numerical_feeling](/04_simulation_labs/numerical_feeling)（三個口算）
7. [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection)（jitter 與 eye 的結論）

讀完你應能回答：什麼是 ISF、為何 LTV、$\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$、
對稱性為何重要、phase noise 怎麼變 jitter。

### 完整路線（每步自己重推 + 自己跑 lab）

照上面**第 1 步到第 12 步**順序，**每條公式蓋住答案自己重推一遍**，
**每個 lab 自己 `python scripts/run_all_sims.py` 跑一遍**對圖對數字
（第 10–12 步引用的進階 lab 也一樣照跑）。建議節奏：

| 階段 | 步驟 | 重點交付（自我檢核） |
|---|---|---|
| 幾何直覺 | 1–2 | 能畫 limit cycle、能說 LTV vs LTI 差別 |
| ISF 核心 | 3–6 | 能重推 Eq.(9)→(11)→(12)→(20)→(21)→(24) |
| 動手 | 7 | 能重現例 A/B/C 的數字，誤差量級對得上 |
| 設計 | 8–9 | 能列設計旋鈕、能把 $\mathcal{L}$ 積成 $\sigma_t$ |
| 進階理論 | 10 | 能在 $\kappa$、$D$、線寬、ADEV、$1/f^2$ 係數五種表示間任意換算、說出每個 2 的出處 |
| 注入與轉換 | 11 | 能從廣義 Adler 推出 $\omega_c$、$\omega_b$ 與 M:N 鎖定，說出 sub-sampling 贏在哪 |
| 系統整合 | 12 | 能把一條時脈鏈每級的 $\mathcal{L}(f)$ 記帳到底、開出並驗收 jitter 預算 |

## 重點回顧

- 十二步 = 九步主幹（相位幾何 → LTV → ISF 定義 → 卷積 → 白噪/flicker → 傅立葉 →
  lab → 設計 → SerDes）＋三步進階（第 10 步 κ 與線形 → 第 11 步注入鎖定與頻率轉換 →
  第 12 步系統整合與量測）。
- 隨手查四頁（卡關時優先回查）：[cheat_sheet](/00_overview/cheat_sheet)、
  [notation](/00_overview/notation)、[glossary](/99_appendix/glossary)、
  [equation_index](/01_paper_map/equation_index)（見本頁開頭「隨手查」表）。
- 快速路線抓九步主幹；完整路線十二步全走：重推每式、跑每個 lab。
- 第 10–12 步為進階：injection/APF 已編入第 11 步；PPV/adjoint 與多數系統整合頁的
  儀器／架構知識屬**外部文獻**（**不在 5 篇 PDF 內**），各頁均有誠實聲明。

## 延伸閱讀

- 五篇論文的分工：[paper_summary_table](/01_paper_map/paper_summary_table)
- 每張圖的來源：[figure_index](/01_paper_map/figure_index)
- 教學主張的交叉索引：[claims_cross_reference](/01_paper_map/claims_cross_reference)
- 為何來源含一篇 off-topic PDF：[build_report](/00_overview/build_report)
