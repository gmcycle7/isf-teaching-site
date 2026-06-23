export const meta = {
  name: 'isf-content-v3',
  description: 'Tier 1-4 deepening: Lorentzian, Allan, PLL budget, topologies, measurement, HTM, exercises, capstone.',
  phases: [{ title: 'Tier1' }, { title: 'Tier2' }, { title: 'Tier34' }],
}

const D = '/Users/matthuang/claude_code/ISF/isf-teaching-site'
const SPEC = `${D}/extracted/_AUTHORING_SPEC.md`
const RESULT = {
  type: 'object', additionalProperties: false,
  properties: { files_written: { type: 'array', items: { type: 'string' } }, todos: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } },
  required: ['files_written'],
}

const COMMON = `你是有 40 年經驗的類比電路 + 數學 + DSP/通訊大師，正在把 ISF 教學網站深化到「研究所等級」。

【先 Read】嚴格遵守：
- 作者規範（**特別是第 11 節 v3 深化增補**：新公式/新圖/新頁/深化規格）：${SPEC}
- 風格/深度範本（對齊其逐步推導、單位、數值、引用密度）：
  ${D}/docs/03_isf_core_theory/impulse_to_phase_shift.md、${D}/docs/03_isf_core_theory/white_noise_to_phase_noise.md、${D}/docs/99_appendix/derivation_floquet_ppv.md
- 結構化來源：${D}/extracted/extracted_equations.json
- 需要時讀對應 sim：${D}/simulations/lab_1x_*.py、common/*.py；論文純文字：/Users/matthuang/claude_code/ISF/extracted/raw_text/<name>.txt

【鐵則】
1. 繁體中文；英文術語第一次出現給中文直覺解釋。逐步推導、不跳步；每步說明物理/數學/近似/單位 + dimension check。
2. 公式 LaTeX 從規範第 3、10.2、11.2 節「逐字」複製，含來源引用（[P1]/[P2]/[P3]/[P4] Eq.(n) page，或外部 [E1]–[E4]）。不自己改常數。
3. **MDX/KaTeX 鐵則**：每個 $$ 顯示公式的 $$ 獨立成行（前後各一行只有 $$）；行內不等式用 > / <（**不要** &gt;/&lt;）；表格數學絕對值用 \\vert 或 \\lvert..\\rvert；每頁 front matter(title,description)+一個 H1；圖片 ![alt](/figures/xxx.png)；連結 [文字](/資料夾/檔名)；程式碼三反引號 python。
4. 每頁紮實（理論頁 ~200-350 行，含多段推導、表格、數值例、圖解讀）。toy/illustrative 要標明；外部文獻標「不在 5 篇 PDF 內」。
5. 用 Write/Edit 寫到指定絕對路徑。不要跑 npm/模擬。回傳 files_written/todos/notes。`

const editRule = `【深化既有頁】先 Read 完整檔，**保留所有既有內容**，只「插入」新段落（在合適位置），寫回完整檔；行數要增加。`

// Tier 1
const A1 = `${COMMON}\n${editRule}\n=== 你負責（Tier1，擁有這 2 檔）===
1) 新建 ${D}/docs/03_isf_core_theory/lorentzian_linewidth.md —「Lorentzian 線寬：解開 1/f² 在 Δf→0 發散的矛盾」。
   用規範 11.2 Lorentzian 全套逐步：相位擴散 Var[Δφ]=2D|t| → 載波自相關 ½cos(ω0τ)e^{-D|τ|}（用高斯特徵函數 E[e^{jΔφ}]=e^{-D|τ|}）→ Wiener-Khinchin → Lorentzian S∝D/(D²+Δω²) → 3-dB 線寬 D/π → 與 ISF 連結 D=Γrms²/(2qmax²)·(i²/Δf)。
   **核心教學點**：1/f² 是線性化近似、在 Δf→0 假發散；真實近載波轉平、總功率守恆。連 [E2] Demir 2000。嵌入 /figures/lorentzian_carrier_lineshape.png（先 Read lab_18_lorentzian.py 引用真實 code），附參數表/單位/如何解讀。給 canonical 數值（由 5 GHz、-100dBc/Hz@1MHz 反推 D 與線寬）。≥2 worked example。
2) 深化 ${D}/docs/03_isf_core_theory/white_noise_to_phase_noise.md：插入「## 嚴格頻譜推導（cyclostationary 自相關 → Wiener-Khinchin）」段——把現有 sum-of-tones 升級成嚴格版：寫 LTV 輸出的 time-averaged autocorrelation，用 ISF Fourier 係數展開，證明 Σcₙ²=2Γrms² 自然從自相關出來；末尾連到 lorentzian_linewidth（近載波 Lorentzian）。`

