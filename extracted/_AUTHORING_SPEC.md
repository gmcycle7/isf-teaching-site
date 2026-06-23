# ISF 教學網站 — AUTHORING SPEC（作者規範，所有頁面共用）

> 這個檔案不是網站頁面（不在 `docs/` 下，不會被 build）。它是所有撰寫者
> （包含人類與 subagent）必須遵守的「單一事實來源」。**公式、notation、引用字串、
> 圖片路徑一律照本檔抄，不要自行發明或改寫常數。** 不確定的地方標 `TODO:`。

---

## 0. 任務與讀者

- **主題**：oscillator phase noise / jitter 理論中的 **Impulse Sensitivity Function (ISF)**。
- **讀者**：電機系大學畢業生，懂電路學、電子學、訊號與系統、隨機程序、傅立葉、基本 DSP；
  但**尚未**掌握 phase noise、jitter、ISF、cyclostationary noise、LTV oscillator model。
- **作者身份/語氣**：40 年經驗的類比電路 + 數學 + DSP/通訊大師。非常清楚、非常細、
  有物理直覺。**逐步推導，不跳步**。
- **語言**：繁體中文為主，保留必要英文專業詞。**每個英文術語第一次出現給中文直覺解釋**，
  例如：「phase noise（相位雜訊，振盪訊號相位的隨機抖動）」。
- **不要**只摘要論文。要「教學」：推導、物理意義、單位、適用/失效條件、數值手感。

---

## 1. 五篇論文與標準引用字串（請逐字使用）

- **[P1]** A. Hajimiri and T. H. Lee, *"A General Theory of Phase Noise in Electrical
  Oscillators,"* IEEE J. Solid-State Circuits, vol. 33, no. 2, pp. 179–194, Feb. 1998.
  （檔案 `general.pdf`，paper_001，**ISF 核心基礎**）
- **[P2]** A. Hajimiri, S. Limotyrakis, and T. H. Lee, *"Jitter and Phase Noise in Ring
  Oscillators,"* IEEE J. Solid-State Circuits, vol. 34, no. 6, pp. 790–804, Jun. 1999.
  （`jitter_ring.pdf`，paper_002，**ring oscillator 延伸**）
- **[P3]** B. Hong and A. Hajimiri, *"A General Theory of Injection Locking and Pulling in
  Electrical Oscillators—Part I: Time-Synchronous Modeling and Injection Waveform Design,"*
  IEEE J. Solid-State Circuits, vol. 54, no. 8, pp. 2109–2121, Aug. 2019.
  （`BHongGenTheor-I_JSSC2019_Postprint.pdf`，paper_003，**injection locking，進階**）
- **[P4]** B. Hong and A. Hajimiri, *"...Part II: Amplitude Modulation in LC Oscillators,
  Transient Behavior, and Frequency Division,"* IEEE JSSC, vol. 54, no. 8, pp. 2122–2139,
  Aug. 2019.（`BHongGenTheor-II_JSSC2019_Postprint.pdf`，paper_004，**APF / 進階**）
- **[P5]** A. Hajimiri and R. Heald, *"Design Issues in Cross-Coupled Inverter Sense
  Amplifier,"* Proc. IEEE ISCAS, 1998.（`Hajimiri_ISCS_98.pdf`，paper_005，
  **與 ISF 無關**；只當作邊角註解，誠實說明 mislabeled）。

引用內文時用 `[P1] Eq. (21), p.185` 這種格式。每個來自論文的定義/公式/結論/figure 都要標來源。
若 PDF 解析不出或不確定，寫 `TODO: manual verification needed from [Px] page N`。

---

## 2. 統一 Notation（權威符號表，全站一致）

