---
title: 速查表 Cheat Sheet
description: 一頁速查：核心公式、canonical 數值、單位換算、設計旋鈕、五篇論文。考前/設計前掃一眼。
---

# 速查表 Cheat Sheet

一頁把全站最常用的公式、數值與旋鈕濃縮起來。每條都連回完整推導頁。

## 核心公式（全部已對照原始 PDF）

| 主題 | 公式 | 來源 |
|---|---|---|
| ISF 操作定義 | $\Delta\phi=\dfrac{\Gamma(\omega_0\tau)}{q_{max}}\Delta q$ | [P1] Eq.(10)(11) → [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) |
| LTV 相位響應 | $\phi(t)=\dfrac{1}{q_{max}}\displaystyle\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau$ | [P1] Eq.(11) → [convolution](/03_isf_core_theory/convolution_derivation) |
| ISF Fourier | $\Gamma=\dfrac{c_0}{2}+\sum_n c_n\cos(n\omega_0\tau+\theta_n)$ | [P1] Eq.(12) → [fourier](/03_isf_core_theory/fourier_series_of_isf) |
| Parseval / rms | $\sum_{n=0}^\infty c_n^2=2\Gamma_{rms}^2$ | [P1] Eq.(20) → [rms_isf](/03_isf_core_theory/rms_isf) |
| 白噪 1/f² | $\mathcal{L}=10\log_{10}\!\Big(\dfrac{\Gamma_{rms}^2}{q_{max}^2}\dfrac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\Big)$ | [P1] Eq.(21) → [white_noise](/03_isf_core_theory/white_noise_to_phase_noise) |
| flicker 1/f³ | $\mathcal{L}=10\log_{10}\!\Big(\dfrac{c_0^2}{q_{max}^2}\dfrac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\dfrac{\omega_{1/f}}{\Delta\omega}\Big)$ | [P1] Eq.(23) → [flicker](/03_isf_core_theory/flicker_noise_upconversion) |
| 1/f³ corner | $\Delta\omega_{1/f^3}=\omega_{1/f}\dfrac{c_0^2}{2\Gamma_{rms}^2}$ | [P1] Eq.(24) |
| SSB↔PSD | $\mathcal{L}(\Delta f)\approx\tfrac12 S_\phi(\Delta f)$ | [psd](/02_foundations/psd_phase_noise_jitter) |
| phase→time | $\Delta t=\dfrac{\Delta\phi}{2\pi f_0}$ | 標準 |
| rms jitter | $\sigma_t=\dfrac{1}{2\pi f_0}\sqrt{\displaystyle\int_{f_1}^{f_2}S_\phi\,df}$ | [serdes](/06_design_insights/serdes_clocking_connection) |
| 累積 jitter | $\sigma_{\Delta t}=\kappa\sqrt{\Delta t}$，$\kappa=\dfrac{\Gamma_{rms}}{q_{max}}\sqrt{\tfrac12\tfrac{\overline{i_n^2}}{\Delta f}}$ | [P2] Eq.(8)(12) |
| ring 頻率 | $f_0=\dfrac{1}{2N\tau_D}$ | [P2] Eq.(14) |
| ring $\Gamma_{rms}$ | $\Gamma_{rms}=\sqrt{\dfrac{2\pi^2}{3\eta^3}\dfrac{1}{N^{1.5}}}\Rightarrow\Gamma_{rms}\propto N^{-3/4}$ | [P2] Eq.(16) |
| ring FOM | $\mathcal{L}=\dfrac{8}{3\eta}\dfrac{kT}{P}\dfrac{V_{DD}}{V_{char}}\Big(\dfrac{f_0}{\Delta f}\Big)^2$（無 $N$！） | [P2] Eq.(23) |
| 廣義 Adler | $\dfrac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta)$，$\Omega=\langle\tilde\Gamma\,i_{inj}\rangle$ | [P3] Eq.(30)(33) |
| APF / 振幅衰減 | $\tau_0=\dfrac{2Q}{\omega_{osc}}$，$\tilde\Lambda_1=\dfrac{\tau_0}{q_{max}}\angle0°$（與 ISF quadrature） | [P4] Eq.(25)(26) |

## Canonical 數值（全站一致）

| 例 | 設定 | 結果 |
|---|---|---|
| A：impulse→time | $q_{max}=1$ pC、$\Delta q=1$ fC、$\Gamma=0.5$、$f_0=5$ GHz | $\Delta\phi=5\times10^{-4}$ rad、$\Delta t=15.9$ fs |
| B：白噪 $\mathcal{L}$ | $\Gamma_{rms}=0.5$、$q_{max}=1$ pC、$S_i=10^{-24}$ A²/Hz、$\Delta f=1$ MHz | $\mathcal{L}=-148$ dBc/Hz |
| C：jitter 積分 | $\mathcal{L}(1\text{MHz})=-100$ dBc/Hz、1/f²、1→100 MHz、5 GHz | $\sigma_t=447.9$ fs |
| ring FOM | $\gamma=2/3$、$V_{DD}/V_{char}=3$、$P=1$ mW、其餘同上 | $\mathcal{L}\approx-91$ dBc/Hz |

> 想自己掃參數？用 [互動計算器](/04_simulation_labs/interactive_calculator)。

## 5 GHz 換算記憶點

- $1$ mrad $\approx 32$ fs；$1$ rad $\approx 31.8$ ps；週期 $=200$ ps。
- dBc/Hz → linear：$10^{\mathcal{L}/10}$；$S_\phi=2\times$linear。
- $2\times q_{max}$ 或 $\tfrac12\Gamma_{rms}$ → $\mathcal{L}$ 降 **6 dB**。

## 設計旋鈕（降 phase noise）

| 想降 | 旋鈕 | 為什麼 |
|---|---|---|
| 1/f²（白噪） | ↑ $q_{max}$（swing/能量）、↓ $\Gamma_{rms}$ | $\mathcal{L}\propto\Gamma_{rms}^2/q_{max}^2$ |
| 1/f³（close-in） | 波形**對稱** → ↓ $c_0$ | corner $\propto c_0^2/\Gamma_{rms}^2$ |
| jitter（時域） | 同上（同一 $\Gamma_{rms}^2/q_{max}^2$）；或鎖 PLL/CDR | $\kappa\propto\Gamma_{rms}/q_{max}$ |
| 在哪注入 noise | 避開 $\lvert\Gamma\rvert$ 大（slope 小）的相位 | cyclostationary $\Gamma_{eff}=\Gamma\alpha$ |

## 五篇論文一句話

- **[P1]** Hajimiri–Lee 1998：ISF 理論本體（振盪器是 LTV）。
- **[P2]** 1999：ISF 套到 ring，jitter/PN 封閉式、$N$-independence。
- **[P3]** Hong 2019 I：ISF 推廣 Adler → 廣義 injection locking。
- **[P4]** Hong 2019 II：APF（振幅版 ISF）、$\tau_0=2Q/\omega_0$、frequency division。
- **[P5]** sense amplifier 論文，**與 ISF 無關**（誠實標註）。

完整對照見 [paper_summary_table](/01_paper_map/paper_summary_table)、[equation_index](/01_paper_map/equation_index)。