const A2 = `${COMMON}\n=== 你負責（Tier1，1 新頁）===
新建 ${D}/docs/02_foundations/allan_variance.md —「Allan variance：相位雜訊的時域對應」。
用規範 11.2 Allan 全套：兩樣本變異數定義 σy²(τ)=⟨½(ȳ_{k+1}-ȳ_k)²⟩、頻域積分 σy²=2∫S_y sin⁴(πfτ)/(πfτ)² df、S_y=(f²/f0²)S_φ。逐步推**五種雜訊的斜率對照表**（white PM τ⁻¹、flicker PM τ⁻¹、white FM τ⁻¹ᐟ²、flicker FM τ⁰ floor、RW FM τ^{+1/2}），各給「為何是這斜率」的直覺。為何時鐘界用 ADEV（普通頻率方差對 flicker/RW 不收斂）。嵌入 /figures/allan_deviation.png（先 Read lab_19_allan.py）。≥2 worked example（含由 L(f) 估 ADEV）。連 psd_phase_noise_jitter、serdes。外部文獻 Allan（IEEE/NIST 標準，標不在 5 篇內）。`

// Tier 2
const A3 = `${COMMON}\n=== 你負責（Tier2，1 新頁）===
新建 ${D}/docs/06_design_insights/pll_noise_budget.md —「PLL 完整相位雜訊預算與最佳 loop BW」。
逐步：五個雜訊源（reference、PFD/charge-pump、divider、loop filter、VCO）各自的 transfer 與加總 S_out=(S_ref N²+S_cp)|H_lp|²+S_vco|H_hp|²（H_lp/H_hp 見規範 10.2，type-II 2nd-order）。in-band（跟 ref/CP，被 N² 放大）vs out-of-band（跟 VCO）。reference spur 簡述。**最佳 loop BW**：對 ∫S_out df 求極小（太窄 VCO 漏出、太寬 ref/CP 漏出）。嵌入 /figures/pll_noise_budget.png（先 Read lab_20_pll_budget.py，實測 optimal fn≈6.9 MHz、σt≈259 fs）。≥2 worked example。連 serdes_clocking_connection、lab_13。PLL loop transfer 高階細節屬標準 PLL 文獻（標不在 5 篇內）。`

const A4 = `${COMMON}\n=== 你負責（Tier2，1 新頁）===
新建 ${D}/docs/06_design_insights/real_oscillator_topologies.md —「真實拓樸的 ISF：cross-coupled LC VCO、Colpitts、CMOS ring stage」。
手算層級（非 Spectre）。三段：
(a) **cross-coupled LC VCO**：differential tank ISF≈-sinθ（純 c1）；**tail current source 噪聲**的有效 ISF 富含 c0（flicker 上轉）與 c2（2ω0 折回）——因 tail 節點擺在 2ω0、switching 換流；故需波形對稱 + **tail filter 調在 2f0**（Hajimiri-Lee cyclostationary、Andreani tail-noise；標 illustrative）。嵌入 /figures/cross_coupled_vco_isf.png（先 Read lab_21_topology_isf.py，明標 illustrative）。
(b) **Colpitts**：為何 ISF 集中在窄相位窗（電流脈衝注入時刻），對應 [P1] Fig.5/6 的 Colpitts。
(c) **CMOS inverter ring stage**：由 switching transition 的斜率推 ISF 形狀（transition 時最敏感），連 lc_vs_ring 的三角 toy。
每段把 device noise → ISF 諧波 → close-in PN 做一條完整鏈（手算 + 量級）。≥2 worked example。`

const A5 = `${COMMON}\n=== 你負責（Tier2，1 新頁）===
新建 ${D}/docs/06_design_insights/measurement_and_spurs.md —「相位雜訊量測與 spur」。
(1) 量 L(f) 三法：spectrum analyzer 直接法（受 SA 自身相位雜訊限制）、PLL/delay-line frequency discriminator（去載波）、**cross-correlation**（兩條獨立通道相關、把不相關的儀器本底開根號降低）。各給原理、優缺點、適用範圍。
(2) **spur（確定性邊帶）vs 隨機相位雜訊**：spur 是離散 tone（單位 dBc，不是 /Hz），來自參考洩漏、電源漣波、注入；隨機 PN 是連續 /Hz。怎麼在頻譜上分辨、各自的成因與對策。
(3) **怎麼讀一張真實 PN 圖**：標出 1/f³、1/f²、floor 三段、各 corner、spur，並反推設計訊息。
無新圖（可重用 white_noise_phase_noise_psd / leeson_vs_isf 概念）。≥1 數值例（由圖讀數反推）。量測儀器/標準屬外部文獻（標不在 5 篇內）。`

