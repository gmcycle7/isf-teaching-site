---
title: 公式推導索引 Equation Index
description: 每條核心公式 → 最終形式、推導頁、來源論文。
---

# 公式推導索引 Equation Index

> 本頁由 `scripts/build_equation_index.py` 從 `extracted/extracted_equations.json` 自動產生。
> 標記 ⚠️ 者表示確切常數/形式仍需人工對照 PDF 確認。

| # | Concept | Final Formula | 推導頁 Derivation | 來源 Source | Notes |
|---|---|---|---|---|---|
| 1 | impulse charge | $\Delta q = \int i(t)\, dt$ | [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) | paper_001 (general.pdf), around Eq. (9), p.182 | step |
| 2 | charge to voltage step | $\Delta V = \dfrac{\Delta q}{C_{node}}$ | [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) | paper_001, Eq. (9), p.182 | step |
| 3 | impulse-to-phase (ISF definition in operational form) | $\Delta\phi = \dfrac{\Gamma(\omega_0\tau)}{q_{max}}\,\Delta q$ | [impulse_to_phase_shift](/03_isf_core_theory/impulse_to_phase_shift) | paper_001, from Eq. (10)-(11), p.182 | final |
| 4 | excess-phase impulse response (LTV) | $h_\phi(t,\tau) = \dfrac{\Gamma(\omega_0\tau)}{q_{max}}\,u(t-\tau)$ | [isf_definition](/03_isf_core_theory/isf_definition) | paper_001, Eq. (10), p.182 | final |
| 5 | LTV phase response (convolution) | $\phi(t) = \dfrac{1}{q_{max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)\,i_n(\tau)\,d\tau$ | [convolution_derivation](/03_isf_core_theory/convolution_derivation) | paper_001, Eq. (11), p.182 | final |
| 6 | ISF Fourier series | $\Gamma(\omega_0\tau) = \dfrac{c_0}{2} + \sum_{n=1}^{\infty} c_n\cos(n\omega_0\tau+\theta_n)$ | [fourier_series_of_isf](/03_isf_core_theory/fourier_series_of_isf) | paper_001, Eq. (12), p.183 | final |
| 7 | rms ISF (Parseval) | $\sum_{n=0}^{\infty} c_n^2 = \dfrac{1}{\pi}\int_0^{2\pi}\vert \Gamma(x)\vert ^2 dx = 2\,\Gamma_{rms}^2$ | [rms_isf](/03_isf_core_theory/rms_isf) | paper_001, Eq. (20), p.185 | final |
| 8 | white noise phase noise (1/f^2) | $\mathcal{L}\{\Delta\omega\} = 10\log_{10}\!\left(\dfrac{\Gamma_{rms}^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{4\,\Delta\omega^2}\right)$ | [white_noise_to_phase_noise](/03_isf_core_theory/white_noise_to_phase_noise) | paper_001, Eq. (21), p.185 | final |
| 9 | flicker noise upconversion (1/f^3) | $\mathcal{L}\{\Delta\omega\} = 10\log_{10}\!\left(\dfrac{c_0^2}{q_{max}^2}\cdot\dfrac{\overline{i_n^2}/\Delta f}{8\,\Delta\omega^2}\cdot\dfrac{\omega_{1/f}}{\Delta\omega}\right)$ | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) | paper_001, Eq. (23), p.185 | final |
| 10 | 1/f^3 corner | $\Delta\omega_{1/f^3} = \omega_{1/f}\cdot\dfrac{c_0^2}{2\,\Gamma_{rms}^2}$ | [flicker_noise_upconversion](/03_isf_core_theory/flicker_noise_upconversion) | paper_001, Eq. (24), p.185 | final |
| 11 | SSB phase noise vs phase PSD | $\mathcal{L}(\Delta f) \approx \tfrac{1}{2} S_\phi(\Delta f)$ | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) | standard small-angle relation; consistent with paper_001 usage | final |
| 12 | phase error to timing error | $\Delta t = \dfrac{\Delta\phi}{2\pi f_0}$ | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) | standard; used throughout paper_002 and SerDes practice | final |
| 13 | phase variance from PSD | $\sigma_\phi^2 = \int_{f_1}^{f_2} S_\phi(f)\, df$ | [psd_phase_noise_jitter](/02_foundations/psd_phase_noise_jitter) | standard | final |
| 14 | rms jitter from phase variance | $\sigma_t = \dfrac{\sigma_\phi}{2\pi f_0} = \dfrac{1}{2\pi f_0}\sqrt{\int_{f_1}^{f_2} S_\phi(f)\, df}$ | [serdes_clocking_connection](/06_design_insights/serdes_clocking_connection) | standard; SerDes clocking | final |
| 15 | accumulated (ring) jitter random walk | $\sigma_{\Delta t} = \kappa\,\sqrt{\Delta t}$ | [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model) | paper_002, Eq. (8), p.792 (kappa via Eq.(12), p.793) | final |
| 16 | ring frequency vs stages | $f_0 = \dfrac{1}{2 N \tau_D}$ | [lc_vs_ring](/06_design_insights/lc_vs_ring) | paper_002, Eq. (14), p.794 | final |
| 17 | ring rms ISF scaling | $\Gamma_{rms}=\sqrt{\dfrac{2\pi^2}{3\eta^3}\cdot\dfrac{1}{N^{1.5}}}\;\Rightarrow\;\Gamma_{rms}\propto N^{-3/4}\ (\Gamma_{rms}^2\propto N^{-3/2})$ | [lc_vs_ring](/06_design_insights/lc_vs_ring) | paper_002, Eq. (16), p.794 (verified verbatim) | final (verified) |
| 18 | ring phase noise FOM (white) | $\mathcal{L}\{\Delta f\}=\dfrac{8}{3\eta}\cdot\dfrac{kT}{P}\cdot\dfrac{V_{DD}}{V_{char}}\cdot\left(\dfrac{f_0}{\Delta f}\right)^2\quad(\text{min at }V_T=0:\ \tfrac{16\gamma}{3\eta})$ | [lc_vs_ring](/06_design_insights/lc_vs_ring) | paper_002, Eq. (23),(25), p.796。前置係數為 $8/(3\eta)$（$\eta$ 為級延遲比例常數 Eq.14，$\approx 1$）；$\gamma$ 僅透過 $V_{char}=\Delta V/\gamma$ 進入。（v2 曾誤改為 $8/(3\gamma)$ 並誤標「逐字核實」，v3 已對照原始 PDF p.796 更正。） | final (verified) |
| 19 | Leeson model (comparison only) | $\mathcal{L}(\Delta\omega) = 10\log_{10}\!\left[\dfrac{2FkT}{P_s}\left(1+\left(\dfrac{\omega_0}{2Q\Delta\omega}\right)^2\right)\left(1+\dfrac{\omega_{1/f^3}}{\vert \Delta\omega\vert }\right)\right]$ | [equation_index](/01_paper_map/equation_index) | Leeson (1966), Proc. IEEE 54(2):329-330, DOI 10.1109/PROC.1966.4682 (citation verified; external, not in the 5 PDFs). Discussed in paper_001 intro. | reference |
| 20 | generalized Adler / phase equation (injection) | $\frac{d\theta}{dt}=(\omega_0-\omega_{inj})+\Omega(\theta),\quad \Omega(\theta)=\frac{1}{T_{inj}}\int_{T_{inj}}\tilde\Gamma(\omega_{inj} t+\theta)\,i_{inj}(t)\,dt,\ \ \tilde\Gamma=\Gamma/q_{max}$ | [paper_003_injection_locking_part1](/05_paper_deep_dives/paper_003_injection_locking_part1) | paper_003 (Hong Part I 2019)：$\tilde\Gamma=\Gamma/q_{max}$ Eq.(26)；時間平均之廣義 Adler 方程 Eq.(30), p.2113（原文平均項取 **＋** 號，平均週期 $T_{inj}$）；鎖定範圍 $\omega_L=\tfrac{1}{2} I_{inj}\vert\tilde\Gamma_1\vert$ Eq.(35), p.2114。本站 $\Omega(\theta)$ 與差頻 $(\omega_0-\omega_{inj})$ 同號相加，符號慣例與 [P3] 一致。 | final (verified) |
| 21 | amplitude perturbation function (APF) | $\tilde\Lambda\ (\text{APF}):\ d(t,\phi)=e^{-t/\tau_0},\ \tau_0=\frac{2Q}{\omega_{osc}};\quad \tilde\Gamma_1=\tfrac{1}{q_{max}}\angle90^\circ,\ \tilde\Lambda_1=\tfrac{\tau_0}{q_{max}}\angle0^\circ\ (\text{quadrature})$ | [paper_004_injection_locking_part2](/05_paper_deep_dives/paper_004_injection_locking_part2) | paper_004 (Hong Part II 2019), Eq.(25),(26),(27), p.2128 (verified verbatim) | final (verified) |
| 22 | PPV / adjoint (broader literature, NOT in the 5 PDFs) | $\dot{\phi}(t) = v_1^T(t)\, B(t)\, \xi(t)\quad\text{(Demir et al. PPV form)}$ | [effective_isf](/03_isf_core_theory/effective_isf) | Demir-Mehrotra-Roychowdhury (2000), IEEE TCAS-I 47(5):655-674, DOI 10.1109/81.847872 (citation verified; external, not in the 5 PDFs). | reference |
| 23 | ring kappa (jitter rate) | $\kappa=\dfrac{\Gamma_{rms}}{q_{max}}\sqrt{\dfrac{1}{2}\dfrac{\overline{i_n^2}}{\Delta f}}\quad(\sigma_{\Delta t}=\kappa\sqrt{\Delta t})$ | [lab_03_ring_oscillator_toy_model](/04_simulation_labs/lab_03_ring_oscillator_toy_model) | paper_002, Eq. (12), p.793 (verified verbatim) | final (verified) |
| 24 | ring per-stage device noise | $\dfrac{\overline{i_n^2}}{\Delta f}=4kT\gamma\,g_{d0}=4kT\gamma\,\mu C_{ox}\dfrac{W}{L}\,\Delta V$ | [device_noise_mapping](/06_design_insights/device_noise_mapping) | paper_002, Eq. (17),(18), p.795 (verified verbatim) | final (verified) |
| 25 | Lorentzian carrier lineshape | $S(\Delta\omega)\propto\dfrac{D}{D^2+\Delta\omega^2},\quad \Delta f_{3\mathrm{dB}}=\dfrac{D}{\pi},\quad D=\dfrac{\Gamma_{rms}^2}{2q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$ | [lorentzian_linewidth](/03_isf_core_theory/lorentzian_linewidth) | phase random walk -> exponential carrier autocorrelation -> Lorentzian; resolves 1/f^2 divergence at Df->0. Background: Demir 2000 [E2]. | final (verified) |
| 26 | Allan variance from PSD | $\sigma_y^2(\tau)=2\int_0^\infty S_y(f)\dfrac{\sin^4(\pi f\tau)}{(\pi f\tau)^2}\,df,\quad S_y=\dfrac{f^2}{f_0^2}S_\phi$ | [allan_variance](/02_foundations/allan_variance) | white/flicker/RW FM -> sigma_y ~ tau^{-1/2}, tau^0, tau^{+1/2}. External: Allan 1966 [E1-ext]. | final |
| 27 | PLL output phase-noise budget | $S_{out}=(S_{ref}N^2+S_{cp})\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$ | [pll_noise_budget](/06_design_insights/pll_noise_budget) | sum of all PLL noise sources shaped by their transfer; optimal loop BW minimizes integrated jitter. | final |
| 28 | ISF as harmonic transfer vector (HTM) | $\text{input at } f \to \text{output at } f+kf_0 \text{ with gain } c_k\ (\text{ISF Fourier coeff})$ | [ltv_htm](/99_appendix/ltv_htm) | rigorous LTV / harmonic transfer matrix view; ISF is the phase output's HTM row. External: Zadeh 1950 [E5]. | reference |

## 圖例

- **final**：該主題的最終結果公式。
- **step**：推導過程中的中間步驟。
- **reference**：作為對照/比較的外部模型（未必出自下載的 5 篇 PDF）。
- ⚠️：`manual_verification_needed = true`，請對照原始 PDF 再確認。