| Symbol | LaTeX | 意義 | 單位 |
|---|---|---|---|
| $t$ | `t` | 時間 | s |
| $\tau$ | `\tau` | noise/impulse 注入時刻 | s |
| $T$ | `T` | 振盪週期 $T=1/f_0$ | s |
| $\omega_0$ | `\omega_0` | 角頻率 $2\pi f_0$ | rad/s |
| $f_0$ | `f_0` | 振盪頻率 | Hz |
| $\phi(t)$ | `\phi(t)` | excess phase（多餘相位） | rad |
| $\Delta\phi$ | `\Delta\phi` | 相位步階/誤差 | rad |
| $A(t)$ | `A(t)` | 瞬時振幅 | V（或 normalized） |
| $\Gamma(\omega_0\tau)$ | `\Gamma(\omega_0\tau)` | ISF（脈衝敏感度函數），無因次、$2\pi$ 週期 | — |
| $q_{max}$ | `q_{max}` | 節點最大電荷擺幅 $=C\cdot V_{max}$ | C |
| $\Delta q$ | `\Delta q` | 注入電荷 | C |
| $i_n(t)$ | `i_n(t)` | noise 電流 | A |
| $\overline{i_n^2}/\Delta f$ | `\overline{i_n^2}/\Delta f` | 電流 noise PSD（單邊） | A²/Hz |
| $S_i(f)$ | `S_i(f)` | 電流 noise PSD | A²/Hz |
| $S_\phi(f)$ | `S_\phi(f)` | phase PSD（單邊） | rad²/Hz |
| $\mathcal{L}(\Delta f)$ | `\mathcal{L}(\Delta f)` | SSB phase noise | dBc/Hz |
| $\Delta f,\ \Delta\omega$ | `\Delta f`, `\Delta\omega` | offset 頻率 | Hz, rad/s |
| $c_0$ | `c_0` | ISF 的 DC 傅立葉係數（DC 值 $=c_0/2$） | — |
| $c_n,\theta_n$ | `c_n`,`\theta_n` | ISF 第 n 諧波幅度/相位 | — |
| $\Gamma_{rms}$ | `\Gamma_{rms}` | ISF 的 rms 值 | — |
| $\Gamma_{eff}$ | `\Gamma_{eff}` | effective ISF（含 cyclostationary） | — |
| $\sigma_t$ | `\sigma_t` | rms timing jitter | s |
| $\sigma_\phi$ | `\sigma_\phi` | rms phase | rad |
| $\kappa$ | `\kappa` | ring 累積 jitter 比例常數 | $\sqrt{s}$ |
| $\omega_{1/f}$ | `\omega_{1/f}` | device 1/f corner | rad/s |
| $N$ | `N` | ring 級數 | — |

**jitter 種類定義**（在 psd_phase_noise_jitter.md 與 serdes 頁要講清楚）：
- **period jitter**：單一週期長度相對 nominal 的偏差 $T_k-T$。
- **cycle-to-cycle jitter**：相鄰兩週期差 $T_{k+1}-T_k$。
- **accumulated / long-term jitter**：相隔 $\Delta t$ 兩 edge 的時間誤差，$\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$。
- **random jitter (RJ)**：高斯、無上界、用 rms 描述；對 SerDes BER 以 $\sigma$ 計。

---

## 3. 權威公式表（請**逐字**複製 LaTeX，含引用）

全部來自 [P1]，equation 編號與 LaTeX 已對照 PDF 渲染頁確認（除非另註 TODO）。

1. **輸出分解** [P1] Eq.(1), p.181：
   `$$V_{out}(t)=A(t)\,f\!\big(\omega_0 t+\phi(t)\big)$$`
2. **電荷→電壓步階** [P1] Eq.(9), p.182：
   `$$\Delta V=\frac{\Delta q}{C_{node}}$$`
3. **excess-phase impulse response（LTV）** [P1] Eq.(10), p.182：
   `$$h_\phi(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau)$$`
4. **LTV phase response（卷積式）** [P1] Eq.(11), p.182：
   `$$\phi(t)=\frac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau$$`
5. **impulse→phase（操作型 ISF 定義）**：
   `$$\Delta\phi=\frac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q$$`
6. **ISF 傅立葉級數** [P1] Eq.(12), p.183：
   `$$\Gamma(\omega_0\tau)=\frac{c_0}{2}+\sum_{n=1}^{\infty}c_n\cos(n\omega_0\tau+\theta_n)$$`
7. **phase response 分諧波** [P1] Eq.(13), p.183：
   `$$\phi(t)=\frac{1}{q_{max}}\!\left[\frac{c_0}{2}\!\int_{-\infty}^{t}\!i_n\,d\tau+\sum_{n=1}^{\infty}c_n\!\int_{-\infty}^{t}\!i_n\cos(n\omega_0\tau+\theta_n)\,d\tau\right]$$`
8. **近 DC 注入單音** [P1] Eq.(15), p.183：
   `$$\phi(t)\approx\frac{I_0\,c_0\sin(\Delta\omega t)}{2q_{max}\,\Delta\omega}$$`
9. **近 $n\omega_0$ 注入單音** [P1] Eq.(16/17), p.183：
   `$$\phi(t)\approx\frac{I_0\,c_n\sin(\Delta\omega t)}{2q_{max}\,\Delta\omega}$$`
10. **白噪 phase noise 求和式** [P1] Eq.(19), p.185：
    `$$\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\overline{i_n^2}/\Delta f\;\sum_{n=0}^{\infty}c_n^2}{8\,q_{max}^2\,\Delta\omega^2}\right)$$`
11. **Parseval / rms ISF** [P1] Eq.(20), p.185：
    `$$\sum_{n=0}^{\infty}c_n^2=\frac{1}{\pi}\int_0^{2\pi}|\Gamma(x)|^2dx=2\,\Gamma_{rms}^2$$`
12. **白噪 1/f² 結果（招牌）** [P1] Eq.(21), p.185：
    `$$\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{\Gamma_{rms}^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)$$`
