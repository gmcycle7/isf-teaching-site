export const meta = {
  name: 'isf-content-v2',
  description: 'Wave A/B/C: expand derivations, add worked examples, write 8 new lab pages + 3 new pages.',
  phases: [
    { title: 'MathDepth' },
    { title: 'DesignExamples' },
    { title: 'NewPages' },
  ],
}

const D = '/Users/matthuang/claude_code/ISF/isf-teaching-site'
const SPEC = `${D}/extracted/_AUTHORING_SPEC.md`

const RESULT = {
  type: 'object', additionalProperties: false,
  properties: {
    files_written: { type: 'array', items: { type: 'string' } },
    todos: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['files_written'],
}

const COMMON = `你是有 40 年經驗的類比電路 + 數學 + DSP/通訊大師，正在「升級」一個 ISF 教學網站。

【先 Read 這些】嚴格遵守：
- 作者規範（含第 10 節 v2 增補：新圖/新公式/新頁/worked-example 規格/編輯鐵則）：${SPEC}
- 風格範本（深度對齊）：${D}/docs/03_isf_core_theory/impulse_to_phase_shift.md、${D}/docs/04_simulation_labs/numerical_feeling.md
- 結構化來源：${D}/extracted/extracted_equations.json、${D}/extracted/paper_metadata.json
- 需要時讀論文純文字：/Users/matthuang/claude_code/ISF/extracted/raw_text/<name>.txt

【鐵則】
1. 繁體中文；英文術語第一次出現給中文直覺解釋。
2. 公式 LaTeX 一律從規範第 3 節與第 10.2 節「逐字」複製，含 [Px] Eq.(n) page 引用；不自己改常數。
3. 推導要「逐步、不跳步」：每步說明用到的物理/數學/近似/單位，並做 dimension check。
4. **MDX/KaTeX 鐵則（違反會 build 失敗或亂碼）**：
   - 每個 $$ 顯示公式的 $$ 要「獨立成一行」（前後各一行只有 $$，內容不可跟 $$ 同一行）。
   - 行內不等式用 > 或 <（**絕對不要**用 &gt; / &lt;），且只放在 $...$ 內。
   - 表格 cell 內若數學含絕對值，用 \\vert 或 \\lvert..\\rvert，不要裸 |。
   - 每頁要有 front matter（title, description）+ 一個 H1。圖片用 ![alt](/figures/xxx.png)。
   - 連結用 [文字](/資料夾/檔名)（不含 docs/、不含 .md）。程式碼用三反引號 python fenced。
5. 不確定的常數/式子標 TODO；toy model 標明非 transistor-level；外部文獻標「不在 5 篇 PDF 內」。
6. 用 Write/Edit 寫到指定「絕對路徑」。不要跑 npm/模擬。完成回傳 files_written/todos/notes。`

// ---- Wave A + B: edit EXISTING pages (file ownership disjoint, no conflicts) ----
const editRule = `【編輯既有頁面】先 Read 完整檔案，**保留所有既有正確內容**，只「插入」：
(i) 在相關公式後插入「逐步代數」展開段；(ii) 在頁尾「重點回顧」前插入「## Worked examples 數值例題」段，
至少 2 題（題目→逐步代入帶單位→結果→dimension check→一行 Python 驗證，引用 simulations/common/）。
寫回完整檔案；**改寫後行數必須比原本多**（代表是擴充不是刪減）。`

const G1 = `${COMMON}\n\n${editRule}\n=== 你負責（MathDepth, 擁有這 2 檔）===
1) ${D}/docs/03_isf_core_theory/white_noise_to_phase_noise.md
   插入：規範 10.2 的「down-conversion 積分」逐步（積化和差、慢項存活、快項被積分器平均）、
   「factor-8 求和 (18)→(19)」逐步（$I_0^2/2\\to\\overline{i_n^2}/\\Delta f$、雙 sideband、對 n 求和）。
   Worked examples：例 B（5GHz,1MHz,q_max=1pC,Γrms=0.5,S_i=1e-24→約 -148 dBc/Hz，逐步）＋第二組數字。
2) ${D}/docs/03_isf_core_theory/fourier_series_of_isf.md
   插入：用 $\\cos A\\cos B$ 積化和差「明算」第 n 諧波把 $n\\omega_0$ 附近 noise 下轉到 carrier（頻率搬移的代數，不只直覺）。
   Worked examples：對給定 ISF 手算 $c_0,c_1,c_2$ 再用 compute_fourier_coefficients 對照（給數字）＋一題算某諧波貢獻。`

const G2 = `${COMMON}\n\n${editRule}\n=== 你負責（MathDepth, 擁有這 2 檔）===
1) ${D}/docs/02_foundations/psd_phase_noise_jitter.md
   插入：規範 10.2 的「$L\\approx\\tfrac12 S_\\phi$ 由小角 PM」完整推導（narrowband，sideband 功率 $(\\phi_p/2)^2$）；
   以及 period / cycle-to-cycle / accumulated jitter 的權重核（$\\lvert1-e^{-j2\\pi fT}\\rvert^2$、二階差分、低頻主導），清掉原本的 TODO；
   給一個 canonical 數值（period jitter 由 $S_\\phi$ 積分）。
   Worked examples：例 C（-100 dBc/Hz→447.9 fs）保留並逐步＋一題由 L 算 period jitter。
2) ${D}/docs/03_isf_core_theory/flicker_noise_upconversion.md
   插入：Eq.(22)→(23)→(24) 的代數（flicker 注入經 $c_0$、與 1/f² 機制相乘、解出 1/f³ corner $\\omega_{1/f^3}=\\omega_{1/f}c_0^2/(2\\Gamma_{rms}^2)$）。
   Worked examples：給 $c_0,c_1,\\omega_{1/f}$（兩組數字）算 1/f³ corner，並說明對稱性如何把它壓低。`

const G3 = `${COMMON}\n\n${editRule}\n=== 你負責（MathDepth, 擁有這 4 檔）===
1) ${D}/docs/03_isf_core_theory/rms_isf.md（已含 Parseval 推導，補強並加例）
   Worked examples：算 $-\\sin$ 的 $\\Gamma_{rms}=1/\\sqrt2\\approx0.707$；算一個三角 ISF 的 $\\Gamma_{rms}$；數值驗證 $\\sum c_n^2=2\\Gamma_{rms}^2$。
2) ${D}/docs/03_isf_core_theory/isf_definition.md
   Worked examples：算 $\\Gamma=-\\sin$ 在 $\\theta=0,\\pi/4,\\pi/2$ 的值與對應 $\\Delta\\phi$（給 $\\Delta q/q_{max}$）。
3) ${D}/docs/03_isf_core_theory/convolution_derivation.md
   插入：把離散疊加→積分的極限過程「逐步」寫清楚（小 impulse 電荷 $i_n d\\tau$、step 保持、積分上限 t）。
   Worked example：用 integrate_phase_from_noise 對一段已知 noise 數值積分得 $\\phi$，比對手算。
4) ${D}/docs/03_isf_core_theory/effective_isf.md
   Worked examples：給一個 duty/NMF $\\alpha$，算 $\\Gamma_{eff,rms}$ 與相對 stationary 的 PN 變化（示意數字，標 toy）。`

const G4 = `${COMMON}\n\n${editRule}\n=== 你負責（DesignExamples, 擁有這 6 檔，每檔加 ≥2 worked example）===
1) ${D}/docs/06_design_insights/symmetry.md — 例：給 $c_0,\\Gamma_{rms},\\omega_{1/f}$ 算 1/f³ corner 隨對稱改善而下降。
2) ${D}/docs/06_design_insights/waveform_slope.md — 例：在 slope 大/小處注入同一 $\\Delta q$，比較 $\\Delta\\phi$（用 $\\Gamma$ 值）。
3) ${D}/docs/06_design_insights/tank_swing.md — 例：$q_{max}$ 加倍→ $\\mathcal{L}$ 降 6 dB（用 Eq.21 逐步）。
4) ${D}/docs/06_design_insights/device_noise_mapping.md — 例：白噪／flicker 映到 $\\Gamma_{rms}$/$c_0$ 的兩個小算例；補幾條公式（此頁目前公式偏少）。
5) ${D}/docs/06_design_insights/lc_vs_ring.md — 插入 ring $f_0=1/(2N\\tau_D)$ 與 $\\Gamma_{rms}\\propto N^{-3/2}$ 的推導/scaling 說明；例：給 $kT/P,\\eta$ 算 ring $\\mathcal{L}$，N=3/5/15 比較（標 ⚠️ 常數待查）。
6) ${D}/docs/06_design_insights/serdes_clocking_connection.md — 例：由 $\\sigma_t$ 算 BER bathtub 開口（用 $Q$ 函數，UI=100ps）＋積分頻寬選擇的數值。`

// ---- New pages ----
const G5 = `${COMMON}\n\n=== 你負責（NewPages, 建立 2 個推導附錄頁）===
1) ${D}/docs/99_appendix/derivation_floquet_ppv.md — 標題「Floquet / adjoint / PPV：ISF 的嚴格基礎」。
   內容：週期系統的 Floquet theory → monodromy/Floquet 指數 → 第一主向量 $v_1(t)$（對應 0 指數的相位方向）→
   adjoint（伴隨）系統 → perturbation projection vector (PPV) → 證明 $\\dot\\phi=v_1^T(t)B(t)\\xi(t)$，並對應到 ISF $\\Gamma/q_{max}$。
   **明確標註：這些屬外部文獻（Demir–Mehrotra–Roychowdhury 2000 IEEE TCAS-I、Kärtner 1990），不在下載的 5 篇 PDF 內**；
   正式 citation 卷期/頁碼標 TODO。連到 isf_definition、effective_isf。
2) ${D}/docs/99_appendix/derivation_leeson.md — 標題「Leeson 模型推導與 ISF 對照」。
   內容：Leeson 出發點（tank 熱雜訊、feedback、$Q$）→ 規範 10.2 的 Leeson 式逐步 → 與 [P1] Eq.(21),(23),(24) 逐項對照
   （$Q$↔$\\Gamma_{rms}/q_{max}$、$F$ 經驗 vs ISF 物理、1/f³ corner）。嵌入 /figures/leeson_vs_isf_overlay.png（lab_16）。
   **標註 Leeson 1966 不在 5 篇 PDF 內**。`

const G6 = `${COMMON}\n\n=== 你負責（NewPages, 建立例題庫）===
建立 ${D}/docs/04_simulation_labs/worked_examples.md，標題「Worked Examples 例題庫」。
~15 題，分 4 級：(A) 基礎換算（rad↔fs、dBc↔linear）；(B) ISF→phase noise（Eq.21/23/24 代數）；
(C) jitter 積分（L→σ_t、period jitter）；(D) 設計反推（要 -120 dBc/Hz 需多大 q_max/Γrms；ring N 選擇）。
每題：**題目 → 逐步解（帶單位）→ 結果 → dimension check → 一行 Python 驗證（引用 simulations/common/）**。
數值沿用規範第 8 節 canonical 為主。頁尾附「自我檢查表」。連到 numerical_feeling 與相關理論頁。`

const labRule = `每個 lab 頁 11 段：1.教學目標 2.數學模型 3.block diagram(mermaid) 4.Python 核心 code（**先 Read 對應 script 引用真實程式碼**）
5.完整 script path 6.參數表 7.單位表 8.模擬圖 ![](/figures/xxx.png) 9.如何解讀圖 10.對應 paper 公式/figure 11.限制與 approximation。`

const G7 = `${COMMON}\n\n${labRule}\n=== 你負責（NewPages, 4 個新 lab 頁；先 Read 對應 simulations/*.py）===
1) ${D}/docs/04_simulation_labs/lab_10_rf_spectrum.md — script simulations/lab_10_rf_spectrum.py；圖 rf_spectrum_phase_noise_sidebands.png；目的：phase noise→RF 裙帶（[P1] Fig.8）。
2) ${D}/docs/04_simulation_labs/lab_11_monte_carlo_jitter.md — lab_11_monte_carlo_jitter.py；圖 monte_carlo_jitter_histogram.png；目的：RJ 高斯、$\\sigma=\\sigma_{edge}\\sqrt{\\Delta N}$（連 [P2] Eq.10）。
3) ${D}/docs/04_simulation_labs/lab_12_serdes_eye_ber.md — lab_12_serdes_eye_ber.py（用 serdes_utils）；圖 serdes_eye_ber_bathtub.png；目的：jitter→eye→BER（規範 10.2 BER 式）。
4) ${D}/docs/04_simulation_labs/lab_13_pll_cdr_transfer.md — lab_13_pll_cdr_transfer.py（用 pll_utils）；圖 pll_cdr_jitter_transfer.png；目的：PLL/CDR 對 VCO/ref 的高通/低通整形。`

const G8 = `${COMMON}\n\n${labRule}\n=== 你負責（NewPages, 4 個新 lab 頁；先 Read 對應 simulations/*.py）===
1) ${D}/docs/04_simulation_labs/lab_14_cyclostationary_isf.md — lab_14_cyclostationary_isf.py；圖 cyclostationary_effective_isf.png；目的：$\\Gamma_{eff}=\\Gamma\\alpha$、注入相位決定 rms。
2) ${D}/docs/04_simulation_labs/lab_15_nonlinear_isf.md — lab_15_nonlinear_isf.py；圖 nonlinear_oscillator_isf.png；目的：van der Pol，ISF 隨大訊號波形改變、非恆 $-\\sin$。
3) ${D}/docs/04_simulation_labs/lab_16_leeson_vs_isf.md — lab_16_leeson_vs_isf.py；圖 leeson_vs_isf_overlay.png；目的：Leeson↔ISF 三段對照（標 Leeson 為外部文獻）。
4) ${D}/docs/04_simulation_labs/lab_17_design_tradeoffs.md — lab_17_design_sweep.py；圖 design_tradeoff_sweeps.png；目的：swing/Γrms/N 設計曲線（連 lab_09 與 06 章）。
   注意：此頁檔名是 lab_17_design_tradeoffs.md（對應既有 sidebar 命名慣例），但 script 是 lab_17_design_sweep.py。`

log('Wave A/B/C content fan-out: 8 agents, disjoint file ownership ...')
const jobs = [
  ['MathDepth', 'core_math_A', G1],
  ['MathDepth', 'core_math_B', G2],
  ['MathDepth', 'core_math_C', G3],
  ['DesignExamples', 'design_examples', G4],
  ['NewPages', 'appendix_derivations', G5],
  ['NewPages', 'examples_bank', G6],
  ['NewPages', 'lab_pages_1', G7],
  ['NewPages', 'lab_pages_2', G8],
]
const results = await parallel(jobs.map(([phase, label, prompt]) => () =>
  agent(prompt, { label, phase, schema: RESULT, agentType: 'general-purpose' })
    .then(r => ({ label, r }))))

const ok = results.filter(Boolean)
let total = 0; const todos = []
for (const x of ok) {
  if (!x || !x.r) continue
  const n = (x.r.files_written || []).length
  total += n
  log(`  [${x.label}] ${n} files`)
  for (const t of (x.r.todos || [])) todos.push(`[${x.label}] ${t}`)
}
log(`Total files: ${total}; TODOs: ${todos.length}`)
return { agents: ok.length, total_files: total, todos,
  per_agent: ok.map(x => ({ label: x.label, files: (x.r.files_written || []).length, notes: x.r.notes })) }
