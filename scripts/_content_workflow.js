export const meta = {
  name: 'isf-content-fanout',
  description: 'Write all remaining ISF teaching MDX pages in parallel, per the authoring spec.',
  phases: [
    { title: 'Foundations' },
    { title: 'CoreTheory' },
    { title: 'Labs' },
    { title: 'DeepDives' },
    { title: 'DesignInsights' },
    { title: 'MapAndAppendix' },
  ],
}

const D = '/Users/matthuang/claude_code/ISF/isf-teaching-site'
const SPEC = `${D}/extracted/_AUTHORING_SPEC.md`

const RESULT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    files_written: { type: 'array', items: { type: 'string' } },
    todos: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['files_written'],
}

const COMMON = `你是一位有 40 年經驗的類比電路 + 數學 + DSP/通訊大師，正在撰寫一個 ISF
（Impulse Sensitivity Function）教學網站的頁面。

【先做這件事】用 Read 讀以下檔案，嚴格遵守它（公式、notation、引用、圖片路徑、MDX 規則一律照抄）：
- 作者規範（最重要）：${SPEC}
- 風格/深度範本（請模仿其逐步推導、單位、數值、引用密度）：
  ${D}/docs/03_isf_core_theory/impulse_to_phase_shift.md
  ${D}/docs/04_simulation_labs/numerical_feeling.md
  ${D}/docs/00_overview/notation.md
- 結構化來源資料（公式/figure/claim/論文 metadata）：
  ${D}/extracted/extracted_equations.json
  ${D}/extracted/paper_metadata.json
  ${D}/extracted/extracted_figures.json
  ${D}/extracted/extracted_claims.json
- 若需要論文原文敘述，可讀（純文字 dump，數學符號會缺，但敘述完整）：
  /Users/matthuang/claude_code/ISF/extracted/raw_text/<name>.txt
  （general / jitter_ring / BHongGenTheor-I / BHongGenTheor-II / Hajimiri_ISCS_98）

【鐵則】
1. 繁體中文撰寫；英文專業詞第一次出現給中文直覺解釋。
2. 每條重要公式逐步推導、不跳步；每步說明用到的物理/數學/近似/單位/dimension check。
3. 每個重要結果帶實際數字（用規範第 8 節的 canonical 數值，全站一致），帶單位。
4. 公式 LaTeX 一律從規範第 3 節「逐字」複製，含 [Px] Eq.(n) page 引用。不要自己改常數。
5. 不確定處寫 TODO；toy model 要標明非 transistor-level；外部文獻要標「不在 5 篇 PDF 內」。
6. 嚴格遵守 MDX/KaTeX 規則（規範第 6 節）：每頁要有 front matter (title, description) + 一個 H1；
   行內數學 $...$、獨立 $$...$$ 必須成對；散文不可有裸 { } 或 < 接字母（不等式寫成 $...$ 或用 &lt;）；
   圖片用 ![alt](/figures/xxx.png)；程式碼用 \`\`\`python fenced；mermaid 用 \`\`\`mermaid，節點文字放雙引號。
7. 連到其他頁用 [文字](/資料夾/檔名)（不含 docs/、不含 .md）。
8. 用 Write 工具把每個頁面寫到指定的「絕對路徑」。不要跑 npm 或模擬，只 Read 與 Write。
9. 內容要紮實、長度足夠（理論頁通常 ~150-300 行 MDX，含多段推導與表格），不要寫空殼或只列大綱。

完成後回傳 files_written（你實際寫出的絕對路徑清單）、todos（你標的 TODO 摘要）、notes。`

function p(title, body) {
  return `${COMMON}\n\n=== 你負責的頁面（${title}）===\n${body}`
}