13. **device flicker** [P1] Eq.(22), p.185：
    `$$\overline{i_{n,1/f}^2}=\overline{i_n^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}$$`
14. **flicker upconversion 1/f³** [P1] Eq.(23), p.185：
    `$$\mathcal{L}\{\Delta\omega\}=10\log_{10}\!\left(\frac{c_0^2}{q_{max}^2}\cdot\frac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\cdot\frac{\omega_{1/f}}{\Delta\omega}\right)$$`
15. **1/f³ corner** [P1] Eq.(24), p.185：
    `$$\Delta\omega_{1/f^3}=\omega_{1/f}\cdot\frac{c_0^2}{2\,\Gamma_{rms}^2}\approx\omega_{1/f}\left(\frac{c_0}{c_1}\right)^2$$`
16. **SSB↔phase PSD**（小角近似）：`$$\mathcal{L}(\Delta f)\approx\tfrac12 S_\phi(\Delta f)$$`
17. **phase→time**：`$$\Delta t=\frac{\Delta\phi}{2\pi f_0}$$`
18. **phase variance**：`$$\sigma_\phi^2=\int_{f_1}^{f_2}S_\phi(f)\,df$$`
19. **rms jitter**：`$$\sigma_t=\frac{1}{2\pi f_0}\sqrt{\int_{f_1}^{f_2}S_\phi(f)\,df}$$`
20. **ring 累積 jitter** [P2] Eq.(8), p.792（κ 由 Eq.(12), p.793）：`$$\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$$` ✓已核實
21. **ring 頻率** [P2] Eq.(15), p.794：`$$f_0=\frac{1}{2N\tau_D}$$`（Eq.(14) 定義正規化級延遲 $\hat t_D=\eta/f'_{max}$；週期關係 $2\pi=2N\hat t_D$ 推得本式為 Eq.(15)）
22. **ring Γrms** [P2] Eq.(16), p.794 ✓已核實：`$$\Gamma_{rms}=\sqrt{\tfrac{2\pi^2}{3\eta^3}\tfrac{1}{N^{1.5}}}\Rightarrow\Gamma_{rms}\propto N^{-3/4}$$`
23. **ring 白噪 FOM** [P2] Eq.(23), p.796 ✓已核實（前置係數 v3 已對照 PDF p.796 更正為 8/(3η)）：`$$\mathcal{L}=\frac{8}{3\eta}\frac{kT}{P}\frac{V_{DD}}{V_{char}}\Big(\frac{f_0}{\Delta f}\Big)^2$$`（η=級延遲比例常數 Eq.(14)，≈1；γ 僅透過 $V_{char}=\Delta V/\gamma$ 進入；min at V_T=0: $\frac{16\gamma}{3\eta}$）

> **重要的 factor-of-2 教學註記**：用時域「白噪×ISF→積分」乾淨推導會得到
> $S_\phi(f)=\Gamma_{rms}^2 S_i/(q_{max}^2(2\pi f)^2)$，對應 $\mathcal{L}=\Gamma_{rms}^2 S_i/(2q_{max}^2\Delta\omega^2)$；
> 而 [P1] Eq.(21) 寫成 $/(4\Delta\omega^2)$。差的 2 倍來自 SSB 記帳慣例，
> 是文獻上著名的小爭議。**不影響** $\Gamma_{rms}^2/q_{max}^2$ scaling 與 $-20$ dB/dec 斜率。
> 在 white_noise_to_phase_noise.md 要明講這件事。

---

## 4. 圖片（已產生於 `static/figures/`，網站用 `/figures/<name>.png` 引用）

