---
title: 中英對照詞彙表 Glossary
description: ISF 相關術語的中英對照，每個給一句中文直覺定義加站內出處頁連結。
---

# 中英對照詞彙表 Glossary

> **See also**：[notation](/00_overview/notation)（嚴格符號與單位）、[math_identities](/99_appendix/math_identities)（數學工具）、[references](/99_appendix/references)（文獻代號 [P1]–[P5]、外部 [E1]–[E4]）

讀英文論文與中文教學頁時最大的摩擦是「同一件事兩種語言」。這頁把全站術語做**中英對照**，
每個給**一句中文直覺**（不是嚴格定義，是「先抓到感覺」）加上**站內出處頁**。要深入就點連結。

> **怎麼用這頁**：當你在某頁遇到不熟的詞，回來這裡掃一句直覺，再決定要不要點進出處頁細讀。
> 嚴格符號與單位請對照 [notation](/00_overview/notation)。標 **(外部)** 者表示**不在下載的
> 5 篇 PDF 內**，以標準文獻補充。

---

## 核心 ISF 詞彙

| 英文 | 中文 | 一句話直覺 | 出處頁 |
|---|---|---|---|
| **ISF (Impulse Sensitivity Function)** | 脈衝敏感度函數 | 振盪器對 noise 的「相位敏感度權重」——告訴你「在波形哪個相位踢一下，會被轉成多少相位」。無因次、$2\pi$ 週期。 | [isf_definition](/03_isf_core_theory/isf_definition) |
| **excess phase** | 多餘相位 $\phi(t)$ | 理想相位 $\omega_0 t$ 之外的偏差；phase noise 與 jitter 都住在這裡。 | [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) |
| **phase noise** | 相位雜訊 | 振盪訊號相位的隨機抖動，在頻域呈現為 carrier 兩側的裙邊。 | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) |
| **timing jitter** | 時間抖動 | 同一件事的時域說法：edge 出現時刻偏離理想的隨機誤差。 | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) |
| **phase perturbation** | 相位擾動 | noise 推動狀態點「沿 limit cycle 切向」的分量；**沒有恢復力**，永久留存。 | [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) |
| **amplitude perturbation** | 振幅擾動 | noise 推動狀態點「徑向」的分量；有 restoring 機制會被拉回，**不永久殘留**。 | [phase_vs_amplitude_noise](/02_foundations/phase_vs_amplitude_noise) |
| **limit cycle** | 極限環 | 振盪器在 state-space 裡穩態繞的封閉軌跡；相位=沿環走多遠、振幅=離環多遠。 | [oscillator_phase](/02_foundations/oscillator_phase) |

---

## 系統與雜訊性質

| 英文 | 中文 | 一句話直覺 | 出處頁 |
|---|---|---|---|
| **LTI (Linear Time-Invariant)** | 線性非時變 | 脈衝響應只看「相隔多久」$t-\tau$；振盪器對 noise **不是** LTI。 | [math_identities](/99_appendix/math_identities) |
| **LTV (Linear Time-Variant)** | 線性時變 | 脈衝響應還要看「在何時踢」$\tau$——同一顆 impulse 在不同相位效果不同，正是 ISF 的精神。 | [convolution_derivation](/03_isf_core_theory/convolution_derivation) |
| **cyclostationary noise** | 週期穩態雜訊 | noise 的強度本身隨振盪週期週期性變化（device 不是隨時都在漏雜訊）。 | [effective_isf](/03_isf_core_theory/effective_isf) |
| **noise-modulating function (NMF)** $\alpha(\omega_0 t)$ | 雜訊調變函數 | $0\le\alpha\le1$ 的週期函數，描述「device 何時在漏雜訊」；與 ISF 相乘得 effective ISF。 | [effective_isf](/03_isf_core_theory/effective_isf) |
| **white noise** | 白噪 | PSD 與頻率無關的雜訊（自相關是 delta）；經 ISF 積分器轉成 $1/f^2$ 相位雜訊。 | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) |
| **flicker noise (1/f noise)** | 閃爍雜訊／$1/f$ 雜訊 | 低頻能量大的 device 雜訊；只透過 ISF 的 $c_0$ 上轉成 close-in $1/f^3$ 相位雜訊。 | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) |
| **upconversion** | 上轉（頻率搬移） | ISF 像 mixer，把低頻（或 $n\omega_0$ 附近）的 device 雜訊搬到 carrier 附近變相位雜訊。 | [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) |