// ---------------------------------------------------------------------------
// FOUNDATIONS
// ---------------------------------------------------------------------------
const G_found_A = p('Foundations A', `
寫這 3 頁（絕對路徑）：

1) ${D}/docs/02_foundations/oscillator_phase.md  —「Oscillator phase 是什麼？」
   必含：state trajectory；limit cycle 是什麼；為何振盪器沒有絕對時間基準；phase
   perturbation = 沿 limit cycle 的位移；amplitude perturbation = 徑向位移；為何 amplitude
   error 被 restoring 拉回、phase error 不會消失而累積成 phase noise/jitter；phase noise 與
   timing jitter 的關係。嵌入圖 /figures/limit_cycle_phase_amplitude.png 與
   /figures/waveform_with_impulse_markers.png，各附：對應公式、實際數字例子、Python 核心 code
   block（引用 simulations/lab_01_sinusoidal_oscillator.py 的真實函式，可先 Read 該檔）、完整
   script path、參數表、如何解讀。引用 [P1] Fig.4、Sec.III-A。

2) ${D}/docs/02_foundations/phase_vs_amplitude_noise.md
   為何相位雜訊重要、振幅雜訊通常被抑制；用 [P4] 的 APF（amplitude perturbation function，
   振幅敏感度，單位 1/A）與 amplitude decay function 說明振幅擾動會衰減（標 TODO 待查確切式）；
   ISF 與 APF 在 ideal LC 為 quadrature（[P4] Fig.3）。給 AM-PM 簡述。

3) ${D}/docs/02_foundations/lti_vs_ltv.md  —「LTI vs LTV」
   LTI: h(t-τ)；LTV: h(t,τ)；為何振盪器對 noise 的敏感度是週期時變；為何同樣 impulse 在不同
   波形位置注入得到不同 phase shift；ISF 本質是 periodically time-varying sensitivity。嵌入
   /figures/lti_vs_ltv_impulse_response.png 與 /figures/sinusoidal_impulse_phase_sweep.png。
   含一個小模擬說明（引用 lab_04）。引用 [P1] Eq.(10) 與 Sec.III。`)

const G_found_B = p('Foundations B', `
寫這 3 頁（絕對路徑）：

1) ${D}/docs/02_foundations/stochastic_noise_basics.md
   複習 white noise、flicker(1/f) noise、PSD、Parseval、autocorrelation、ergodicity、
   cyclostationary noise（週期穩態：noise 強度隨振盪相位週期變化，例如 transistor 只在導通時漏
   噪）。每個詞給中文直覺 + 單位。鋪陳後面 effective ISF。引用 [P1] cyclostationary 段落。

2) ${D}/docs/02_foundations/psd_phase_noise_jitter.md  —「phase noise → jitter」（重要）
   逐步推導：$\\Delta t=\\Delta\\phi/(2\\pi f_0)$；$\\sigma_\\phi^2=\\int_{f_1}^{f_2}S_\\phi df$；
   $\\sigma_t=\\sigma_\\phi/(2\\pi f_0)$；SSB 近似 $\\mathcal{L}(f)\\approx\\frac12 S_\\phi(f)$。解釋：
   為何 phase error 可轉 timing error；為何 phase PSD 積分得 variance；為何積分頻寬重要；
   dBc/Hz 如何轉 linear；random/period/cycle-to-cycle/accumulated jitter 差異（用 notation 頁的表）。
   嵌入 /figures/phase_noise_to_jitter_integration.png。用 canonical 例 C（5GHz, -100dBc/Hz → 447.9 fs）。

3) ${D}/docs/02_foundations/dsp_view_of_phase_noise.md
   用 DSP/訊號處理視角看：phase 是一個被「ISF 加權 + 積分器」處理的隨機過程；積分器 1/(jω)
   把白噪變 1/f²；Welch PSD 估計；取樣與 aliasing 注意事項；把 [P1] 的連續式對應到離散模擬
   （引用 lab_06）。嵌入 /figures/white_noise_phase_noise_psd.png 作為 DSP 驗證。`)

