---
title: 速查表 Cheat Sheet
description: 一頁速查：核心公式、canonical 數值、單位換算、設計旋鈕、五篇論文，加上 v5–v8 速查列（jitter 核、κ↔D↔線寬字典、App.B 閉式、M:N 鎖定、PLL peaking、FOM、SerDes）。考前/設計前掃一眼。
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
| ring 頻率 | $f_0=\dfrac{1}{2N\tau_D}$ | [P2] Eq.(15) |
| ring $\Gamma_{rms}$ | $\Gamma_{rms}=\sqrt{\dfrac{2\pi^2}{3\eta^3}}\;\dfrac{1}{N^{1.5}}\Rightarrow\Gamma_{rms}\propto N^{-3/2}$（$\eta=0.75$ 時 $\approx4/N^{1.5}$，即 [P2] Fig.8 實線；根號只含常數） | [P2] Eq.(16) |
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

## v5–v8 速查（jitter 核／κ↔D↔線寬／App.B／M:N 鎖定／PLL／FOM／SerDes）

一律用「本頁欄位 = 全文抄，慣例旗標照抄」；連結是唯一推導頁。

### jitter 核（三核＋白噪閉式）— [jitter_kernels](/02_foundations/jitter_kernels)

| 核 | 公式（單邊 $S_\phi$、$\int_0^\infty$ 慣例） | 白噪 FM 閉式 |
|---|---|---|
| TIE（0 階） | $\sigma_{TIE}^2=\dfrac{1}{\omega_0^2}\displaystyle\int_{f_1}^{f_2}S_\phi\,df$ | — |
| N-period（1 階差分） | $\sigma_P^2(N)=\dfrac{1}{\omega_0^2}\displaystyle\int_0^\infty S_\phi\,4\sin^2(\pi fNT)\,df$ | $=\kappa^2NT$（精確＝[P2] Eq.(8)） |
| cycle-to-cycle（2 階差分） | $\sigma_{c2c}^2=\dfrac{1}{\omega_0^2}\displaystyle\int_0^\infty S_\phi\,16\sin^4(\pi fT)\,df$ | $=2\kappa^2T\Rightarrow\sigma_{c2c}=\sqrt2\,\sigma_P(1)$ |

> 前置常數是 $1/\omega_0^2$，**不是** $2/\omega_0^2$（那個 2 屬雙邊譜或 $\mathcal{L}=\tfrac12S_\phi$ 記帳）。

### κ↔D↔線寬↔ADEV↔$S_\phi$ 字典（含 19.9/39.8 mHz canonical）— [diffusion_dictionary](/03_isf_core_theory/diffusion_dictionary)

主角：$\kappa^2=\dfrac{\Gamma_{rms}^2}{2q_{max}^2}\dfrac{\overline{i_n^2}}{\Delta f}$（[P2] Eq.(11)/(12)）；canonical（$\Gamma_{rms}=0.5$）$\kappa^2=0.125$ rad²/s，真 LC（$\Gamma_{rms}=1/\sqrt2$）$=0.25$。

| 衣服 | 公式 | canonical 值 |
|---|---|---|
| $\kappa$（相位）／$\kappa_t$（時間） | $\sigma_{\Delta\phi}=\kappa\sqrt{\Delta t}$；$\kappa_t=\kappa/\omega_0$ | $\kappa=0.354$ rad/$\sqrt{\text{s}}$ |
| $D$ 慣例甲／乙 | $\mathrm{Var}=D_{甲}\vert t\vert=2D_{乙}\vert t\vert\Rightarrow D_{甲}=\kappa^2,\ D_{乙}=\kappa^2/2$ | $0.125$／$0.0625$ |
| Lorentzian 3-dB 線寬 | $\Delta f_{3\mathrm{dB}}=\kappa^2/(2\pi)$ | **19.9 mHz**（真 LC **39.8 mHz**） |
| $S_\phi$ 係數（單邊） | $S_\phi=2\kappa^2/(2\pi f)^2$ | $b_{-2}=6.33\times10^{-3}$ rad²·Hz |
| white-FM ADEV | $\sigma_y(\tau)=\kappa/(2\pi f_0\sqrt\tau)$ | $1.13\times10^{-11}$@1s（5 GHz） |