---

## 傅立葉與統計量

| 英文 | 中文 | 一句話直覺 | 出處頁 |
|---|---|---|---|
| **rms / effective ISF** | rms ISF $\Gamma_{rms}$ / 有效 ISF $\Gamma_{eff}$ | $\Gamma_{rms}$ 是 ISF 的均方根，直接決定 $1/f^2$ 相位雜訊大小；$\Gamma_{eff}=\Gamma\cdot\alpha$ 把 cyclostationary 併進來。 | [rms_isf](/03_isf_core_theory/rms_isf) |
| **$q_{max}$** | 最大電荷擺幅 | 節點電荷擺幅 $=C\cdot V_{max}$，用來 normalize ISF；越大相位雜訊越低。 | [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) |
| **$c_0$ (DC ISF coefficient)** | ISF 的 DC 係數 | 控制 $1/f$ 上轉的關鍵；ISF 的 DC **值** $=c_0/2$。對稱波形 $c_0\approx0$。 | [symmetry](/06_design_insights/symmetry) |
| **Fourier series / coefficients** $c_n,\theta_n$ | 傅立葉級數／係數 | 把 $2\pi$ 週期的 ISF 拆成 DC 加諧波；第 $n$ 條諧波搬移 $n\omega_0$ 附近的雜訊。 | [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) |
| **PSD (Power Spectral Density)** | 功率譜密度 | 每單位頻寬的雜訊功率；$S_i$（A²/Hz）、$S_\phi$（rad²/Hz）。對頻率積分得 variance。 | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) |
| **SSB phase noise** $\mathcal{L}(\Delta f)$ | 單邊帶相位雜訊 | 相對 carrier、單一 sideband、每 Hz 的相位雜訊功率；$\approx\frac12 S_\phi$。 | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) |
| **dBc/Hz** | 分貝（相對載波）每赫茲 | $\mathcal{L}$ 的單位：「c」=相對 carrier、「/Hz」=每單位頻寬，取 $10\log_{10}$。 | [math_identities](/99_appendix/math_identities) |

---

## 振盪器種類與進階概念