// Tier 3-4
const A6 = `${COMMON}\n${editRule}\n=== 你負責（Tier34，擁有這 2 檔）===
1) 新建 ${D}/docs/99_appendix/ltv_htm.md —「嚴格 LTV 框架：Zadeh 時變傳函與 harmonic transfer matrix」。
   用規範 11.2 HTM：LTV y(t)=∫h(t,τ)x dτ；Zadeh H(f,t)；週期 LTV → 輸入頻率 f 成分被搬到 f+k f0、增益是 ISF 第 k 個傅立葉係數 c_k；**證明 ISF 就是相位輸出對各諧波的轉換向量**（連 [P1] Eq.(13) 與 fourier 頁的 frequency translation）。連讀者訊號與系統背景（卷積、LTI vs LTV）。屬數學深化、可引外部（Zadeh 1950；標不在 5 篇內）。
2) 深化 ${D}/docs/03_isf_core_theory/effective_isf.md：插入「## 從 device 熱雜訊推 NMF α(t)」段——transistor bias-dependent 熱雜訊（i²∝gm 或導通與否）→ 週期 gating α(t)∈[0,1] → Γ_eff=Γα；給 switching-pair worked example（α 為 2-per-period gate）算 Γeff 的 c0/c2 變化如何影響 1/f³。保留原內容只插入。`

const A7 = `${COMMON}\n=== 你負責（Tier4，1 新頁，capstone）===
新建 ${D}/docs/03_isf_core_theory/capstone_lc_end_to_end.md —「Capstone：一顆 ideal LC 從 state equations 到 BER（全嚴格一條龍）」。
把全站串成一條主脊，每步嚴格＋帶數值，當作「只讀一頁就懂整套」：
1. LC state equations（$\\dot v,\\dot i_L$）→ 線性化／Floquet（連 derivation_floquet_ppv）。
2. 推 $\\Gamma(\\theta)=-\\sin\\theta$（連 isf_definition）。
3. $\\Gamma_{rms}=1/\\sqrt2$（Parseval）。
4. 代 [P1] Eq.(21) 得 $S_\\phi/\\mathcal{L}(\\Delta\\omega)$（canonical 例 B，-148 dBc/Hz）。
5. **Lorentzian 線寬** $\\Delta f_{3dB}=\\Gamma_{rms}^2/(2\\pi q_{max}^2)\\cdot(i^2/\\Delta f)$（連 lorentzian_linewidth）。
6. 積分得 $\\sigma_t$（連 jitter 積分）。
7. $\\sigma_t$→BER bathtub（連 serdes）。
每步標來源頁與公式編號、給數值、做 dimension check。結尾一張「整套地圖」總表。`

const A8 = `${COMMON}\n=== 你負責（Tier4，3 新頁，習題＋完整解答）===
各章成套習題，每題：題目 → 完整逐步解（帶單位＋dimension check）→ 數值答案 → 一行 Python 驗證（引用 simulations/common/）。題型涵蓋推導題、數值題、設計反推題。
1) ${D}/docs/02_foundations/exercises.md（基礎章，6–8 題）：phase/jitter 換算、PSD/Parseval、LTI vs LTV、Allan 斜率判讀、Lorentzian 線寬估算。
2) ${D}/docs/03_isf_core_theory/exercises.md（核心理論章，6–8 題）：由 ISF 算 Γrms、c0→1/f³ corner、白噪→L、impulse→phase、Fourier 係數、effective ISF。
3) ${D}/docs/06_design_insights/exercises.md（設計章，6–8 題）：q_max/Γrms/對稱性 設計反推、ring vs LC 比較、PLL 最佳 BW、σt→BER、tail noise 對策。
每章末附「解答展開」（可用 details 區塊或直接列解）。`

log('v3 deepening fan-out: 8 agents, disjoint file ownership ...')
const jobs = [
  ['Tier1', 'lorentzian+spectral', A1], ['Tier1', 'allan', A2],
  ['Tier2', 'pll_budget', A3], ['Tier2', 'topologies', A4], ['Tier2', 'measurement', A5],
  ['Tier34', 'htm+cyclo', A6], ['Tier34', 'capstone', A7], ['Tier34', 'exercises', A8],
]
const results = await parallel(jobs.map(([phase, label, prompt]) => () =>
  agent(prompt, { label, phase, schema: RESULT, agentType: 'general-purpose' }).then(r => ({ label, r }))))
const ok = results.filter(Boolean)
let total = 0; const todos = []
for (const x of ok) { if (!x || !x.r) continue; const n = (x.r.files_written || []).length; total += n; log(`  [${x.label}] ${n} files`); for (const t of (x.r.todos || [])) todos.push(`[${x.label}] ${t}`) }
log(`Total files: ${total}; TODOs: ${todos.length}`)
return { agents: ok.length, total_files: total, todos, per_agent: ok.map(x => ({ label: x.label, files: (x.r.files_written || []).length, notes: x.r.notes })) }