> 三個 factor-of-2 家族要先問清楚：單邊/雙邊 PSD、$\mathrm{Var}=D\vert t\vert$ vs $2D\vert t\vert$、SSB $/2$ vs $/4$。

### App.B 閉式：$\Gamma_{rms}(A,N)$、$c_0$、corner — [asymmetric_isf_closed_form](/03_isf_core_theory/asymmetric_isf_closed_form)

$$
\Gamma_{rms}^2=\frac{2\pi^2}{3\eta^3}\frac{1}{N^3}\left[4\frac{1+A^3}{(1+A)^3}\right],\quad
\Gamma_{dc}=\frac{2\pi}{\eta^2}\frac{1}{N^2}\left(\frac{1-A}{1+A}\right),\quad c_0=2\Gamma_{dc}
$$

$$
f_{1/f^3}=f_{1/f}\cdot\frac{3}{2\eta N}\cdot\frac{(1-A)^2}{1-A+A^2}\qquad([\text{P2}]\ \text{Eq.}(52)\text{–}(57),\ \text{p.803})
$$

$A\equiv f'_{rise}/f'_{fall}$；$A=1$ 精確退化為 [P2] Eq.(16)（$\Gamma_{rms}\propto N^{-1.5}$）；corner 在 $A=1$ 二次趨零、對 $A\to1/A$ 對稱、$\propto1/N$。慣例旗標：此 corner 為 [P2] Eq.(7)/(57) 值；[P1] Eq.(24)（$c_0=2\Gamma_{dc}$ 代入）$=2\times$ 本值。

### [P1] 附錄：$\Gamma=f'/(f'^2+f''^2)$ — [isf_from_waveform](/03_isf_core_theory/isf_from_waveform)

$$
\Gamma(x)=\frac{f'}{f'^{\,2}+f''^{\,2}}\qquad([\text{P1}]\ \text{Eq.}(37),\ \text{p.193})
$$

$f=\cos x$ 代入：分母 $\sin^2+\cos^2=1$，$\Gamma=-\sin x$ 精確成立，波峰處有界（解掉 $1/\text{slope}$ heuristic 的發散）。三法排序：A 打脈衝（最準）→ B 本式（一週期波形足夠）→ C 斜率近似 $\Gamma=f'/f_{max}'^2$（最快，ring 專用，Eq.(38)）。

### 鎖定雜訊整形 corner＝$\omega_L\cos\theta_{ss}$ — [injection_locking_noise](/06_design_insights/injection_locking_noise) Part A

$$
\omega_c\equiv\omega_L\cos\theta_{ss}=\sqrt{\omega_L^2-\Delta\omega^2}\qquad([\text{P3}]\ \text{Eq.}(40)\ \text{的 pull-in frequency})
$$

鎖定中心（$\Delta\omega=0$）corner 最寬；邊緣（$\Delta\omega\to\omega_L$）$\cos\theta_{ss}\to0$，自身雜訊高通抑制**完全消失**。自身雜訊高通、參考雜訊低通（一階 PLL 圖像）。

### 最佳注入波形 $\omega_L^*=I_{rms}\tilde\Gamma_{rms}$ — [injection_locking_noise](/06_design_insights/injection_locking_noise) 末節

固定 $I_{rms}\equiv\sqrt{\langle i_{inj}^2\rangle}$ 下，Cauchy–Schwarz 給 lock range 上限（[P3] Eq.(43)–(45), p.2119–2120）：

$$
\omega_L^*=I_{rms}\,\tilde\Gamma_{rms},\qquad i_{inj,0}^*(x)=\pm\frac{I_{rms}}{\tilde\Gamma_{rms}}\tilde\Gamma(x)
$$