| 英文 | 中文 | 一句話直覺 | 出處頁 |
|---|---|---|---|
| **ring oscillator** | 環形振盪器 | $N$ 級反相器串成環；ISF 集中在 transition、$\Gamma_{rms}\propto N^{-3/2}$。 | [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| **LC oscillator** | LC 振盪器 | tank 諧振、波形近正弦；理想 ISF $=-\sin\theta$。 | [lab_02](/04_simulation_labs/lab_02_lc_oscillator_toy_model) |
| **accumulated jitter** | 累積（長期）jitter | 開環振盪器無絕對時間參考，誤差像隨機漫步 $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ 成長。 | [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| **injection locking / pulling** | 注入鎖定／拉扯 | 外部訊號注入把振盪器頻率「拉」向它；同一個 ISF 也主宰這現象（廣義 Adler）。 | [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1) |
| **APF (Amplitude Perturbation Function)** $\Delta(\phi)$ | 振幅擾動函數 | ISF 之於相位，APF 之於振幅；單位 1/A。理想 LC 中與 ISF 正交（quadrature）。 | [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2) |
| **Adler's equation** | Adler 方程 | 描述 injection-locked 相位差的一階微分方程（1946）；ISF 把它推廣到任意波形。 | [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1) |

---

## 注入鎖定與量測（Injection Locking & Measurement）

| 英文 | 中文 | 一句話直覺 | 出處頁 |
|---|---|---|---|
| **realignment factor** $\beta$ | 重新對齊係數 | 每根注入脈衝把相位「拉回」多少的線性化增益；決定離散迴路穩定範圍 $0<\beta<2$ 與雜訊整形轉角 $\approx\beta f_{ref}/2\pi$。 | [subharmonic_injection](/06_design_insights/subharmonic_injection) |
| **impulse-train locking** | 脈衝列鎖定 | 用週期性脈衝（而非連續正弦）注入時，鎖定範圍由脈衝的第 $N$ 諧波幅度與 ISF 基頻交互決定，是 subharmonic injection（次諧波注入）的核心機制。 | [subharmonic_injection](/06_design_insights/subharmonic_injection) |
| **washboard potential**（tilted washboard） | 傾斜搓衣板位能 | 把 Adler 方程改寫成一顆粒子在傾斜週期位能 $U(\theta)$ 裡滾動的圖像；鎖定＝滾進最近凹槽，cycle slip＝熱雜訊把粒子踢過鄰近障壁。 | [lab_36](/04_simulation_labs/lab_36_lock_acquisition) |
| **ILFD (Injection-Locked Frequency Divider)** | 注入鎖定除頻器 | 本身就是一顆跑在 $f_0=f_{inj}/N$ 的振盪器，靠 ISF 第 $N$ 諧波鎖定，而不是數位除法電路。 | [injection_locked_division](/06_design_insights/injection_locked_division) |
| **dual-Dirac model** | 雙 Dirac 模型 | 業界標準：把任意形狀的有界 DJ 近似成兩個 Dirac delta（左右各半），配合高斯 RJ 的 $Q$ 函數尾巴積分求 $\text{TJ(BER)}$。 | [dj_dual_dirac](/06_design_insights/dj_dual_dirac) |
| **ADEV / Allan deviation** | 亞倫偏差 | 時鐘／頻率標準界慣用的時域穩定度指標：兩樣本變異數的平方根；log–log 斜率一眼讀出白／閃爍／隨機漫步 FM 雜訊型態。 | [allan_variance](/02_foundations/allan_variance) |
| **sub-sampling PLL** | 次取樣鎖相環 | 用參考邊緣直接取樣 VCO 正弦當鑑相器，divider 整個從雜訊路徑消失，charge-pump 噪聲不再被 $\times N^2$ 放大。 | [sampling_pll](/06_design_insights/sampling_pll) |
| **Lorentzian linewidth** | 洛倫茲線寬 | 相位 random walk 的自相關是指數衰減，Wiener–Khinchin 轉出一條有限高、有限寬的鐘形頻譜；$1/f^2$ 只是它遠離中心的漸近尾巴。 | [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) |
| **cycle slip / Kramers escape** | 週期滑動／克拉默逃逸 | 雜訊把鎖定相位整圈（$2\pi$）踢過 washboard 障壁的稀有事件；逃逸率遵循 Kramers 公式（外部文獻）。 | [lab_36](/04_simulation_labs/lab_36_lock_acquisition) |
| **cross-correlation measurement** | 交叉相關量測法 | 用兩條獨立量測通道相關，把各自不相關的儀器本底以 $1/\sqrt{M}$ 壓低，量出比單通道乾淨的 $\mathcal{L}(f)$。 | [measurement_and_spurs](/06_design_insights/measurement_and_spurs) |
| **polyphase filter** | 多相濾波器 | RC-CR 網路在 $\omega=1/RC$ 處產生 $90^\circ$ 相移來做 I/Q，多級串接可拓寬頻寬；本身不主動產生新的 close-in 相位雜訊。 | [quadrature_and_coupled_oscillators](/06_design_insights/quadrature_and_coupled_oscillators) |
| **FOM / FOM$_{jitter}$** | 品質指標／jitter 版品質指標 | FOM 把 $\mathcal{L}$、$(f_0/\Delta f)^2$、$P$ 湊成拓樸間可比較的單一數字，且有理論天花板 $173.8-10\log_{10}F_{eff}$；FOM$_{jitter}$ 把 $\mathcal{L}$ 換成直接的 $\sigma_t$。 | [fom_limit](/06_design_insights/fom_limit) ／ [pll_noise_budget](/06_design_insights/pll_noise_budget) |
| **$K_{push}$**（supply pushing） | 電源推移係數 | 每 1 V 電源變動把振盪頻率推多少（$\partial f_0/\partial V_{DD}$），與 $K_{VCO}$ 數學上完全平行；理想上應為 0。 | [varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing) |
| **TDC (Time-to-Digital Converter)** | 時間數位轉換器 | 把兩個邊緣的時間差量成一個整數；有限解析度 $\Delta t_{res}$ 變成 ADPLL 的 in-band 量化雜訊。 | [adpll_tdc_dco](/06_design_insights/adpll_tdc_dco) |
| **DCO (Digitally Controlled Oscillator)** | 數位控制振盪器 | 用開關電容組而非連續 varactor 電壓調頻；有限頻率解析度 $\Delta f_{res}$ 變成 out-of-band 量化雜訊。 | [adpll_tdc_dco](/06_design_insights/adpll_tdc_dco) |
| **JTOL (jitter tolerance)** | 抖動容忍度 | CDR 迴路能追多少輸入 jitter 而不吃掉眼圖裕度的規格曲線 $(\text{UI}-\text{TJ}_{eye})/\lvert1-H(f)\rvert$，低／中／高頻各段斜率不同。 | [cdr_bang_bang_jtol](/06_design_insights/cdr_bang_bang_jtol) |
| **BBPD / Alexander PD** | 二元（bang-bang）相位偵測器 | 只輸出早／晚 $\text{sign}(\Delta t)$ 的相位偵測器，沒有線性增益；迴路頻寬其實是由 jitter 的 rms 值決定。 | [cdr_bang_bang_jtol](/06_design_insights/cdr_bang_bang_jtol) |
| **FOM$_T$**（tuning-range-normalized FOM） | 調諧範圍正規化品質指標 | 把 FOM 加上 $20\log_{10}(\text{TR}\%/10)$ 修正項，讓寬調諧範圍的設計不被「同 FOM」低估；外部經驗慣例，非恆等式。 | [design_recipe](/06_design_insights/design_recipe) |
| **design recipe**（spec-driven design） | 規格驅動設計配方 | 從規格（$\mathcal{L}$、$P$、調諧範圍）反推拓樸選擇、tank 元件值、偏壓電流的 7 步標準流程。 | [design_recipe](/06_design_insights/design_recipe) |

---

## 嚴謹數學基礎（外部文獻）

| 英文 | 中文 | 一句話直覺 | 出處頁 |
|---|---|---|---|
| **PPV (Perturbation Projection Vector)** | 擾動投影向量 **(外部)** | ISF 的嚴謹一般化：把擾動投影到相位方向的向量；對應 Demir 等人 2000 的理論。**不在 5 篇 PDF 內。** | [effective_isf](/03_isf_core_theory/effective_isf) |
| **adjoint method** | 伴隨法 **(外部)** | 從週期穩態解算 PPV/ISF 的數值方法（解伴隨系統）。**不在 5 篇 PDF 內。** | [effective_isf](/03_isf_core_theory/effective_isf) |
| **Floquet theory** | Floquet 理論 **(外部)** | 週期係數線性系統的穩定性理論；給出 PPV 的數學地基。**不在 5 篇 PDF 內。** | [effective_isf](/03_isf_core_theory/effective_isf) |
| **Wiener–Khinchin theorem** | 維納–辛欽定理 **(外部)** | PSD 是自相關函數的傅立葉轉換；連接時域與頻域雜訊。標準隨機程序定理。 | [math_identities](/99_appendix/math_identities) |
| **Leeson model** | Leeson 模型 **(外部)** | 1966 的經驗相位雜訊模型；ISF 理論把它涵蓋為特例。**不在 5 篇 PDF 內。** | [references](/99_appendix/references) |

---

## 一句話速記（最常混淆的幾組）

- **phase noise vs timing jitter**：同一件事，前者頻域（dBc/Hz）、後者時域（fs）；
  $\sigma_t=\sigma_\phi/(2\pi f_0)$ 互換。
- **phase perturbation vs amplitude perturbation**：相位**留**、振幅**被拉回**——所以 phase noise 才是主角。
- **LTI vs LTV**：差在「脈衝響應看不看絕對時刻 $\tau$」；振盪器是 LTV。
- **$c_0$ vs $1/f^3$ corner**：$c_0$ 決定 flicker 上不上轉；$1/f^3$ corner $=\omega_{1/f}(c_0/c_1)^2$，
  **不等於** device 的 $\omega_{1/f}$。
- **device $1/f$ corner $\omega_{1/f}$ vs phase-noise $1/f^3$ corner $\Delta\omega_{1/f^3}$**：兩個不同的東西，
  別搞混（見 [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion)）。

## 延伸閱讀

- 嚴格符號與單位：[notation](/00_overview/notation)
- 數學工具箱：[math_identities](/99_appendix/math_identities)
- 完整文獻清單與引用慣例：[references](/99_appendix/references)
- 公式索引：[equation_index](/01_paper_map/equation_index)