// ---------------------------------------------------------------------------
// CORE THEORY
// ---------------------------------------------------------------------------
const G_core_A = p('Core Theory A', `
寫這 2 頁（絕對路徑），深度要對齊範本 impulse_to_phase_shift.md：

1) ${D}/docs/03_isf_core_theory/isf_definition.md  —「ISF 定義」（核心）
   逐步：current impulse→charge displacement→state perturbation→投影到 phase direction→
   phase shift 與注入時間有關→定義 $\\Gamma(\\omega_0\\tau)$。清楚說明：$\\Gamma$ 無因次、週期、
   不是 noise 本身、是相位敏感度；不同 node/不同 noise source 有不同 ISF；large-signal periodic
   operating point 決定 ISF。給 ideal LC 推導 $\\Gamma(\\theta)=-\\sin\\theta$（用 [P1] Fig.4 直覺：
   peak 注入只改振幅、zero crossing 注入最大相位）。嵌入 /figures/lc_waveform_and_isf.png 與
   /figures/isf_impulse_sweep_sinusoidal.png。**做一個「各 paper ISF 定義比較表」**（[P1][P2] 用 Γ；
   [P3][P4] 在 injection 脈絡用同一 Γ；APF 是振幅版）。引用 [P1] Eq.(10),(11)。

2) ${D}/docs/03_isf_core_theory/convolution_derivation.md  —「convolution derivation」（核心）
   從單一 impulse response 推到任意 noise 電流 $i_n(t)$：目標
   $\\phi(t)=\\int_{-\\infty}^{t}[\\Gamma(\\omega_0\\tau)/q_{max}]i_n(\\tau)d\\tau$（[P1] Eq.(11)）。
   逐步：切成小 impulse→每個電荷 $i_n d\\tau$→每個造成小 phase step→step 對未來保持→累加所有過去
   →積分上限 t→這是 LTV 不是普通 LTI 卷積。畫 mermaid block diagram：
   i_n(t) → ×Γ(ω₀t)/q_max → ∫dt → φ(t)。給 Python numerical verification（用
   isf_utils.integrate_phase_from_noise，Read simulations/common/isf_utils.py 引用真實 code）。`)

const G_core_B = p('Core Theory B', `
寫這 2 頁（絕對路徑）：

1) ${D}/docs/03_isf_core_theory/fourier_series_of_isf.md  —「ISF Fourier series」（核心）
   推導 $\\Gamma(x)=c_0/2+\\sum c_n\\cos(nx+\\theta_n)$（[P1] Eq.(12)）。說明：為何可展成 Fourier；
   $c_0$ 物理意義（DC、控制 1/f upconversion）；$c_n$ 物理意義（把 $n\\omega_0$ 附近 device noise
   frequency-translate 到 carrier，[P1] Eq.(13),(16), Fig.8）；為何 flicker 透過 $c_0$/低階上轉成
   close-in phase noise；為何 waveform symmetry 降低某些係數；如何用數值積分算係數。給 Python：
   引用真實 isf_utils.compute_fourier_coefficients（Read 該檔）。嵌入
   /figures/isf_fourier_reconstruction.png、/figures/isf_fourier_coefficients.png、
   /figures/symmetric_vs_asymmetric_isf_c0.png。

2) ${D}/docs/03_isf_core_theory/rms_isf.md  —「rms ISF」
   推導 Parseval $\\sum_{n=0}^\\infty c_n^2=(1/\\pi)\\int_0^{2\\pi}|\\Gamma|^2dx=2\\Gamma_{rms}^2$
   （[P1] Eq.(20)）。解釋 $\\Gamma_{rms}$ 決定 1/f² phase noise（接 white_noise 頁）；說明 DC 項
   factor 的細節（$c_0/2$ 是 DC 值，注意 Parseval 中 DC 的 factor 慣例，給教學註記）。給 ring 的
   $\\Gamma_{rms}\\propto N^{-3/2}$（[P2] Eq.(16)，標 ⚠️ 常數待查）。嵌入
   /figures/isf_fourier_coefficients.png（驗證 $\\sum c_n^2=2\\Gamma_{rms}^2$）與
   /figures/lc_vs_ring_isf_comparison.png。`)