| 檔名 | 由哪個 script/function | 公式 | 教學訊息 |
|---|---|---|---|
| `limit_cycle_phase_amplitude.png` | lab_01 `fig_limit_cycle` | 2-D state model | phase=切向(持續)、amplitude=徑向(被拉回) |
| `waveform_with_impulse_markers.png` | lab_01 `fig_impulse_markers` | $V=\cos$, peak vs ZC | 同 impulse、相位不同→效果不同 (LTV) |
| `lc_waveform_and_isf.png` | lab_02 `main` | $\Gamma=-\sin\theta$ | LC ISF；Δφ∝Δq；ZC 注入=純相位跳 |
| `ring_oscillator_timing_noise_accumulation.png` | lab_03 `fig_accumulation` | $\sigma_{\Delta t}=\sigma\sqrt{\Delta N}$ | 累積 jitter 隨機漫步 |
| `lc_vs_ring_isf_comparison.png` | lab_03 `fig_lc_vs_ring_isf` | $-\sin$ vs triangular | ring 敏感度集中在 transition；N↑ rms↓ |
| `sinusoidal_impulse_phase_sweep.png` | lab_04 `fig_isf_sweep` | $\Delta\phi=-\sin\theta\cdot\Delta q/q_{max}$ | 相位敏感度隨注入相位變化 |
| `isf_impulse_sweep_sinusoidal.png` | lab_04 `fig_isf_sweep` | numeric vs $-\sin$ | 數值法萃取 ISF，誤差~0.001 |
| `lti_vs_ltv_impulse_response.png` | lab_04 `fig_lti_vs_ltv` | $h(t-\tau)$ vs $h_\phi(t,\tau)$ | LTV：階高隨注入相位變 |
| `isf_fourier_reconstruction.png` | lab_05 `fig_reconstruction` | Eq.(12) | 諧波越多越逼近 |
| `isf_fourier_coefficients.png` | lab_05 `fig_coefficients` | $c_n$, Parseval | 係數頻譜；驗證 $\sum c_n^2=2\Gamma_{rms}^2$ |
| `symmetric_vs_asymmetric_isf_c0.png` | lab_05 `fig_symmetric_vs_asymmetric` | $c_0$ | 只有 $c_0\neq0$ 才上轉 1/f |
| `white_noise_phase_noise_psd.png` | lab_06 `main` | $S_\phi\propto1/f^2$ | 白噪→1/f² 相位雜訊；理論吻合 |
| `flicker_upconversion_symmetric_vs_asymmetric.png` | lab_07 `main` | 1/f³ vs 抑制 | 對稱性決定 close-in 1/f³ |
| `phase_noise_to_jitter_integration.png` | lab_08 `main` | $\sigma_t$ 積分 | L(f)→rms jitter；5GHz, -100dBc/Hz→~448fs |

嵌入語法（Markdown）：`![說明](/figures/limit_cycle_phase_amplitude.png)`。
每張圖在所屬頁要附：對應公式、參數表、單位、Python 核心 code、完整 script path
（如 `simulations/lab_01_sinusoidal_oscillator.py`）、如何解讀、是否 toy model。

---

## 5. Python API（撰寫 code block 時引用真實函式，勿杜撰）

`simulations/common/isf_utils.py`：`wrap_phase`, `gamma_symmetric`, `gamma_asymmetric(alpha)`,
`gamma_lc_ideal`(=−sin), `gamma_triangular(n_stages)`, `impulse_to_phase_step(dq,gamma,qmax)`,
`integrate_phase_from_noise(t,i,gamma_vals,qmax)`, `apply_isf_weighting(t,i,gamma_func,qmax,omega0)`,
`compute_fourier_coefficients(theta,gamma,n_harmonics)->(a0,a,b,c,phase)`,
`reconstruct_from_fourier`, `gamma_rms(theta,gamma)`, `effective_isf(gamma,alpha)`.

`simulations/common/noise_utils.py`：`white_noise(n,psd,fs,rng)`, `flicker_noise(n,fs,k_flicker,...)`,
`estimate_psd(x,fs,nperseg)`, `phase_psd_to_l_dbc_per_hz(s_phi)`, `phase_to_time_error(phi,f0)`,
`integrate_rms_jitter(f,l_dbc,f0,fmin,fmax)->(sigma_t,sigma_phi)`, `leeson_one_over_f2(f,Lref,fref)`.

`simulations/common/oscillator_models.py`：`sinusoidal_oscillator`, `simulate_lc(...)`,
`excess_phase`, `extract_isf_by_injection(...)`, `ring_edge_times`, `accumulated_jitter_curve`,
`phase_to_time`.

跑法：`python scripts/run_all_sims.py`（產生全部圖到 `static/figures/`）。

---

## 6. MDX / KaTeX 規則（**違反會 build 失敗，務必遵守**）

1. 每頁開頭要有 front matter：
   ```
   ---
   title: <頁面標題>
   description: <一句話>
   ---
   ```
   並在內文第一行放一個 `#` H1 標題。
2. 行內數學用 `$...$`，獨立公式用 `$$...$$`。**`$` 必須成對**。
3. **散文中不要出現裸的 `{` `}` 或 `<` 後接字母**（MDX 會當成 JSX）。
   - 不等式請寫成數學：`$\Delta\omega < \omega_{1/f}$`，或用 `&lt;` / `&gt;`。
   - 需要大括號就放進 `$...$` 或 code span（反引號）。
4. 多步推導用 `$$\begin{aligned} ... \\ ... \end{aligned}$$`（KaTeX 支援）。
5. 圖片：`![alt](/figures/name.png)`。程式碼：用 ```` ```python ```` fenced block。
6. Mermaid 區塊用 ```` ```mermaid ````（已啟用 theme-mermaid）。block diagram 用
   `A["i_n(t)"] --> B["× Γ(ω₀t)/q_max"] --> C["∫ dt"] --> D["φ(t)"]` 這種寫法；
   節點文字放進雙引號避免特殊字元問題。