等號 ⟺ 注入波形與 ISF 同形（matched filter）。純弦 ISF：正弦注入已最佳（增益 1）。ring 窄脈衝 ISF：增益 $\approx\sqrt{\eta N/3}$（$N=17$ 時 $\approx2.06$，對照 [P3] Fig.19 "almost doubled"）。

### M:N 次諧波鎖定／ILFD：$\lvert\tilde\Gamma_N\rvert$ — [paper_004](/05_paper_deep_dives/paper_004_injection_locking_part2)

鎖定 $M\omega_{inj}=N\omega_{osc}$ 時（$M=1$ 為 ÷$N$ ILFD），半鎖定範圍只騎在 ISF 第 $N$ 諧波上（[P4] Eq.(28)–(30), p.2129，已核實）：

$$
\Omega(\theta)=\frac12 I_{inj}\lvert\tilde\Gamma_N\rvert\cos(N\theta+\angle\tilde\Gamma_N)\ \Rightarrow\
\omega_L=\frac12 I_{inj}\lvert\tilde\Gamma_N\rvert=\frac{I_{inj}\,c_N}{2\,q_{max}}
$$

半波對稱 ISF（$c_2=c_4=\cdots=0$）⟹ ÷2 一階內鎖不上——差動節點對稱是 phase-noise 的好消息，卻是 ILFD 的壞消息（解法：換到 tail 節點取 $c_2$）。

### ADEV floor：$\sqrt{2\ln2\cdot h_{-1}}$ — [allan_variance](/02_foundations/allan_variance)

$$
\sigma_{y,\text{floor}}=\sqrt{2\ln2\cdot h_{-1}}\approx1.1774\sqrt{h_{-1}}\qquad(\text{flicker FM，}\tau\text{-無關 floor})
$$

canonical（$1/f^3$ corner $=3.2$ kHz）：floor $\approx1.06\times10^{-9}$（1.1 ppb）；knee $\tau_{knee}=0.3607/f_c\approx113\ \mu$s（白 FM $\tau^{-1/2}$ 段撞上 floor）。

### PLL peaking：$\zeta=0.707\to2.09$ dB — [pll_noise_budget](/06_design_insights/pll_noise_budget) 補充推導

type-II 帶零點必有 peaking：$f_{pk}=f_n\sqrt{2/(s+1)}$，$s=\sqrt{1+1/\zeta^4}$（黃金比例彩蛋：$\zeta=1/\sqrt2$ 時峰值 $=\varphi=1.618$）。

| $\zeta$ | $f_{pk}/f_n$ | peaking (dB) | phase margin |
|---|---|---|---|
| 0.707 | 0.786 | **2.09** | 65.5° |
| 1.0 | 0.707 | 1.25 | 76.3° |

級聯 20 級 SONET regenerator：$20\times2.09=41.8$ dB，故規格壓在 **0.1 dB** 量級／級。

### FOM＝$173.8-10\log_{10}F_{eff}$ — [fom_limit](/06_design_insights/fom_limit)

$$
\mathrm{FOM}=173.8\ \text{dB}-10\log_{10}F_{eff}\qquad(T=300\ \text{K，配對 }1\cdot kT\text{，不是 }2kT)
$$

ring 天花板（$\gamma=2/3,\eta=1$）：$F_{eff,min}=32/9\Rightarrow\mathrm{FOM}_{max}^{ring}=168.32$ dB；LC 天花板隨 $Q$ 上升（$F_{eff}\propto1/Q^2$）。

### aperture SNR：$-20\log_{10}(2\pi f_{in}\sigma_t)$ — [adc_aperture_jitter](/06_design_insights/adc_aperture_jitter)

$$
\text{SNR}_{jitter}=-20\log_{10}(2\pi f_{in}\sigma_t)\ \text{dB},\qquad \text{ENOB}=\frac{\text{SNR}-1.76}{6.02}\ \text{bit}
$$