const G_core_C = p('Core Theory C', `
寫這 3 頁（絕對路徑），是設計直覺的關鍵：

1) ${D}/docs/03_isf_core_theory/white_noise_to_phase_noise.md  —（核心）
   推導 white current noise 經 ISF → 1/f² phase noise。含：$S_i$；ISF modulation；積分器把白噪變
   1/f²；$S_\\phi(f)$ 與 $\\mathcal{L}(\\Delta f)$ 關係；dBc/Hz 直覺。逐步導到 [P1] Eq.(19)→(20)→(21)。
   **務必寫清楚規範第 3 節的 factor-of-2 教學註記**（時域乾淨推導得 $/(2q^2\\Delta\\omega^2)$，[P1]
   Eq.(21) 是 $/(4)$，差 2 倍來自 SSB 記帳，不影響 scaling/斜率）。給 canonical 例 B（5GHz,1MHz,
   q_max=1pC,Γrms=0.5,S_i=1e-24 → 約 -148 dBc/Hz，逐步算、帶單位）。嵌入
   /figures/white_noise_phase_noise_psd.png。引用 lab_06。

2) ${D}/docs/03_isf_core_theory/flicker_noise_upconversion.md  —（核心）
   flicker noise 是什麼；為何 low-freq noise 被週期敏感度 upconvert；ISF 的 $c_0$/低階與 flicker
   upconversion 關係（[P1] Eq.(22),(23)）；1/f³ corner $\\Delta\\omega_{1/f^3}=\\omega_{1/f}c_0^2/(2\\Gamma_{rms}^2)$
   （[P1] Eq.(24)）並強調它 ≠ device 1/f corner；waveform symmetry 為何重要；differential/complementary
   波形對 flicker 的幫助與限制（[P2] symmetry, Fig.17）。嵌入
   /figures/flicker_upconversion_symmetric_vs_asymmetric.png、/figures/symmetric_vs_asymmetric_isf_c0.png。
   引用 lab_07、lab_05。

3) ${D}/docs/03_isf_core_theory/effective_isf.md
   cyclostationary noise → effective ISF $\\Gamma_{eff}(x)=\\Gamma(x)\\alpha(x)$（[P1] cyclostationary 段；
   $\\alpha$ = noise-modulating function，0..1 週期）。說明為何 device noise 被閘控、如何併入 ISF。
   並用一段補充「PPV / adjoint method / Floquet theory」：明確標註**不在這 5 篇 PDF**，屬 Demir 等
   外部文獻，給直覺（PPV 是 Floquet 第一主向量，adjoint 法可由模擬萃取 ISF），標 TODO 待人工補引用。`)

// ---------------------------------------------------------------------------
// LABS
// ---------------------------------------------------------------------------
const labRule = `每個 lab 頁必須有這 11 段：1.教學目標 2.數學模型 3.block diagram(mermaid)
4.Python 核心 code（**先 Read 對應 script 引用真實程式碼**）5.完整 script path 6.參數表 7.單位表
8.模擬圖(用 ![](/figures/xxx.png) 嵌入) 9.如何解讀圖 10.對應 paper 公式/figure 11.限制與 approximation。`

const G_labs_A = p('Labs A', `
${labRule}
寫這 3 頁（先 Read 對應 simulations/*.py）：
1) ${D}/docs/04_simulation_labs/lab_01_sinusoidal_oscillator.md
   script: simulations/lab_01_sinusoidal_oscillator.py；圖：limit_cycle_phase_amplitude.png、
   waveform_with_impulse_markers.png。目標：相位 vs 振幅擾動的幾何直覺。
2) ${D}/docs/04_simulation_labs/lab_02_lc_oscillator_toy_model.md
   script: simulations/lab_02_lc_toy_model.py；圖：lc_waveform_and_isf.png。模型假設：LC 用 2-D
   旋轉 state，$\\Gamma=-\\sin\\theta$，small-signal $\\Delta\\phi\\propto\\Delta q$。對應 [P1] Fig.4,6,7a。
3) ${D}/docs/04_simulation_labs/lab_03_ring_oscillator_toy_model.md
   script: simulations/lab_03_ring_toy_model.py；圖：ring_oscillator_timing_noise_accumulation.png、
   lc_vs_ring_isf_comparison.png。模型：N 級、每級 additive timing noise → 累積 jitter random walk
   $\\sigma_{\\Delta t}=\\kappa\\sqrt{\\Delta t}$（[P2] Eq.10）。說明 toy model 看得見/看不見什麼。`)

const G_labs_B = p('Labs B', `
${labRule}
寫這 2 頁（先 Read 對應 simulations/*.py）：
1) ${D}/docs/04_simulation_labs/lab_04_impulse_injection_sweep.md
   script: simulations/lab_04_impulse_sweep.py；圖：sinusoidal_impulse_phase_sweep.png、
   isf_impulse_sweep_sinusoidal.png、lti_vs_ltv_impulse_response.png。目標：數值掃描注入相位、
   反推 ISF，驗證 $\\Gamma=-\\sin\\theta$（誤差~0.001），並展示 LTV。對應 [P1] Eq.(10),(11),Fig.4。
2) ${D}/docs/04_simulation_labs/lab_05_isf_fourier_coefficients.md
   script: simulations/lab_05_fourier_isf.py；圖：isf_fourier_reconstruction.png、
   isf_fourier_coefficients.png、symmetric_vs_asymmetric_isf_c0.png。目標：算 $c_n$、Parseval 驗證
   $\\sum c_n^2=2\\Gamma_{rms}^2$、對稱 vs 不對稱 $c_0$。對應 [P1] Eq.(12),(20),(24)。`)