7. 表格用標準 Markdown。cell 內若有 `|` 要寫 `\|`。
8. 連結到其他頁：`[文字](/02_foundations/oscillator_phase)`（路徑不含 docs/、不含 .md）。
9. KaTeX 只用標準指令（`\frac \sqrt \sum \int \Gamma \omega \Delta \cdot \approx \propto
   \log_{10} \sin \cos \langle \rangle \overline \begin{aligned}`）。不要用未定義巨集。
10. 不要用 HTML `<br>`；要換行就分段。需要時用 `<br/>`（自閉）。

---

## 7. 頁面結構模板

**理論頁**（02_*, 03_*）：H1 →「這頁要回答什麼」→ 物理直覺（blockquote）→ 逐步推導
（每步：用到什麼物理/數學、近似、單位、為何合理、怎麼檢查 dimension）→ 數值例子（帶單位）
→ 對應圖（若有）→ 適用/失效條件 → 與哪些 paper/公式對應（引用）→「重點回顧」清單 →
「延伸閱讀」連結。

**Lab 頁**（04_*）：H1 → 1.教學目標 2.數學模型 3.block diagram(mermaid) 4.Python 核心 code
5.完整 script path 6.參數表 7.單位表 8.模擬圖(嵌入) 9.如何解讀圖 10.對應 paper 公式/figure
11.限制與 approximation。

**Deep-dive 頁**（05_*）：H1=論文標題 → Citation → 一句話貢獻 → 為何重要 → 主要假設 →
Key equations（原式/意義/逐步推導/數值例/Python 驗證）→ Key figures → Design insights →
Limitations → 與其他 paper 關係 → What to remember。

**Design 頁**（06_*）：H1 → 問題（為什麼…）→ 用 ISF 公式回答 → 數值/scaling →
design knobs 清單 → 與 SerDes 關聯。

---

## 8. 可重複使用的數值例子（canonical，請全站一致）

- **例 A（impulse→phase）**：$q_{max}=1$ pC、$\Delta q=1$ fC、$\Gamma=0.5$、$f_0=5$ GHz。
  $\Delta\phi=0.5\times10^{-15}/10^{-12}=5\times10^{-4}$ rad $=0.0286^\circ$；
  $\Delta t=\Delta\phi/(2\pi f_0)=5\times10^{-4}/(2\pi\cdot5\times10^9)=15.9$ fs。
- **例 B（白噪 L）**：$f_0=5$ GHz、$\Delta f=1$ MHz、$q_{max}=1$ pC、$\Gamma_{rms}=0.5$、
  $S_i=10^{-24}$ A²/Hz。用 Eq.(21)：$\mathcal{L}=10\log_{10}[(0.25/10^{-24})\cdot
  (10^{-24}/(4(2\pi\cdot10^6)^2))]$。先算 $\Delta\omega=2\pi\cdot10^6=6.283\times10^6$ rad/s，
  $\Delta\omega^2=3.948\times10^{13}$。括號 $=0.25/(4\cdot3.948\times10^{13})=1.583\times10^{-15}$，
  $\mathcal{L}=10\log_{10}(1.583\times10^{-15})=-148.0$ dBc/Hz。（這是「單一白噪源」的理想值，
  真實電路有多個源、cyclostationary、flicker，會更高。）
- **例 C（jitter 積分）**：$f_0=5$ GHz、$\mathcal{L}(1\text{MHz})=-100$ dBc/Hz、1/f² 斜率、
  積分 1→100 MHz。$\sigma_\phi=14.07$ mrad、$\sigma_t=447.9$ fs（見 lab_08，數值=解析）。

> 數值要帶單位、要示範 dimension check（例如 rad ÷ (rad/s) = s）。

---

## 9. 誠實/TODO 原則

- toy model 一律標明「這是 pedagogical toy model，非 transistor-level」。
- 來自外部文獻（PPV / adjoint / Floquet / Leeson / Demir）要標「不在下載的 5 篇 PDF 內，
  以標準文獻補充」。
- 不確定的常數/figure/citation 寫 `TODO: manual verification needed ...`。
- [P5] 一律誠實說明它是 sense amplifier 論文、與 ISF 無關。

---

## 10. v2 增補（新圖、新公式、新頁、worked-example 規格）

### 10.1 新增模擬圖（已產生於 static/figures/，用 `/figures/<name>.png` 引用）

