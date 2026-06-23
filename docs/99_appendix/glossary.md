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
| **ring oscillator** | 環形振盪器 | $N$ 級反相器串成環；ISF 集中在 transition、$\Gamma_{rms}\propto N^{-3/4}$。 | [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| **LC oscillator** | LC 振盪器 | tank 諧振、波形近正弦；理想 ISF $=-\sin\theta$。 | [lab_02](/04_simulation_labs/lab_02_lc_oscillator_toy_model) |
| **accumulated jitter** | 累積（長期）jitter | 開環振盪器無絕對時間參考，誤差像隨機漫步 $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$ 成長。 | [lab_03](/04_simulation_labs/lab_03_ring_oscillator_toy_model) |
| **injection locking / pulling** | 注入鎖定／拉扯 | 外部訊號注入把振盪器頻率「拉」向它；同一個 ISF 也主宰這現象（廣義 Adler）。 | [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1) |
| **APF (Amplitude Perturbation Function)** $\Lambda(\phi)$ | 振幅擾動函數 | ISF 之於相位，APF 之於振幅；單位 1/A。理想 LC 中與 ISF 正交（quadrature）。 | [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2) |
| **Adler's equation** | Adler 方程 | 描述 injection-locked 相位差的一階微分方程（1946）；ISF 把它推廣到任意波形。 | [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1) |

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