const G_labs_C = p('Labs C', `
${labRule}
寫這 4 頁（先 Read 對應 simulations/*.py）：
1) ${D}/docs/04_simulation_labs/lab_06_white_noise_phase_noise.md
   script: simulations/lab_06_white_noise_phase_noise.py；圖：white_noise_phase_noise_psd.png。
   目標：白噪→1/f²，模擬吻合理論 $S_\\phi=\\Gamma_{rms}^2 S_i/(q_{max}^2(2\\pi f)^2)$。提 factor-of-2 註記。
2) ${D}/docs/04_simulation_labs/lab_07_flicker_noise_upconversion.md
   script: simulations/lab_07_flicker_noise.py；圖：flicker_upconversion_symmetric_vs_asymmetric.png。
   目標：1/f 經對稱 vs 不對稱 ISF → close-in 1/f³ 抑制與否，顯示 PSD 斜率與 $c_0$ 影響。
3) ${D}/docs/04_simulation_labs/lab_08_jitter_integration.md
   script: simulations/lab_08_jitter_integration.py；圖：phase_noise_to_jitter_integration.png。
   目標：L(f)→rms jitter，數值=解析（447.9 fs）。對齊 numerical_feeling 例 C。
4) ${D}/docs/04_simulation_labs/lab_09_design_tradeoffs.md
   （無新圖，可重用 lc_vs_ring_isf_comparison.png 與 white_noise_phase_noise_psd.png）綜合 lab：
   掃 $q_{max}$、$\\Gamma_{rms}$、$N$ 對 phase noise/jitter 的影響（用公式做 scaling 表與口算，
   說明這是 toy scaling）。連到 design insights 各頁。`)

// ---------------------------------------------------------------------------
// DEEP DIVES
// ---------------------------------------------------------------------------
const ddRule = `每個 deep-dive 頁結構：H1=論文標題 → ## Citation → ## One-sentence contribution →
## Why this paper matters → ## Main assumptions → ## Key equations（每條：Original formula / Meaning /
Step-by-step derivation / Numerical example / Python verification 若適用）→ ## Key figures →
## Design insights → ## Limitations → ## Relationship to other papers → ## What to remember。
公式與引用照規範第 3 節與 paper_metadata.json。`

const G_dd = p('Deep Dives', `
${ddRule}
寫這 6 頁：
1) ${D}/docs/05_paper_deep_dives/index.md — 逐篇精讀導覽：列 5 篇、它們在課程中的角色、閱讀順序、
   並誠實說明 paper_005 與 ISF 無關。
2) ${D}/docs/05_paper_deep_dives/paper_001_general_theory_phase_noise.md — [P1]，最重要，
   涵蓋 Eq.(9)-(24) 的精華，連到各核心理論頁。
3) ${D}/docs/05_paper_deep_dives/paper_002_jitter_phase_noise_ring.md — [P2]，ring 的 jitter/phase
   noise、$\\Gamma_{rms}\\propto N^{-3/2}$、N-independence 結論（標 ⚠️ 常數待查）、symmetry/Fig.17。
4) ${D}/docs/05_paper_deep_dives/paper_003_injection_locking_part1.md — [P3]，ISF-based time-synchronous
   model、廣義 Adler 方程、lock range、injection waveform design（進階；公式標 TODO 待查確切式）。
5) ${D}/docs/05_paper_deep_dives/paper_004_injection_locking_part2.md — [P4]，APF（振幅版 ISF，單位
   1/A）、ISF/APF quadrature、amplitude modulation、ILFD/frequency division（進階；標 TODO）。
6) ${D}/docs/05_paper_deep_dives/paper_005_cross_coupled_sense_amp.md — [P5]，**誠實說明這是
   cross-coupled sense amplifier 論文、與 ISF/phase noise 無關**，唯一概念橋樑是 cross-coupled pair
   的 regeneration/正回授也是 latch/LC 振盪的基礎。不要假裝它跟 ISF 有關。`)