| 檔名 | script / function | 公式 | 教學訊息 |
|---|---|---|---|
| `rf_spectrum_phase_noise_sidebands.png` | lab_10 `main` | $v=\cos(\omega_0 t+\phi(t))$, FFT | phase noise 把載波塗成裙帶（[P1] Fig.8） |
| `monte_carlo_jitter_histogram.png` | lab_11 `main` | $\sigma_{\Delta t}=\sigma_{edge}\sqrt{\Delta N}$ | RJ 是高斯，σ 隨 √ΔN |
| `serdes_eye_ber_bathtub.png` | lab_12 `main` | BER bathtub（RJ） | jitter→eye 閉合→BER |
| `pll_cdr_jitter_transfer.png` | lab_13 `main` | $\lvert H_{lp}\rvert^2,\lvert H_{hp}\rvert^2$ | PLL 把 VCO noise 高通、ref 低通 |
| `cyclostationary_effective_isf.png` | lab_14 `main` | $\Gamma_{eff}=\Gamma\alpha$ | noise 注入相位決定 $\Gamma_{eff,rms}$ |
| `nonlinear_oscillator_isf.png` | lab_15 `main` | van der Pol | ISF 隨大訊號波形改變，非恆為 $-\sin$ |
| `leeson_vs_isf_overlay.png` | lab_16 `main` | Leeson vs ISF | 兩模型同 1/f³,1/f²,floor 三段 |
| `design_tradeoff_sweeps.png` | lab_17 `main` | $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$ | swing/Γrms/N 的設計曲線 |

新 util：`simulations/common/pll_utils.py`（`H_lowpass_mag2,H_highpass_mag2,shape_output_phase_noise`）、
`serdes_utils.py`（`Q,ber_bathtub,eye_traces`）。

### 10.2 新增權威公式（v2，逐字複製）