canonical $\sigma_t=447.9$ fs：$f_{in}=f_0=5$ GHz 時 $2\pi f_{in}\sigma_t=\sigma_\phi=14.07$ mrad ⟹ SNR $=37.0$ dB（例 C 直接搬過來）。

### TJ＝$\mathrm{DJ}_{\delta\delta}+2Q^{-1}(\mathrm{BER})\sigma$ — [dj_dual_dirac](/06_design_insights/dj_dual_dirac)

$$
\mathrm{TJ}(\mathrm{BER})=\mathrm{DJ}_{\delta\delta}+2\,Q^{-1}(\mathrm{BER})\,\sigma
$$

BER$=10^{-12}\Rightarrow Q^{-1}=7.034$，故 $\mathrm{TJ}=\mathrm{DJ}_{\delta\delta}+14.07\,\sigma$。DJ 不隨 BER 變（有界一次吃掉）；RJ 項隨 BER 嚴苛只緩慢長大（$10^{-12}\to10^{-15}$：$14.07\sigma\to15.88\sigma$）。

### ×N／÷N／buffer 記帳 — [clock_chain_budget](/06_design_insights/clock_chain_budget)

| 元件 | 相位關係 | $\mathcal{L}(f)$ 記帳 |
|---|---|---|
| 理想 ×N 倍頻 | $\phi_{out}=N\phi_{in}$ | $\mathcal{L}+20\log_{10}N$ |
| 理想 ÷N 除頻 | $\phi_{out}=\phi_{in}/N$ | $\mathcal{L}-20\log_{10}N$ |
| 過 PLL（×N） | in-band 跟 ref、out-of-band 跟 VCO | $N^2S_{ref}\lvert H_{lp}\rvert^2+S_{vco}\lvert H_{hp}\rvert^2$ |
| buffer/divider 加成床 | $\phi_{out}=\phi_{in}+\phi_{add}$（不相關） | $\mathcal{L}_{out}=10\log_{10}(10^{\mathcal{L}_{in}/10}+10^{\mathcal{L}_{buf}/10})$（**先轉線性、相加、再轉回 dB**） |

守恆量：理想 ×N/÷N 下，**以秒計的 $\sigma_t$ 全程不變**（只有 $\mathcal{L}$/rad 記帳在變）。

### $K_{push}$ 路徑：$S_\phi=K^2S_v/\Delta f^2$ — [varactor_tuning_supply_pushing](/06_design_insights/varactor_tuning_supply_pushing)

$$
K_{VCO}\equiv\frac{\partial f_0}{\partial V_{tune}},\quad K_{push}\equiv\frac{\partial f_0}{\partial V_{DD}},\qquad
S_\phi(\Delta f)=\frac{K_{VCO}^2\,S_v(\Delta f)}{\Delta f^2}\ \ (\text{supply 版同式，}K_{VCO}\to K_{push},\ S_v\to S_{v,DD})
$$

與 ISF 白噪結果並排：分母同是 $\Delta\omega^2$／$\Delta f^2$ 的積分器，只是入口不同（$\Gamma_{rms}/q_{max}$ vs $2\pi K_{VCO}$）。白噪 tune/supply → $1/f^2$；$1/f$ tune/supply → $1/f^3$（與 device $c_0$ 機制平行）。lab_38 第一性驗證 $K_{push}$（β 比 1.002）。

## 五篇論文一句話

- **[P1]** Hajimiri–Lee 1998：ISF 理論本體（振盪器是 LTV）。
- **[P2]** 1999：ISF 套到 ring，jitter/PN 封閉式、$N$-independence。
- **[P3]** Hong 2019 I：ISF 推廣 Adler → 廣義 injection locking。
- **[P4]** Hong 2019 II：APF（振幅版 ISF）、$\tau_0=2Q/\omega_0$、frequency division。
- **[P5]** sense amplifier 論文，**與 ISF 無關**（誠實標註）。

完整對照見 [paper_summary_table](/01_paper_map/paper_summary_table)、[equation_index](/01_paper_map/equation_index)。