// ---------------------------------------------------------------------------
// DESIGN INSIGHTS
// ---------------------------------------------------------------------------
const G_design = p('Design Insights', `
寫這 6 頁（design 頁要把理論轉成 design intuition，不可只摘要）：
1) ${D}/docs/06_design_insights/symmetry.md — 為何 waveform symmetry 影響 flicker upconversion
   （$c_0$→1/f³ corner，[P1] Eq.(24)；[P2] Fig.17）。嵌入 symmetric_vs_asymmetric_isf_c0.png、
   flicker_upconversion_symmetric_vs_asymmetric.png。列降低 $c_0$ 的 design knobs。
2) ${D}/docs/06_design_insights/waveform_slope.md — 為何在 waveform slope 小的位置注入 noise 較危險
   （斜率小→該相位 |Γ| 大→相位敏感）；為何快 transition 有幫助。嵌入 lc_waveform_and_isf.png。
3) ${D}/docs/06_design_insights/tank_swing.md — 為何更大 swing 降低 phase sensitivity（$q_{max}$↑→
   phase noise ∝ $1/q_{max}^2$，[P1] Eq.(21)）；power/voltage headroom 取捨。
4) ${D}/docs/06_design_insights/device_noise_mapping.md — 把 transistor white/flicker noise 映到
   ISF harmonics 與 $c_0$/$\\Gamma_{rms}$；cyclostationary（effective ISF）；哪些 knobs 改 $\\Gamma_{rms}$、
   哪些改 $q_{max}$。
5) ${D}/docs/06_design_insights/lc_vs_ring.md — 從 ISF 比較 LC vs ring：波形、amplitude restoration、
   transition slope、tank energy、noisy device 數目、相位敏感度分佈、jitter accumulation、design knobs。
   建 toy model 假設（LC=sinusoidal state；ring=N 級 delay+timing noise），說明看得見/看不見什麼。
   給 [P2] Eq.(14) $f_0=1/(2N\\tau_D)$、$\\Gamma_{rms}\\propto N^{-3/2}$（⚠️）、FOM $\\frac{8}{3\\eta}\\frac{kT}{P}(\\omega_0/\\Delta\\omega)^2$（⚠️）、
   N-independence 結論。嵌入 lc_vs_ring_isf_comparison.png、ring_oscillator_timing_noise_accumulation.png。
6) ${D}/docs/06_design_insights/serdes_clocking_connection.md —（重點）必含：oscillator phase noise 如何
   變 clock jitter；clock jitter 如何影響 sampling uncertainty 與 eye opening；phase noise 積分頻寬如何選；
   RJ/DJ/accumulated jitter 差異；CDR/PLL 對 oscillator phase noise 的 filtering（high-pass on VCO noise）；
   TX PLL / RX PLL / LC-VCO / ring-VCO 實務直覺。逐步推導 $\\Delta t=\\Delta\\phi/(2\\pi f_0)$ 與
   $\\sigma_t=\\frac{1}{2\\pi f_0}\\sqrt{\\int_{f_1}^{f_2}S_\\phi(f)df}$。嵌入 phase_noise_to_jitter_integration.png。
   另外回答規範要求的 10 個 design 問題（symmetry/swing/slope/LC vs ring/ISF–jitter/積分換算/改 Γrms 的 knobs/
   改 q_max 的 knobs/降 white-noise phase noise/降 flicker close-in 的方法）——可分散在 06 各頁，但本頁要有總表連結。`)

// ---------------------------------------------------------------------------
// PAPER MAP + APPENDIX + learning_path
// ---------------------------------------------------------------------------
const G_map = p('Paper Map + learning_path', `
寫這 4 頁：
1) ${D}/docs/00_overview/learning_path.md — 詳細循序學習路徑（9 步，對應首頁），每步：要達成什麼、
   讀哪幾頁、先備、預期收穫；給「快速路線」與「完整路線」。
2) ${D}/docs/01_paper_map/paper_summary_table.md — 含表格
   | Paper | Year | Main Contribution | Key Equations | Key Figures | What We Use It For |
   （5 篇，資料取自 paper_metadata.json）。另用教學角度整理：哪篇是 ISF 核心基礎、哪篇延伸到 ring、
   哪篇關於 adjoint/PPV/PSS/PNoise/simulation（說明這 5 篇其實**沒有**專門 PPV/PSS 論文，PPV/adjoint
   屬外部文獻，誠實標註）、哪篇修正/批判/補充前人（[P1] 取代 Leeson 經驗式）、哪些公式在不同 paper 是
   同一件事不同寫法、哪些符號定義不同需統一（連到 notation 頁）。
3) ${D}/docs/01_paper_map/figure_index.md — 表格
   | Figure | Generated By (script/function) | Formula Behind It | Source | Teaching Message | Toy? | Redrawn? | Verify? |
   涵蓋 extracted_figures.json 的 14 張生成圖 + 引用的 PDF 圖。每張生成圖追溯 script path/function/params/公式/來源。
4) ${D}/docs/01_paper_map/claims_cross_reference.md — 表格列出 extracted_claims.json 的 C1..C13：
   | Claim | Source Paper | Confidence | Verify? | 哪幾頁用到 |。並標哪些是跨論文一致、哪些需人工確認。`)