**down-conversion（white_noise/fourier 必補的中間步驟）**：對 $i(\tau)=I_0\cos((n\omega_0+\Delta\omega)\tau)$，
用積化和差 $\cos A\cos B=\tfrac12[\cos(A-B)+\cos(A+B)]$，慢項 $\cos(\Delta\omega\tau-\theta_n)$ 存活、
快項（$\approx 2n\omega_0$）被積分器平均掉：
$$
\int^{t}\!\!c_n\cos(n\omega_0\tau+\theta_n)\,I_0\cos((n\omega_0+\Delta\omega)\tau)\,d\tau\approx\frac{I_0 c_n}{2}\cdot\frac{\sin(\Delta\omega t-\theta_n)}{\Delta\omega}
$$
**factor-8 求和（(18)→(19)）**：單邊帶功率 $(I_0 c_n/(4q_{max}\Delta\omega))^2=I_0^2c_n^2/(16q_{max}^2\Delta\omega^2)$；
白噪令 $I_0^2/2\to\overline{i_n^2}/\Delta f$（故 $I_0^2\to2\overline{i_n^2}/\Delta f$），上下兩 sideband 各一份，對 $n$ 求和：
$$
\mathcal{L}=\sum_n\frac{2(\overline{i_n^2}/\Delta f)c_n^2}{16\,q_{max}^2\Delta\omega^2}=\frac{(\overline{i_n^2}/\Delta f)\sum_n c_n^2}{8\,q_{max}^2\Delta\omega^2}
$$
**$L\approx\tfrac12 S_\phi$（小角 PM）**：$\phi(t)=\phi_p\sin\omega_m t$ 小角下
$\cos(\omega_0t+\phi)\approx\cos\omega_0t-\tfrac{\phi_p}{2}[\cos(\omega_0-\omega_m)t-\cos(\omega_0+\omega_m)t]$，
每個 sideband 相對功率 $(\phi_p/2)^2$；相位方差密度 $S_\phi=\phi_p^2/2$ 故 $\mathcal{L}=S_\phi/2$。
**period / cycle-to-cycle jitter 核**：
$$
\sigma_{T}^2=\frac{1}{(2\pi f_0)^2}\int_0^{\infty}S_\phi(f)\,\lvert 1-e^{-j2\pi fT}\rvert^2\,df
$$
period jitter 是相位的一階差分（高通核 $\lvert1-e^{-j2\pi fT}\rvert^2$）；cycle-to-cycle 是二階差分
（核 $\lvert1-e^{-j2\pi fT}\rvert^4$）；accumulated 則不含差分（低頻主導）。確切常數若不確定標 TODO。
**PLL（type-II 2nd order）**：
$$
\lvert H_{lp}\rvert^2=\frac{(2\zeta\omega_n\omega)^2+\omega_n^4}{(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2},\quad
\lvert H_{hp}\rvert^2=\frac{\omega^4}{(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2}
$$
輸出 $S_{out}=S_{ref}\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$。
**SerDes BER（RJ）**：$\text{BER}(t)=\tfrac12[Q(\tfrac{UI/2-t}{\sigma_t})+Q(\tfrac{UI/2+t}{\sigma_t})]$，$Q(x)=\tfrac12\,\mathrm{erfc}(x/\sqrt2)$。
**Leeson（外部文獻，非 5 篇 PDF）**：
$$
\mathcal{L}(\Delta\omega)=10\log_{10}\!\left[\frac{2FkT}{P_s}\left(1+\Big(\frac{\omega_0}{2Q\Delta\omega}\Big)^2\right)\left(1+\frac{\omega_{1/f^3}}{\lvert\Delta\omega\rvert}\right)\right]
$$
**ring**：$f_0=\dfrac{1}{2N\tau_D}$；$\Gamma_{rms}\propto N^{-3/4}$（[P2] Eq.(16)，⚠️ 常數待查）。
**Floquet/PPV（外部文獻）**：$\dot\phi(t)=v_1^{T}(t)B(t)\xi(t)$，ISF $=q_{max}\cdot$（PPV 在注入節點的分量）。標明非 5 篇 PDF。

### 10.3 新增頁面（要新建）

- `99_appendix/derivation_floquet_ppv.md`：Floquet→$v_1(t)$→adjoint/PPV→證明 ISF 是 PPV 投影。明標外部文獻（Demir 2000、Kärtner），TODO 待補正式 citation。
- `99_appendix/derivation_leeson.md`：Leeson 推導 + 與 ISF 結果逐項對照（$Q,F,1/f^3$ corner）。嵌入 `/figures/leeson_vs_isf_overlay.png`。
- `04_simulation_labs/worked_examples.md`：~15 題分級（基礎換算／ISF→PN／jitter 積分／設計反推），每題：題目、逐步解、單位、dimension check、一行 Python 驗證。
- `04_simulation_labs/lab_10_rf_spectrum.md` … `lab_17_design_sweep.md`：8 個新 lab 頁，照第 7 節 lab 模板 11 段，嵌入 10.1 的對應圖，先 Read 對應 `simulations/lab_1x_*.py` 引用真實 code。

### 10.4 worked-example 規格（Wave B）

每個 03_* 與 06_* 頁至少 **2 個 worked example**，格式：
> **例**：給定數值 → 逐步代入（帶單位）→ 結果 → dimension check → 一行 Python 驗證（引用 `simulations/common/`）。
數值沿用第 8 節 canonical（$q_{max}=1$ pC、$\Gamma=0.5$、$f_0=5$ GHz、$\Gamma_{rms}=0.5$、$S_i$、$\mathcal{L}(1\text{MHz})=-100$ dBc/Hz）為主，需要時可加第二組不同數字。

### 10.5 編輯既有頁面的鐵則（Wave A/B 改寫時）

- **先 Read 既有檔案，保留原有正確內容**，只「插入」展開推導段與 worked-example 段；不要整頁重寫導致內容流失。
- 嚴守 MDX/KaTeX：**每個 `$$` 圍欄要獨立成行**（前後各一行只有 `$$`）；行內不等式用 `>`/`<`（**不要**用 `&gt;`/`&lt;`）；表格 cell 內數學的 `|` 用 `\vert` 或 `\lvert..\rvert`。

---

## 11. v3 深化增補（Lorentzian / Allan / PLL budget / 拓樸 / HTM / 嚴格頻譜 / 習題 / capstone）

### 11.1 新增圖（已產生於 static/figures/）

| 檔名 | script | 公式 | 教學訊息 |
|---|---|---|---|
| `lorentzian_carrier_lineshape.png` | lab_18 | $S\propto D/(D^2+\Delta\omega^2)$ | 載波是 Lorentzian、近載波轉平；1/f² 只是遠端漸近 |
| `allan_deviation.png` | lab_19 | $\sigma_y(\tau)$ 斜率 | white/flicker/RW FM → $\tau^{-1/2},\tau^0,\tau^{+1/2}$ |
| `pll_noise_budget.png` | lab_20 | $S_{out}=\sum$ 各源×transfer | PLL 雜訊預算 + 最佳 loop BW |
| `cross_coupled_vco_isf.png` | lab_21 | tank vs tail 有效 ISF | tail 的 $c_0,c_2$ 才是麻煩（illustrative） |

### 11.2 新增權威公式（v3）

**Lorentzian 線寬**（相位 random walk 的嚴格後果；連 [E2] Demir 2000）：
- 相位擴散：$\operatorname{Var}[\Delta\phi(t)]=2D|t|$（$D$=phase diffusion，rad²/s）。
- 載波自相關：$R_x(\tau)=\tfrac12\cos(\omega_0\tau)\,e^{-D|\tau|}$。
- 頻譜（繞載波單邊）：$S(\Delta\omega)\propto\dfrac{D}{D^2+\Delta\omega^2}$（**Lorentzian**）。
- 3-dB 線寬（FWHM）：$\Delta f_{3\mathrm{dB}}=\dfrac{D}{\pi}$ Hz；HWHM $=\dfrac{D}{2\pi}$ Hz。
- 與 ISF 連結：$S_\phi=\dfrac{2D}{\Delta\omega^2}$（1/f² skirt）$\Rightarrow D=\dfrac{\Gamma_{rms}^2}{2q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$、
  $\Delta f_{3\mathrm{dB}}=\dfrac{\Gamma_{rms}^2}{2\pi q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$。
- **關鍵教學點**：[P1] Eq.(21) 的 $1/\Delta\omega^2$ 在 $\Delta\omega\to0$ 發散是「線性化近似」假象；真實頻譜近載波轉平成 Lorentzian、總功率守恆（積分=載波功率）。

**Allan variance / ADEV**：
- 兩樣本（Allan）變異數：$\sigma_y^2(\tau)=\big\langle\tfrac12(\bar y_{k+1}-\bar y_k)^2\big\rangle$。
- 由頻域：$\sigma_y^2(\tau)=2\displaystyle\int_0^\infty S_y(f)\dfrac{\sin^4(\pi f\tau)}{(\pi f\tau)^2}\,df$，其中 $S_y(f)=\dfrac{f^2}{f_0^2}S_\phi(f)$。
- 斜率對照：white PM $\tau^{-1}$、flicker PM $\tau^{-1}$、**white FM $\tau^{-1/2}$、flicker FM $\tau^{0}$（floor）、random-walk FM $\tau^{+1/2}$**。

**PLL 輸出雜訊預算**：$S_{out}=(S_{ref}N^2+S_{cp})\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$；
最佳 loop BW $f_n^\*$ 使 $\int S_{out}df$（積分 jitter）最小（in-band ref/CP vs out-of-band VCO 的權衡）。
$\lvert H_{lp}\rvert^2,\lvert H_{hp}\rvert^2$ 見規範 10.2。

**HTM / 嚴格 LTV**（連讀者訊號與系統背景）：
- LTV：$y(t)=\int h(t,\tau)x(\tau)d\tau$；Zadeh 時變傳函 $H(f,t)=\int h(t,t-\sigma)e^{-j2\pi f\sigma}d\sigma$。
- 週期 LTV（振盪器）：harmonic transfer matrix，輸入頻率 $f$ 的成分被搬到 $f+k f_0$，增益為 ISF 的第 $k$ 個傅立葉係數 $c_k$——**ISF 就是相位輸出對各諧波的轉換向量**（連 [P1] Eq.(13)、fourier 頁）。

### 11.3 新增頁面（要新建）＋深化

新建：
- `03_isf_core_theory/lorentzian_linewidth.md`：用 11.2 的 Lorentzian 全套，解 1/f² 發散矛盾；嵌入 lorentzian 圖。
- `02_foundations/allan_variance.md`：ADEV 定義、L(f)↔ADEV、斜率表；嵌入 allan 圖。
- `06_design_insights/pll_noise_budget.md`：五源預算 + 最佳 BW；嵌入 pll_budget 圖。
- `06_design_insights/real_oscillator_topologies.md`：cross-coupled LC VCO（tail 2×upconversion、tail filter）、Colpitts、CMOS ring stage（由 switching slope 推 ISF）；嵌入 cross_coupled_vco_isf 圖（標 illustrative）。
- `06_design_insights/measurement_and_spurs.md`：量 L(f) 三法（SA 直接、delay-line discriminator、cross-correlation）、spur vs 隨機 PN、如何讀 PN 圖。
- `99_appendix/ltv_htm.md`：Zadeh $H(f,t)$、HTM、ISF 是相位輸出 HTM 的轉換向量。
- `03_isf_core_theory/capstone_lc_end_to_end.md`：一顆 ideal LC 從 state equations → Floquet → $\Gamma=-\sin$ → $\Gamma_{rms}$ → $S_\phi$ → **Lorentzian 線寬** → $\sigma_t$ → BER，每步嚴格＋數值。
- `02_foundations/exercises.md`、`03_isf_core_theory/exercises.md`、`06_design_insights/exercises.md`：各 6–8 題（推導+數值+設計反推），**附完整解答＋Python 驗證**。

深化（既有頁，只插入、保留原內容）：
- `03_isf_core_theory/white_noise_to_phase_noise.md`：新增「## 嚴格頻譜推導（cyclostationary 自相關 → Wiener-Khinchin）」段，證明 $\sum c_n^2=2\Gamma_{rms}^2$ 自然從自相關出來，並連到 Lorentzian。
- `03_isf_core_theory/effective_isf.md`：新增「從 device bias-dependent 熱雜訊推 NMF $\alpha(t)$」與 switching-pair worked example。

### 11.4 鐵則（同前）
照第 6 節 MDX/KaTeX 規則（$$ 圍欄獨立成行、數學用 >/< 不用實體、表格 | 用 \vert、front matter+H1）。
深化既有頁要先 Read、保留原內容、只插入。標 illustrative/toy；外部文獻標「不在 5 篇 PDF 內」（Demir 2000、Allan、Leeson 已有 citation）。