const G_appendix = p('Appendix', `
寫這 4 頁：
1) ${D}/docs/99_appendix/math_identities.md — 本站用到的數學工具：傅立葉級數/Parseval、卷積與 LTV、
   隨機過程 PSD/Wiener-Khinchin、$10\\log_{10}$/dB 換算、積分器頻率響應 $1/(j\\omega)$、small-angle
   PM 近似、三角恆等式、random walk variance。每條給簡短證明或出處，並連到用到它的頁。
2) ${D}/docs/99_appendix/python_environment.md — 如何建環境（Python 3.12、numpy/scipy/matplotlib、
   CJK 字型 Heiti TC）、目錄結構（simulations/common 與各 lab）、如何跑 python scripts/run_all_sims.py、
   每個 common 模組與函式一覽（取自規範第 5 節）、reproducibility（固定 rng seed）。
3) ${D}/docs/99_appendix/glossary.md — 中英對照詞彙表（ISF, phase noise, timing jitter, phase/amplitude
   perturbation, LTV/LTI, cyclostationary, white/flicker noise, upconversion, rms/effective ISF, adjoint,
   PPV, Floquet, PSD, SSB phase noise, dBc/Hz, limit cycle, q_max, APF…），每個給一句中文直覺定義 + 出處頁連結。
4) ${D}/docs/99_appendix/references.md — 5 篇 PDF 完整引用（規範第 1 節 [P1]-[P5]）+ 外部補充文獻
   （Leeson 1966、Demir-Mehrotra-Roychowdhury 2000 PPV、Kaertner——標明**不在下載資料夾**，僅作背景）。
   說明引用慣例與 TODO（哪些 citation 需人工核對）。`)

// ---------------------------------------------------------------------------
// Run: fan out all groups in parallel, tagged by phase for display.
// ---------------------------------------------------------------------------
log('Fanning out ISF content pages across 12 writer agents ...')

const jobs = [
  ['Foundations', 'found_A', G_found_A],
  ['Foundations', 'found_B', G_found_B],
  ['CoreTheory', 'core_A', G_core_A],
  ['CoreTheory', 'core_B', G_core_B],
  ['CoreTheory', 'core_C', G_core_C],
  ['Labs', 'labs_A', G_labs_A],
  ['Labs', 'labs_B', G_labs_B],
  ['Labs', 'labs_C', G_labs_C],
  ['DeepDives', 'deep_dives', G_dd],
  ['DesignInsights', 'design', G_design],
  ['MapAndAppendix', 'paper_map', G_map],
  ['MapAndAppendix', 'appendix', G_appendix],
]

const results = await parallel(
  jobs.map(([phase, label, prompt]) => () =>
    agent(prompt, { label, phase, schema: RESULT_SCHEMA, agentType: 'general-purpose' })
      .then((r) => ({ label, r }))
  )
)

const ok = results.filter(Boolean)
let totalFiles = 0
const allTodos = []
for (const x of ok) {
  if (!x || !x.r) continue
  const n = (x.r.files_written || []).length
  totalFiles += n
  log(`  [${x.label}] wrote ${n} files`)
  for (const t of x.r.todos || []) allTodos.push(`[${x.label}] ${t}`)
}
log(`Total files written: ${totalFiles}; TODO items: ${allTodos.length}`)

return {
  agents: ok.length,
  total_files: totalFiles,
  todos: allTodos,
  per_agent: ok.map((x) => ({ label: x.label, files: (x.r.files_written || []).length, notes: x.r.notes })),
}
